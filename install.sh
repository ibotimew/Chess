#!/usr/bin/env bash

set -e

echo "♟️ Chess App kurulumu başlıyor..."

# 1️⃣ Arch Linux kontrolü
if ! command -v pacman &> /dev/null; then
  echo "❌ Bu script yalnızca Arch Linux içindir."
  exit 1
fi

# 2️⃣ Gerekli sistem paketleri
echo "📦 Sistem paketleri yükleniyor / kontrol ediliyor..."

sudo pacman -S --needed --noconfirm \
  python \
  python-pipx \
  stockfish \
  sdl2 \
  sdl2_image \
  sdl2_mixer \
  sdl2_ttf

# 3️⃣ pipx PATH ayarla
echo "🔧 pipx PATH ayarlanıyor..."
pipx ensurepath

# 4️⃣ Eski chess binary kalıntısı varsa temizle
BIN="$HOME/.local/bin/chess"
if [ -f "$BIN" ]; then
  echo "🧹 Eski chess binary temizleniyor: $BIN"
  rm -f "$BIN"
fi

# 5️⃣ pipx ile uygulamayı kur
echo "🐍 Chess App pipx ile kuruluyor..."
pipx install -e .

# 6️⃣ Shell cache temizle
hash -r || true

# 7️⃣ Komut kontrolü
if command -v chess &> /dev/null; then
  echo ""
  echo "✅ Kurulum başarılı!"
  echo "▶️ Oyunu başlatmak için:"
  echo "   chess"
else
  echo ""
  echo "⚠️ Kurulum yapıldı ama 'chess' komutu bulunamadı."
  echo "Yeni bir terminal açıp tekrar deneyin."
fi
