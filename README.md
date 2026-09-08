# Python File Integrity Monitor

A beginner-friendly cybersecurity project that creates a trusted SHA-256
baseline for a directory and alerts when files are added, modified, or deleted.
Every check is recorded in a timestamped activity log.

## Why This Project Matters

Unexpected file changes can indicate accidental damage, unauthorized access, or
malicious activity. File integrity monitoring helps defenders identify those
changes. This learning project demonstrates Python, file handling, cryptographic
hashing, logging, command-line interfaces, testing, and basic security monitoring.

> This is an educational tool, not a replacement for an enterprise monitoring
> product. Only monitor systems and files you own or are authorized to inspect.

## Features

- Calculates SHA-256 hashes using memory-efficient chunks
- Creates a JSON baseline of known files
- Detects added, modified, and deleted files
- Prints a simple terminal alert
- Maintains a UTC timestamped activity log
- Skips symbolic links and common development folders
- Uses only the Python standard library
- Includes automated unit tests

## Project Structure

```text
python-file-integrity-monitor/
├── file_integrity_monitor.py
├── tests/
│   └── test_file_integrity_monitor.py
├── docs/
│   ├── PROJECT_PROPOSAL.md
│   └── ARCHITECTURE.md
├── data/                 # Generated baseline (ignored by Git)
├── logs/                 # Generated activity log (ignored by Git)
├── README.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

## Requirements

- Python 3.8 or newer
- Windows, macOS, or Linux
- No third-party packages

## Quick Start

Open a terminal inside the project folder.

### 1. Create a folder to monitor

Windows PowerShell:

```powershell
mkdir monitored_files
Set-Content monitored_files/example.txt "Original content"
```

Linux or macOS:

```bash
mkdir -p monitored_files
printf 'Original content\n' > monitored_files/example.txt
```

### 2. Create the trusted baseline

```bash
python file_integrity_monitor.py init monitored_files
```

Expected result:

```text
[OK] Baseline created for 1 files.
```

### 3. Check file integrity

```bash
python file_integrity_monitor.py check monitored_files
```

If nothing changed:

```text
[OK] No file changes detected.
```

After editing or deleting a monitored file, run the check again:

```text
[ALERT] 1 file change(s) detected!
  - MODIFIED: example.txt
```

The detailed history is stored in `logs/activity.log`.

## Commands

```bash
python file_integrity_monitor.py init DIRECTORY
python file_integrity_monitor.py check DIRECTORY
```

Optional custom paths:

```bash
python file_integrity_monitor.py init DIRECTORY --state my-baseline.json --log my-log.txt
```

Run `init` again only when you intentionally want to trust the current file
state as the new baseline.

## Run the Tests

```bash
python -m unittest discover -s tests -v
```

## How It Works

1. `init` scans every regular file in the selected directory.
2. Each file is read in chunks and given a SHA-256 fingerprint.
3. The fingerprints and metadata are saved in `data/baseline.json`.
4. `check` scans the directory again and compares the fingerprints.
5. Differences are classified as added, modified, or deleted.
6. Results are displayed and written to the activity log with UTC timestamps.

Read the complete [project proposal](docs/PROJECT_PROPOSAL.md) and
[system architecture](docs/ARCHITECTURE.md) for the scope, objectives, design,
data model, and evaluation criteria.

Changing a filename appears as one deletion and one addition. Metadata-only
changes are not alerts because integrity is based on file content.

## Security Limitations

- An attacker who can edit both monitored files and the baseline may bypass it.
- It does not watch continuously; checks run only when the command is executed.
- It does not identify who changed a file or why.
- Permission errors are logged, but inaccessible files cannot be verified.
- SHA-256 verifies content integrity; it does not encrypt files.

For a stronger future version, protect or sign the baseline, schedule periodic
checks, send email notifications, and add a dashboard.

## Learning Outcomes

After completing and explaining this project, you should understand:

- Reading files safely with Python
- Why cryptographic hashes act as file fingerprints
- Comparing saved and current system state
- Recording security events with timestamps
- Returning meaningful command-line exit codes
- Writing basic unit tests

## GitHub Topics

`python` · `cybersecurity` · `file-integrity-monitoring` · `sha256` ·
`security-monitoring` · `beginner-project`
