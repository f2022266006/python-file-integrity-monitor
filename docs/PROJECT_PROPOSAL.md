# Project Proposal

## Project Title

**Python File Integrity Monitor: SHA-256-Based Security Change Detection**

## Background

Important files can be changed accidentally, corrupted, deleted, or modified by
an unauthorized person. A file integrity monitor records a trusted fingerprint
for each file and later compares the current fingerprint with the trusted one.
This gives defenders an early warning that a file may no longer be reliable.

## Problem Statement

Beginners and small laboratory environments need a simple way to detect changes
to important files without installing a complex enterprise security platform.
The proposed application will establish a trusted baseline for a selected
directory and report added, modified, or deleted files during later checks.

## Aim

To design and implement a beginner-friendly Python security tool that uses
SHA-256 hashes to detect file-system changes and records every result in a
timestamped activity log.

## Objectives

1. Calculate a SHA-256 fingerprint for every readable regular file in a selected
   directory.
2. Save file fingerprints and basic metadata in a structured JSON baseline.
3. Compare the trusted baseline with a new scan.
4. Detect and classify added, modified, and deleted files.
5. display clear terminal alerts when changes are found.
6. Record baseline creation, successful checks, warnings, and errors with UTC
   timestamps.
7. Avoid monitoring the program's own baseline and log files.
8. Validate core behavior with automated unit tests.
9. Document installation, operation, limitations, and responsible use.

## Scope

### Included

- Recursive scanning of a user-selected directory
- SHA-256 content hashing
- JSON baseline creation
- Manual integrity checks
- Added, modified, and deleted file detection
- Console alerts and file-based activity logging
- Windows, Linux, and macOS support through standard Python

### Not Included

- Continuous real-time monitoring
- User attribution or attacker identification
- Automatic file restoration
- Malware analysis
- Remote monitoring or cloud storage
- Protection against an attacker who can alter the baseline itself

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-01 | The user can initialize a baseline for an existing directory. |
| FR-02 | The system calculates SHA-256 hashes in memory-efficient chunks. |
| FR-03 | The user can compare the current directory with its baseline. |
| FR-04 | The system reports added, modified, and deleted files separately. |
| FR-05 | The system logs events with UTC timestamps. |
| FR-06 | The system reports invalid paths and missing baselines clearly. |

## Non-Functional Requirements

- **Usability:** Commands and alerts must be understandable to a beginner.
- **Portability:** The project must use only Python's standard library.
- **Efficiency:** Large files must be read in chunks rather than loaded fully.
- **Safety:** Symbolic links and common development directories are skipped.
- **Maintainability:** Scanning, comparison, storage, logging, and CLI logic are
  separated into testable functions.

## Methodology

1. Study cryptographic hashing and file-integrity monitoring.
2. Define the baseline JSON format and command-line interface.
3. Implement directory traversal and SHA-256 hashing.
4. Implement baseline persistence and comparison logic.
5. Add console alerts, timestamps, and activity logging.
6. Test unchanged, modified, added, deleted, and invalid-input cases.
7. Document the project and evaluate its limitations.

## Tools and Technologies

- Python 3.8+
- `hashlib` for SHA-256
- `pathlib` and `os` for file handling
- `json` for baseline storage
- `logging` for activity records
- `argparse` for the command-line interface
- `unittest` for automated testing
- Git and GitHub for version control and presentation

## Expected Outcomes

- A working command-line file integrity monitor
- Reliable classification of common file changes
- A timestamped audit trail
- Automated evidence that the comparison logic works
- A documented beginner cybersecurity portfolio project

## Evaluation Criteria

The project is successful when it:

- Produces identical hashes for unchanged content
- Produces different hashes after content modification
- Correctly reports added, modified, and deleted files
- Reports no alert when nothing changed
- Creates readable timestamped log records
- Passes all automated tests

## Future Enhancements

- Continuous monitoring with a file-system watcher
- Digitally signed or access-controlled baselines
- Email or desktop notifications
- Scheduled scans
- Web dashboard and charts
- Configurable exclusions
- Exportable security reports
