#!/usr/bin/env bash

set -e

echo "🗑️ Chess App kaldırılıyor..."

# pipx ile kurulmuşsa kaldır
if command -v pipx &> /dev/null; then
  pipx uninstall chess || true
fi

# config dizini
CONFIG_DIR="$HOME/.config/chess-app"

if [ -d "$CONFIG_DIR" ]; then
  echo "⚙️ Config dizini siliniyor: $CONFIG_DIR"
  rm -rf "$CONFIG_DIR"
fi

echo "✅ Chess App tamamen kaldırıldı."
