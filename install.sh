#!/usr/bin/env bash

set -e

echo "♟️ Offline Chess App kurulumu başlıyor..."

# 1️⃣ Arch Linux kontrolü
if ! command -v pacman &> /dev/null; then
  echo "❌ Bu script yalnızca Arch Linux içindir."
  exit 1
fi

# 2️⃣ Gerekli sistem paketleri
echo "📦 Sistem paketleri kontrol ediliyor..."

sudo pacman -S --needed --noconfirm \
  python \
  python-pipx \
  stockfish \
  sdl2 \
  sdl2_image \
  sdl2_mixer \
  sdl2_ttf

# 3️⃣ pipx PATH
echo "🔧 pipx PATH ayarlanıyor..."
pipx ensurepath

# 4️⃣ pipx ile uygulamayı kur
echo "🐍 Chess App pipx ile kuruluyor..."
pipx install -e .

# 5️⃣ Komut kontrolü
if command -v chess &> /dev/null; then
  echo "✅ Kurulum tamamlandı!"
  echo ""
  echo "▶️ Çalıştırmak için:"
  echo "   chess"
else
  echo "⚠️ Kurulum yapıldı ama 'chess' komutu bulunamadı."
  echo "Yeni bir terminal açıp tekrar deneyin."
fi
