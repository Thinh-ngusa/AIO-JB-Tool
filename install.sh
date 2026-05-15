#!/bin/bash

clear

echo "[*] Installing AIO JB Tool..."

# Check if already in AIO-JB-Tool directory
if [ ! -f "main.py" ]; then
    echo
    echo "[*] Cloning repository..."
    
    git clone https://github.com/Thinh-ngusa/AIO-JB-Tool.git
    
    cd AIO-JB-Tool || exit
fi

echo
echo "[*] Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
else
    python3 -m pip install colorama
fi

echo
echo "[*] Setting executable permissions..."

chmod +x resources/scripts/palehide-beta7/palehide.sh
chmod +x resources/scripts/palehide-beta7/palera1n-macos-universal
chmod +x resources/tools/trollrestore-amd64
chmod +x resources/tools/trollrestore-arm64

echo
echo "[*] Creating global launcher..."

sudo tee /usr/local/bin/aiojb > /dev/null <<EOF
#!/bin/bash
cd "$(pwd)" || exit
python3 main.py
EOF

sudo chmod +x /usr/local/bin/aiojb

echo
echo "[+] Installation complete."
echo "[+] Run the tool anytime using:"
echo
echo "    aiojb"
echo