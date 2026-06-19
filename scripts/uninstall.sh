#!/usr/bin/env bash

# ==========================================================
# OpenShell Public Uninstaller
# ==========================================================

set -e


APP_NAME="OpenShell Public"


echo ""
echo "=============================================="
echo " Uninstalling: $APP_NAME"
echo "=============================================="
echo ""


# ----------------------------------------------------------
# Check root directory
# ----------------------------------------------------------

if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found"
    echo "Run this script from repository root"
    exit 1
fi



# ----------------------------------------------------------
# Python dependencies
# ----------------------------------------------------------

echo "[*] Removing Python dependencies..."

pip3 uninstall \
    -r requirements.txt \
    -y \
    --break-system-packages \
    || true


echo "[+] Python dependencies removed"



# ----------------------------------------------------------
# Remove PYTHONPATH injection
# ----------------------------------------------------------

echo "[*] Cleaning PYTHONPATH configuration..."


BASHRC="$HOME/.bashrc"


if [ -f "$BASHRC" ]; then

    grep -v \
    'OpenShell Public' \
    "$BASHRC" > "$BASHRC.tmp" \
    || true


    grep -v \
    'PYTHONPATH=' \
    "$BASHRC.tmp" > "$BASHRC"


    rm -f "$BASHRC.tmp"

fi


echo "[+] Environment cleaned"



# ----------------------------------------------------------
# Remove Python cache
# ----------------------------------------------------------

echo "[*] Removing Python cache files..."


find . \
    -type d \
    -name "__pycache__" \
    -exec rm -rf {} + \
    2>/dev/null || true


find . \
    -name "*.pyc" \
    -delete \
    2>/dev/null || true


echo "[+] Python cache removed"



# ----------------------------------------------------------
# Persistent data
# ----------------------------------------------------------

echo ""

read -p \
"Remove OpenShell local data (storage/logs)? [y/N]: " REMOVE_DATA


if [[ "$REMOVE_DATA" =~ ^[Yy]$ ]]; then


    echo "[*] Removing local storage..."


    rm -rf \
        console/storage \
        console/logs


    echo "[+] Local data removed"

else

    echo "[!] Storage and logs preserved"

fi



# ----------------------------------------------------------
# Finish
# ----------------------------------------------------------

echo ""

echo "=============================================="
echo " OpenShell Public uninstalled"
echo "=============================================="

echo ""

echo "Restart your shell to reload environment:"
echo ""
echo "    source ~/.bashrc"
echo ""

exit 0