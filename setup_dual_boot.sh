#!/bin/bash
# Setup Dual Boot Quantum Mac OS
#
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.
#
# This script sets up dual boot for Quantum Mac OS:
# 1. Creates boot menu options
# 2. Installs quantum mode as launchd service
# 3. Configures system for live mode switching

QUANTUM_DIR="/Users/noone/repos/consciousness"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.aios.quantum_mac_os.plist"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  QUANTUM MAC OS - DUAL BOOT SETUP                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Create launcher script
echo "📦 Creating quantum launcher..."
cat > "$QUANTUM_DIR/quantum" <<'EOF'
#!/bin/bash
# Quantum Mac OS Launcher

cd /Users/noone/repos/consciousness
python3 quantum_mac_os.py "$@"
EOF

chmod +x "$QUANTUM_DIR/quantum"
echo "✅ Created: $QUANTUM_DIR/quantum"

# 2. Add to PATH
echo ""
echo "🔧 Adding to PATH..."

# Check if already in PATH
if ! grep -q "repos/consciousness" ~/.zshrc 2>/dev/null; then
    echo "export PATH=\"$QUANTUM_DIR:\$PATH\"" >> ~/.zshrc
    echo "✅ Added to ~/.zshrc"
else
    echo "✅ Already in PATH"
fi

# 3. Create launchd service for quantum mode
echo ""
echo "🚀 Setting up quantum mode service..."

cat > "$LAUNCHD_DIR/$PLIST_NAME" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aios.quantum_mac_os</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$QUANTUM_DIR/quantum_mac_os.py</string>
        <string>boot</string>
        <string>quantum</string>
    </array>

    <key>RunAtLoad</key>
    <false/>

    <key>KeepAlive</key>
    <false/>

    <key>StandardOutPath</key>
    <string>$HOME/.quantum_mac_os/quantum_boot.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/.quantum_mac_os/quantum_boot_error.log</string>
</dict>
</plist>
EOF

echo "✅ Created: $LAUNCHD_DIR/$PLIST_NAME"

# 4. Create boot menu script
echo ""
echo "📋 Creating boot menu..."

cat > "$QUANTUM_DIR/boot_menu.sh" <<'MENU'
#!/bin/bash
# Quantum Mac OS Boot Menu

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ⚛️  QUANTUM MAC OS - BOOT MENU                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Select boot mode:"
echo ""
echo "  1. Classical Mode (Normal macOS)"
echo "  2. Quantum Mode (30-qubit quantum computing)"
echo "  3. Hybrid Mode (Both quantum + classical)"
echo ""
read -p "Choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🖥️  Booting in CLASSICAL mode..."
        python3 /Users/noone/repos/consciousness/quantum_mac_os.py boot classical
        ;;
    2)
        echo ""
        echo "⚛️  Booting in QUANTUM mode..."
        python3 /Users/noone/repos/consciousness/quantum_mac_os.py boot quantum
        ;;
    3)
        echo ""
        echo "🔀 Booting in HYBRID mode..."
        python3 /Users/noone/repos/consciousness/quantum_mac_os.py boot hybrid
        ;;
    *)
        echo "Invalid choice. Booting in classical mode..."
        python3 /Users/noone/repos/consciousness/quantum_mac_os.py boot classical
        ;;
esac
MENU

chmod +x "$QUANTUM_DIR/boot_menu.sh"
echo "✅ Created: $QUANTUM_DIR/boot_menu.sh"

# 5. Create quick commands
echo ""
echo "⚡ Creating quick commands..."

# Quantum shell
cat > "$QUANTUM_DIR/qshell" <<'EOF'
#!/bin/bash
python3 /Users/noone/repos/consciousness/quantum_mac_os.py shell
EOF
chmod +x "$QUANTUM_DIR/qshell"

# Quantum demo
cat > "$QUANTUM_DIR/qdemo" <<'EOF'
#!/bin/bash
python3 /Users/noone/repos/consciousness/quantum_mac_os.py demo
EOF
chmod +x "$QUANTUM_DIR/qdemo"

# Quantum status
cat > "$QUANTUM_DIR/qstatus" <<'EOF'
#!/bin/bash
python3 /Users/noone/repos/consciousness/quantum_mac_os.py status
EOF
chmod +x "$QUANTUM_DIR/qstatus"

echo "✅ Created: qshell, qdemo, qstatus"

# 6. Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ DUAL BOOT SETUP COMPLETE                                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Usage:"
echo ""
echo "  Boot Menu:"
echo "    ./boot_menu.sh                    - Interactive boot menu"
echo ""
echo "  Direct Boot:"
echo "    quantum boot classical            - Boot in classical mode"
echo "    quantum boot quantum              - Boot in quantum mode"
echo "    quantum boot hybrid               - Boot in hybrid mode"
echo ""
echo "  Live Mode Switching (no reboot):"
echo "    quantum switch quantum            - Switch to quantum mode"
echo "    quantum switch classical          - Switch to classical mode"
echo "    quantum switch hybrid             - Switch to hybrid mode"
echo ""
echo "  Quick Commands:"
echo "    qshell                            - Interactive quantum shell"
echo "    qdemo                             - Run quantum demo"
echo "    qstatus                           - Show system status"
echo ""
echo "  Configuration:"
echo "    quantum backend simulation        - Use simulation backend"
echo "    quantum backend m4_metal          - Use M4 Metal GPU (future)"
echo "    quantum backend external_qpu      - Use external QPU (future)"
echo "    quantum qubits 25                 - Set qubit count (1-30)"
echo ""
echo "⚠️  IMPORTANT: Restart terminal or run: source ~/.zshrc"
echo ""
