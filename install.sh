#!/bin/sh
# Install asci system-wide on Linux / macOS.
#
#   sudo ./install.sh
#   curl -fsSL https://raw.githubusercontent.com/wetpant000/asci/main/install.sh | sudo sh
#
# Installs the commands `asci` and `asi` into $PREFIX/bin (default /usr/local/bin).
set -e

PREFIX="${PREFIX:-/usr/local}"
BIN="$PREFIX/bin"
SRC_URL="https://raw.githubusercontent.com/wetpant000/asci/main/asci.py"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required. Install it first." >&2
    exit 1
fi

if ! mkdir -p "$BIN" 2>/dev/null || [ ! -w "$BIN" ]; then
    echo "Permission denied for $BIN. Run with sudo:  sudo sh install.sh" >&2
    exit 1
fi

DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"

if [ -f "$DIR/asci.py" ]; then
    cp "$DIR/asci.py" "$BIN/asci"
else
    # Piped from curl: download the script.
    curl -fsSL "$SRC_URL" -o "$BIN/asci"
fi

chmod 755 "$BIN/asci"
ln -sf "$BIN/asci" "$BIN/asi"

echo "asci installed to $BIN"
echo "Try:  asci cat   or   asi dog"
