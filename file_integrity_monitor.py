#!/usr/bin/env python3
"""A small, dependency-free file integrity monitor for learning purposes."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Mapping, Set


DEFAULT_STATE = Path("data/baseline.json")
DEFAULT_LOG = Path("logs/activity.log")
DEFAULT_EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__"}
BUFFER_SIZE = 1024 * 1024


def utc_now() -> str:
    """Return the current time in a readable UTC format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    """Calculate a SHA-256 hash without loading the whole file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        while chunk := file_handle.read(BUFFER_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def paths_to_exclude(root: Path, paths: Iterable[Path]) -> Set[Path]:
    """Resolve state/log paths so the monitor does not monitor its own output."""
    excluded = set()
    for path in paths:
        candidate = path if path.is_absolute() else Path.cwd() / path
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        excluded.add(candidate.resolve())
    return excluded


def scan_directory(root: Path, excluded_files: Set[Path]) -> Dict[str, dict]:
    """Create a snapshot of regular files below root."""
    snapshot: Dict[str, dict] = {}
    for current_dir, dir_names, file_names in os.walk(root, followlinks=False):
        dir_names[:] = [name for name in dir_names if name not in DEFAULT_EXCLUDED_DIRS]
        current_path = Path(current_dir)
        for file_name in file_names:
            path = current_path / file_name
            try:
                if path.is_symlink() or path.resolve() in excluded_files:
                    continue
                stat = path.stat()
                relative_name = path.relative_to(root).as_posix()
                snapshot[relative_name] = {
                    "sha256": sha256_file(path),
                    "size_bytes": stat.st_size,
                    "modified_utc": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(timespec="seconds"),
                }
            except (OSError, PermissionError) as error:
                logging.warning("Could not read %s: %s", path, error)
    return dict(sorted(snapshot.items()))


def save_baseline(state_path: Path, root: Path, files: Mapping[str, dict]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "algorithm": "sha256",
        "created_utc": utc_now(),
        "monitored_path": str(root),
        "files": files,
    }
    state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_baseline(state_path: Path) -> dict:
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError("Baseline not found. Run the init command first.") from error
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read baseline: {error}") from error
    if data.get("version") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError("The baseline file has an unsupported or invalid format.")
    return data


def compare_snapshots(old: Mapping[str, dict], new: Mapping[str, dict]) -> dict:
    old_names, new_names = set(old), set(new)
    return {
        "added": sorted(new_names - old_names),
        "deleted": sorted(old_names - new_names),
        "modified": sorted(
            name
            for name in old_names & new_names
            if old[name].get("sha256") != new[name].get("sha256")
        ),
    }


def configure_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s UTC | %(levelname)s | %(message)s")
    formatter.converter = time.gmtime
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)


def validate_root(target: str) -> Path:
    root = Path(target).expanduser().resolve()
    if not root.exists():
        raise ValueError(f"Target does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Target must be a directory: {root}")
    return root


def initialize(target: str, state_path: Path, log_path: Path) -> int:
    root = validate_root(target)
    excluded = paths_to_exclude(root, [state_path, log_path])
    files = scan_directory(root, excluded)
    save_baseline(state_path, root, files)
    logging.info("Baseline created for %s with %d files", root, len(files))
    print(f"[OK] Baseline created for {len(files)} files.")
    print(f"     State: {state_path.resolve()}")
    return 0


def check(target: str, state_path: Path, log_path: Path) -> int:
    root = validate_root(target)
    baseline = load_baseline(state_path)
    expected_root = Path(baseline["monitored_path"]).resolve()
    if root != expected_root:
        raise ValueError(f"Baseline belongs to {expected_root}, not {root}.")

    excluded = paths_to_exclude(root, [state_path, log_path])
    current = scan_directory(root, excluded)
    changes = compare_snapshots(baseline["files"], current)
    total = sum(len(names) for names in changes.values())

    if total == 0:
        logging.info("Integrity check passed for %s; no changes detected", root)
        print("[OK] No file changes detected.")
        return 0

    print(f"[ALERT] {total} file change(s) detected!")
    for category in ("modified", "deleted", "added"):
        for name in changes[category]:
            message = f"{category.upper()}: {name}"
            logging.warning(message)
            print(f"  - {message}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and check SHA-256 baselines for a directory."
    )
    parser.add_argument("command", choices=["init", "check"])
    parser.add_argument("target", help="Directory to monitor")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    configure_logging(args.log)
    try:
        if args.command == "init":
            return initialize(args.target, args.state, args.log)
        return check(args.target, args.state, args.log)
    except ValueError as error:
        logging.error(str(error))
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
