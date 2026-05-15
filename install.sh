#!/bin/bash

clear

echo "[*] Installing AIO JB Tool..."

# Add Homebrew paths early
if [[ "$(uname -m)" == "arm64" ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
else
    export PATH="/usr/local/bin:$PATH"
fi

# Clone repo if not already inside project
if [ ! -f "main.py" ]; then
    echo
    echo "[*] Cloning repository..."

    git clone https://github.com/Thinh-ngusa/AIO-JB-Tool.git
    cd AIO-JB-Tool || exit 1
fi

INSTALL_DIR="$(pwd)"

echo
echo "[*] Checking Homebrew..."

if ! command -v brew &> /dev/null; then
    echo "[!] Homebrew not found. Installing Homebrew..."

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if [[ "$(uname -m)" == "arm64" ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> "$HOME/.zshrc"
    else
        export PATH="/usr/local/bin:$PATH"
        echo 'export PATH="/usr/local/bin:$PATH"' >> "$HOME/.zshrc"
    fi

    if ! command -v brew &> /dev/null; then
        echo "[!] Failed to install Homebrew."
        echo "[*] Please install manually: https://brew.sh"
        exit 1
    fi

    echo "[+] Homebrew installed successfully."
else
    echo "[+] Homebrew found at: $(command -v brew)"
fi

echo
echo "[*] Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt || python3 -m pip install --user -r requirements.txt
else
    python3 -m pip install colorama || python3 -m pip install --user colorama
fi

echo
echo "[*] Checking system dependencies..."

echo "[*] Installing libimobiledevice..."
brew install libimobiledevice || true

echo "[*] Installing ideviceinstaller..."

if ! command -v ideviceinstaller &> /dev/null; then
    brew install --HEAD ideviceinstaller || {
        echo "[!] brew install --HEAD ideviceinstaller failed."
        echo "[*] Trying libimobiledevice tap..."

        brew tap libimobiledevice/homebrew-libimobiledevice || true
        brew install ideviceinstaller || true
    }
fi

if command -v ideviceinstaller &> /dev/null; then
    echo "[+] ideviceinstaller found at: $(command -v ideviceinstaller)"
else
    echo "[!] ideviceinstaller is still not available."
    echo "[*] Try manually:"
    echo "    brew install --HEAD ideviceinstaller"
fi

echo
echo "[*] Checking useful tools..."

for tool in idevice_id ideviceinfo idevicepair; do
    if command -v "$tool" &> /dev/null; then
        echo "[+] $tool found"
    else
        echo "[!] $tool not found"
    fi
done

echo
echo "[*] Setting executable permissions..."

chmod +x resources/scripts/palehide-beta7/palehide.sh 2>/dev/null || true
chmod +x resources/scripts/palehide-beta7/palera1n-macos-universal 2>/dev/null || true
chmod +x resources/tools/trollrestore-amd64 2>/dev/null || true
chmod +x resources/tools/trollrestore-arm64 2>/dev/null || true

echo
echo "[*] Creating global launcher..."

sudo tee /usr/local/bin/aiojb > /dev/null <<EOF
#!/bin/bash
cd "$INSTALL_DIR" || exit 1
python3 main.py
EOF

sudo chmod +x /usr/local/bin/aiojb

echo
echo "[+] Installation complete."
echo "[+] Run the tool anytime using:"
echo
echo "    aiojb"
echo