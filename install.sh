#!/usr/bin/env bash

set -e

echo "♟️ Chess App kurulumu başlıyor..."

# 1️⃣ Arch kontrolü
if ! command -v pacman &> /dev/null; then
  echo "❌ Bu script yalnızca Arch Linux içindir."
  exit 1
fi

# 2️⃣ Zorunlu sistem paketleri
echo "📦 Zorunlu sistem paketleri yükleniyor..."

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
    echo "   Lütfen manuel kur:"
    echo "   sudo pacman -S --needed base-devel git"
    echo "   git clone https://aur.archlinux.org/yay.git"
    echo "   cd yay && makepkg -si"
    echo ""
    echo "   sonra:"
    echo "   yay -S stockfish"
    echo ""
    echo "   Oyun motorsuz çalışacaktır."
  fi
else
  echo "✅ Stockfish zaten kurulu."
fi

# 4️⃣ pipx PATH
echo "🔧 pipx PATH ayarlanıyor..."
pipx ensurepath

# 5️⃣ Eski chess binary temizle
BIN="$HOME/.local/bin/chess"
if [ -f "$BIN" ]; then
  echo "🧹 Eski chess binary siliniyor: $BIN"
  rm -f "$BIN"
fi

# 6️⃣ Uygulamayı pipx ile kur
echo "🐍 Chess App pipx ile kuruluyor..."
pipx install -e .

# 7️⃣ Shell cache temizle
hash -r || true

# 8️⃣ Son kontrol
echo ""
if command -v chess &> /dev/null; then
  echo "✅ Kurulum başarılı!"
  echo "▶️ Başlatmak için:"
  echo "   chess"
else
  echo "⚠️ Kurulum tamamlandı ama 'chess' komutu bulunamadı."
  echo "Yeni bir terminal açıp tekrar deneyin."
fi
