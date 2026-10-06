import os
import shutil

from gi import require_version

require_version("Nautilus", "4.1")

from gi.repository import GObject, Gio, Nautilus


class OpenTerminalHere(GObject.GObject, Nautilus.MenuProvider):
    """Right-click 'Open Terminal Here' respecting `omarchy default terminal`.

    Uses xdg-terminal-exec so it follows ~/.config/xdg-terminals.list,
    which is what `omarchy default terminal <name>` writes.
    Launch via uwsm-app when available (Omarchy/Hyprland scope pattern).
    """

    def _build_commands(self, target_dir):
        xdg_term = shutil.which("xdg-terminal-exec")
        uwsm_app = shutil.which("uwsm-app")
        setsid = shutil.which("setsid")

        cmds = []
        if xdg_term:
            base = [xdg_term, f"--dir={target_dir}"]
            if uwsm_app and setsid:
                cmds.append([setsid, uwsm_app, "--"] + base)
            if uwsm_app:
                cmds.append([uwsm_app, "--"] + base)
            cmds.append(list(base))

        # Fallbacks if xdg-terminal-exec is missing: try Omarchy terminals directly.
        fallbacks = [
            ("alacritty", ["--working-directory", target_dir]),
            ("kitty", ["--directory", target_dir]),
            ("ghostty", ["--working-directory", target_dir]),
            ("foot", ["--working-directory", target_dir]),
        ]
        for binary, args in fallbacks:
            path = shutil.which(binary)
            if path:
                cmd = [path] + args
                if uwsm_app and setsid:
                    cmds.append([setsid, uwsm_app, "--"] + cmd)
                cmds.append(list(cmd))
                break

        return cmds

    def _launch_in_dir(self, target_dir):
        if not target_dir or not os.path.isdir(target_dir):
            return
        for cmd in self._build_commands(target_dir):
            try:
                Gio.Subprocess.new(cmd, Gio.SubprocessFlags.NONE)
                return
            except Exception:
                continue

    def _dir_for_file(self, file):
        if file.get_uri_scheme() != "file":
            return None
        location = file.get_location()
        if not location:
            return None
        path = location.get_path()
        if not path:
            return None
        # If a file (not dir) is right-clicked, open its parent.
        if os.path.isfile(path):
            return os.path.dirname(path)
        if os.path.isdir(path):
            return path
        return None

    def _make_item(self, target_dir, name_suffix):
        item = Nautilus.MenuItem(
            name=f"OpenTerminalHere::{name_suffix}",
            label="Open Terminal Here",
            icon="utilities-terminal",
        )
        item.connect("activate", lambda menu, d=target_dir: self._launch_in_dir(d))
        return item

    def get_file_items(self, *args):
        files = args[0] if len(args) == 1 else args[1]
        if len(files) != 1:
            return []
        target = self._dir_for_file(files[0])
        if not target:
            return []
        return [self._make_item(target, "file")]

    def get_background_items(self, *args):
        folder = args[0] if len(args) == 1 else args[1]
        target = self._dir_for_file(folder)
        if not target:
            return []
        return [self._make_item(target, "background")]
