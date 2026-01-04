#!/usr/bin/env bash

set -e

echo "🗑️ Chess App kaldırılıyor..."

# 1️⃣ pipx ile kurulmuşsa kaldır
if command -v pipx &> /dev/null; then
  pipx uninstall chess || true
fi

# 2️⃣ Kullanıcı PATH'inde kalan chess binary'sini sil
BIN="$HOME/.local/bin/chess"

if [ -f "$BIN" ]; then
  echo "🧹 Kalan binary siliniyor: $BIN"
  rm -f "$BIN"
fi

# 3️⃣ Config dizini sil
CONFIG_DIR="$HOME/.config/chess-app"

if [ -d "$CONFIG_DIR" ]; then
  echo "⚙️ Config dizini siliniyor: $CONFIG_DIR"
  rm -rf "$CONFIG_DIR"
fi

# 4️⃣ Shell cache temizle
hash -r || true

echo "✅ Chess App tamamen kaldırıldı."
echo "ℹ️  Yeni bir terminal açarsan değişiklikler kesinleşir."
