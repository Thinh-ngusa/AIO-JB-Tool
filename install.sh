#!/bin/bash

clear

echo
echo "AIO JB Tool Installer"
echo "---------------------"

REPO_URL="https://github.com/Thinh-ngusa/AIO-JB-Tool.git"
PROJECT_DIR="$HOME/AIO-JB-Tool"

if ! command -v brew >/dev/null 2>&1; then
    echo
    echo "[!] Homebrew is not installed."
    echo "[*] Installing Homebrew..."

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if ! command -v brew >/dev/null 2>&1; then
        echo
        echo "[!] Failed to install Homebrew."
        exit 1
    fi
fi

echo
echo "[*] Installing dependencies..."

brew install python
brew install libimobiledevice
brew install usbmuxd
brew install libirecovery

echo
echo "[*] Restarting usbmuxd..."

brew services restart usbmuxd

echo
echo "[*] Installing Python packages..."

python3 -m pip install --upgrade pip
python3 -m pip install colorama

echo
echo "[*] Preparing project folder..."

if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR" || exit 1
    git pull
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR" || exit 1
fi

echo
echo "[*] Setting executable permissions..."

chmod +x resources/scripts/palehide-beta7/palehide.sh 2>/dev/null
chmod +x resources/scripts/palehide-beta7/palera1n-macos-universal 2>/dev/null

echo
echo "[*] Creating aiojb launcher..."

sudo tee /usr/local/bin/aiojb >/dev/null <<EOF
#!/bin/bash
cd "$PROJECT_DIR" || exit
python3 main.py
EOF

sudo chmod +x /usr/local/bin/aiojb

echo
echo "[+] Installation completed."
echo
echo "Run the tool using:"
echo
echo "aiojb"
echo