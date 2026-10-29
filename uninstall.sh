#!/bin/sh
# Remove asci from Linux / macOS:  sudo ./uninstall.sh
set -e
BIN="${PREFIX:-/usr/local}/bin"
rm -f "$BIN/asci" "$BIN/asi"
echo "asci removed from $BIN"
