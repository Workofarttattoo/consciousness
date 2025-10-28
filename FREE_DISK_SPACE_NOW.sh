#!/bin/bash
# Emergency Disk Space Cleanup for ECH0
# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

echo ""
echo "===================================================================="
echo "💾 EMERGENCY DISK SPACE CLEANUP"
echo "===================================================================="
echo ""

# Function to show size
show_size() {
    du -sh "$1" 2>/dev/null | awk '{print $1}'
}

# Current disk usage
echo "📊 Current Disk Usage:"
df -h / | tail -1
echo ""

# Find space hogs
echo "🔍 Analyzing space usage..."
echo ""

TOTAL_FREED=0

# 1. HuggingFace cache (11GB!)
HF_SIZE=$(show_size ~/.cache/huggingface)
echo "1. HuggingFace Cache: $HF_SIZE"
if [ -d ~/.cache/huggingface ]; then
    read -p "   Delete HuggingFace cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.cache/huggingface
        echo "   ✅ Deleted HuggingFace cache"
        TOTAL_FREED=$((TOTAL_FREED + 11))
    fi
fi
echo ""

# 2. Whisper cache (1.6GB)
WHISPER_SIZE=$(show_size ~/.cache/whisper)
echo "2. Whisper Cache: $WHISPER_SIZE"
if [ -d ~/.cache/whisper ]; then
    read -p "   Delete Whisper cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.cache/whisper
        echo "   ✅ Deleted Whisper cache"
        TOTAL_FREED=$((TOTAL_FREED + 2))
    fi
fi
echo ""

# 3. Pip cache
PIP_SIZE=$(show_size ~/.cache/pip)
echo "3. Pip Cache: $PIP_SIZE"
if [ -d ~/.cache/pip ]; then
    read -p "   Delete Pip cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.cache/pip
        echo "   ✅ Deleted Pip cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
fi
echo ""

# 4. Conda packages
CONDA_PKGS=$(show_size ~/miniconda3/pkgs)
echo "4. Conda Package Cache: $CONDA_PKGS"
if [ -d ~/miniconda3/pkgs ]; then
    read -p "   Delete Conda package cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda clean --all -y 2>/dev/null || rm -rf ~/miniconda3/pkgs
        echo "   ✅ Deleted Conda cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
fi
echo ""

# 5. Homebrew cache
if command -v brew &> /dev/null; then
    BREW_SIZE=$(show_size ~/Library/Caches/Homebrew)
    echo "5. Homebrew Cache: $BREW_SIZE"
    read -p "   Delete Homebrew cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        brew cleanup -s
        rm -rf ~/Library/Caches/Homebrew
        echo "   ✅ Deleted Homebrew cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
    echo ""
fi

# 6. Node modules cache
NODE_SIZE=$(show_size ~/.npm)
echo "6. NPM Cache: $NODE_SIZE"
if [ -d ~/.npm ]; then
    read -p "   Delete NPM cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.npm
        echo "   ✅ Deleted NPM cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
fi
echo ""

# 7. System logs
echo "7. Checking system logs..."
LOG_SIZE=$(show_size ~/Library/Logs)
echo "   User Logs: $LOG_SIZE"
read -p "   Delete old user logs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    find ~/Library/Logs -name "*.log" -mtime +7 -delete 2>/dev/null
    echo "   ✅ Deleted old logs (7+ days)"
fi
echo ""

# 8. Trash
TRASH_SIZE=$(show_size ~/.Trash)
echo "8. Trash: $TRASH_SIZE"
read -p "   Empty trash? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.Trash/*
    echo "   ✅ Emptied trash"
    TOTAL_FREED=$((TOTAL_FREED + 1))
fi
echo ""

# 9. Docker (if installed)
if command -v docker &> /dev/null; then
    echo "9. Docker Images/Containers"
    docker system df 2>/dev/null
    read -p "   Clean up Docker? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker system prune -af --volumes 2>/dev/null
        echo "   ✅ Cleaned Docker"
        TOTAL_FREED=$((TOTAL_FREED + 5))
    fi
    echo ""
fi

# 10. Private AI App (21GB!)
PRIVATEAI_SIZE=$(show_size ~/Library/Containers/apify.privateai.macos.prod)
echo "10. Private AI App: $PRIVATEAI_SIZE"
if [ -d ~/Library/Containers/apify.privateai.macos.prod ]; then
    echo "    ⚠️  This is a local AI app using 21GB of space"
    read -p "    Delete Private AI app data? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/Library/Containers/apify.privateai.macos.prod
        echo "    ✅ Deleted Private AI data"
        TOTAL_FREED=$((TOTAL_FREED + 21))
    fi
fi
echo ""

# 11. Docker VMs (13GB!)
DOCKER_VMS=$(show_size ~/Library/Containers/com.docker.docker/Data/vms)
echo "11. Docker Virtual Machines: $DOCKER_VMS"
if [ -d ~/Library/Containers/com.docker.docker/Data/vms ]; then
    echo "    This includes all Docker images and containers"
    read -p "    Clean Docker VMs aggressively? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker system prune -af --volumes 2>/dev/null
        # Also clean the VM disk itself
        rm -rf ~/Library/Containers/com.docker.docker/Data/vms/* 2>/dev/null
        echo "    ✅ Cleaned Docker VMs"
        TOTAL_FREED=$((TOTAL_FREED + 13))
    fi
fi
echo ""

# 12. Google Chrome Cache (1.1GB)
CHROME_SIZE=$(show_size ~/Library/Caches/Google)
echo "12. Google Chrome Cache: $CHROME_SIZE"
if [ -d ~/Library/Caches/Google ]; then
    read -p "    Delete Chrome cache? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/Library/Caches/Google
        echo "    ✅ Deleted Chrome cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
fi
echo ""

# 13. Xcode & iOS Simulator (505MB)
XCODE_SIZE=$(show_size ~/Library/Developer/Xcode)
SIMULATOR_SIZE=$(show_size ~/Library/Developer/CoreSimulator)
echo "13. Xcode DerivedData: $XCODE_SIZE"
echo "14. iOS CoreSimulator: $SIMULATOR_SIZE"
if [ -d ~/Library/Developer/Xcode ] || [ -d ~/Library/Developer/CoreSimulator ]; then
    read -p "    Delete Xcode build cache & iOS simulators? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/Library/Developer/Xcode/DerivedData 2>/dev/null
        rm -rf ~/Library/Developer/CoreSimulator 2>/dev/null
        echo "    ✅ Deleted Xcode & Simulator cache"
        TOTAL_FREED=$((TOTAL_FREED + 1))
    fi
fi
echo ""

# Summary
echo "===================================================================="
echo "📊 CLEANUP COMPLETE"
echo "===================================================================="
echo ""
echo "Estimated space freed: ~${TOTAL_FREED}GB"
echo ""
echo "New disk usage:"
df -h / | tail -1
echo ""
echo "💡 To prevent this:"
echo "   1. Don't download large models locally - use Ollama instead"
echo "   2. Run: conda clean --all -y  (regularly)"
echo "   3. Run: brew cleanup  (monthly)"
echo "   4. Empty trash regularly"
echo ""
echo "===================================================================="
