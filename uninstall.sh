#!/usr/bin/env bash
# Removes what install.sh added: the Nautilus extension file.
set -euo pipefail

DEST="$HOME/.local/share/nautilus-python/extensions/open-terminal-here.py"

if [[ -f $DEST ]]; then
  rm -f "$DEST"
  echo "removed: $DEST"
else
  echo "nothing to remove: $DEST not found"
fi

env -u PYTHONPATH -u PYTHONHOME PATH=/usr/local/sbin:/usr/local/bin:/usr/bin:/home/"$USER"/.local/bin nautilus -q 2>/dev/null || true
echo "Nautilus will reload without 'Open Terminal Here' on next open."
