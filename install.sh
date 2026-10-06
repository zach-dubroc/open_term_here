#!/usr/bin/env bash
# Installer for the Nautilus "Open Terminal Here" extension.
# Copies the extension into ~/.local/share/nautilus-python/extensions/
# and asks Nautilus to reload so the context menu appears.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/extensions/open-terminal-here.py"
DEST_DIR="$HOME/.local/share/nautilus-python/extensions"
DEST="$DEST_DIR/open-terminal-here.py"

if ! command -v nautilus >/dev/null; then
  echo "error: nautilus is not installed" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp -f "$SRC" "$DEST"
echo "installed: $DEST"

# Quit Nautilus so it reloads extensions on next open.
# Run with a clean PATH so nautilus-python finds system gi, not mise shims.
if env -u PYTHONPATH -u PYTHONHOME PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/home/"$USER"/.local/bin nautilus -q 2>/dev/null; then
  echo "Nautilus quit — reopen Files and right-click to see 'Open Terminal Here'."
else
  echo "Installed. Reopen Files and right-click to see 'Open Terminal Here'."
fi
echo "Terminal used: whatever 'omarchy default terminal' reports (xdg-terminal-exec)."
