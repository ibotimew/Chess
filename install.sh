#!/usr/bin/env bash

set -e

echo "♟️ Chess App kurulumu başlıyor..."

# 1️⃣ Arch kontrolü
if ! command -v pacman &> /dev/null; then
  echo "❌ Bu script yalnızca Arch Linux içindir."
  exit 1
fi

# 2️⃣ Zorunlu sistem paketleri
echo "📦 Zorunlu sistem paketleri yükleniyor / kontrol ediliyor..."

sudo pacman -S --needed --noconfirm \
  python \
  python-pipx \
  sdl2 \
  sdl2_image \
  sdl2_mixer \
  sdl2_ttf

# 3️⃣ Stockfish (yay üzerinden)
echo "🤖 Stockfish kontrol ediliyor..."

if ! command -v stockfish &> /dev/null; then
  if command -v yay &> /dev/null; then
    echo "⬇️ Stockfish yay ile kuruluyor..."
    yay -S --needed --noconfirm stockfish
  else
    echo "⚠️  Stockfish bulunamadı ve yay yüklü değil."
    echo "   Oyun motorsuz çalışacaktır."
    echo "   Manuel kurulum:"
    echo "   yay -S stockfish"
  fi
else
  echo "✅ Stockfish zaten kurulu."
fi

# 4️⃣ pipx PATH
echo "🔧 pipx PATH ayarlanıyor..."
pipx ensurepath

# 5️⃣ Eski chess binary kalıntısı temizle
BIN="$HOME/.local/bin/chess"
if [ -f "$BIN" ]; then
  echo "🧹 Eski chess binary siliniyor: $BIN"
  rm -f "$BIN"
fi

# 6️⃣ pipx ile kur / güncelle (KRİTİK KISIM)
echo "🐍 Chess App pipx ile kuruluyor / güncelleniyor..."

if pipx list | grep -q chess-app; then
  pipx reinstall chess-app
else
  pipx install -e .
fi

# 7️⃣ Shell cache temizle
hash -r || true

# 8️⃣ Son kontrol
echo ""
if command -v chess &> /dev/null; then
  echo "✅ Kurulum başarılı!"
  echo "▶️ Oyunu başlatmak için:"
  echo "   chess"
else
  echo "❌ HATA: 'chess' komutu bulunamadı."
  echo "Yeni bir terminal açıp tekrar deneyin."
fi
