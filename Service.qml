import QtQuick

// Service entry point required by the Omarchy shell plugin contract.
// The real payload of this plugin lives outside the shell: a Nautilus
// Python extension installed by install.sh. This service is intentionally
// a no-op so the plugin validates, loads, and enables cleanly without
// adding bar UI.
Item {
  id: root

  // Injected by omarchy-shell for first- and third-party services.
  property var shell: null
  property var manifest: null
  property var pluginRegistry: null
}
