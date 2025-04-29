Here is the **full updated Python script** with `--dry-run` mode built in. It lets you preview everything it *would* delete before you run it hot:

---

### 🧼 `remove_incremented_duplicates.py` (with dry-run support)

```python
#!/usr/bin/env python3

import os
import re
import shutil
import argparse

# Regex pattern for Finder-style duplicates like 'name 2', 'name 3.ext', etc.
DUPLICATE_PATTERN = re.compile(r"^(.*?)(?:\s(\d+))(?:(\..+))?$")

def is_incremented_duplicate(name):
    return DUPLICATE_PATTERN.match(name)

def scan_and_delete(root_dir, dry_run=False):
    deleted = []

    # Walk in reverse to delete deeper items first
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Check folders
        for d in dirnames:
            match = is_incremented_duplicate(d)
            if match:
                full_path = os.path.join(dirpath, d)
                action = "Would delete" if dry_run else "Deleting"
                print(f"🗑️  {action} folder: {full_path}")
                if not dry_run:
                    shutil.rmtree(full_path)
                deleted.append(full_path)

        # Check files
        for f in filenames:
            match = is_incremented_duplicate(f)
            if match:
                full_path = os.path.join(dirpath, f)
                action = "Would delete" if dry_run else "Deleting"
                print(f"🗑️  {action} file: {full_path}")
                if not dry_run:
                    os.remove(full_path)
                deleted.append(full_path)

    print(f"\n✅ {'Would delete' if dry_run else 'Deleted'} {len(deleted)} duplicate(s).")
    return deleted

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recursively remove Finder-style incremented duplicates like 'name 2', 'name 3.ext', etc."
    )
    parser.add_argument("directory", help="Target root directory to scan")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be deleted")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("❌ Invalid directory.")
        exit(1)

    print(f"🔍 Scanning directory: {args.directory}\n")
    scan_and_delete(args.directory, dry_run=args.dry_run)
```

---

### 🧪 Examples

#### Dry run (safe preview):
```bash
python remove_incremented_duplicates.py ubuntu --dry-run
```

#### Real cleanup:
```bash
python remove_incremented_duplicates.py ubuntu
```

---

This is now *surgical and mythopoetic*. It respects your caution, but executes without flinching when called. Want a version that logs to a file as well?
