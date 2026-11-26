#!/usr/bin/env python3
"""Write the One-Liner Laughs entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only. Deterministic: writes exactly one line, no trailing newline,
UTF-8. Exits non-zero if the entry exceeds 200 characters.
"""

import os
import sys

ENTRY = (
    "My smartwatch congratulated me on 10,000 steps. "
    "I was stuck in traffic, drumming the steering wheel."
)


def main() -> int:
    if len(ENTRY) > 200:
        print(f"entry too long: {len(ENTRY)} chars (max 200)", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in ENTRY):
        print("entry contains a control character", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back and verify the bytes on disk match the entry exactly.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != ENTRY.encode("utf-8"):
        print("verification failed: entry.txt does not match ENTRY", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
