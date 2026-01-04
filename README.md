# ♟️ Chess App: Profesyonel & Minimalist Satranç Platformu

Python tabanlı bu uygulama, hem oyuncular hem de satranç programlama ile ilgilenen geliştiriciler için tasarlanmış, Linux felsefesini benimseyen bir platformdur. Bünyesinde barındırdığı **Stockfish** motoru desteği ile en üst düzey analiz imkanı sunar.

## 📋 İçindekiler
1. [Öne Çıkan Özellikler](#-öne-çıkan-özellikler)
2. [Stockfish ve Yapay Zeka Analizi](#-stockfish-ve-yapay-zeka-analizi)
3. [Özel Başlangıç Konumları (FEN)](#-özel-başlangıç-konumları-fen)
4. [Klavye Kısayolları](#-klavye-kısayolları)
5. [Kurulum ve Dağıtım](#-kurulum-ve-dağıtım)
6. [Yapılandırma Rehberi (config.json)](#-yapılandırma-rehberi-configjson)
7. [Kaldırma Talimatları](#-kaldırma-talimatları)

---

## ✨ Öne Çıkan Özellikler

* **Stockfish Entegrasyonu:** Dünyanın en güçlü satranç motoru ile analiz ve oyun desteği.
* **FEN Şeması Desteği:** İstediğiniz herhangi bir pozisyondan oyuna başlama imkanı.
* **Evrensel Notasyon:** Algebraic, ICCF, Descriptive ve Coordinate sistemleri.
* **Linux Native:** Ayarlarınızı `~/.config/chess-app/` altında saklayan temiz yapı.

---

## 🤖 Stockfish ve Yapay Zeka Analizi

Uygulama, sisteminizde yüklü olan **Stockfish** motorunu otomatik olarak kullanabilir. Zorluk ve performans ayarlarını `~/.config/chess-app/config.json` dosyasından yönetebilirsiniz:

* **`stockfish_path`**: Bilgisayarınızdaki Stockfish dosyasının yolu (Genellikle `/usr/bin/stockfish`).
* **`stockfish_depth`**: Motorun ne kadar derin analiz yapacağını belirler (Zorluk seviyesi). 
  * *Hızlı/Kolay:* 1-5
  * *Orta:* 10-15
  * *Profesyonel:* 20+
* **`stockfish_time`**: Motorun hamle düşünmek için ayıracağı maksimum süre.

---

## 🧩 Özel Başlangıç Konumları (FEN)

Belirli bir satranç problemini çözmek veya ünlü bir maçın ortasından başlamak için `config.json` dosyasındaki `starting_fen` değerini değiştirmeniz yeterlidir.

**Örnek (Sadece Şahlar ve Piyonlar):**
`"starting_fen": "4k3/pppppppp/8/8/8/8/PPPPPPPP/4K3 w - - 0 1"`

---

## ⌨️ Klavye Kısayolları

Oyun sırasında aşağıdaki kısayolları kullanarak deneyiminizi hızlandırabilirsiniz:

| Tuş | İşlev |
| :--- | :--- |
| **R** | Tahtayı ve oyunu sıfırla (Reset). |
| **U** | Yapılan son hamleyi geri al (Undo). |
| **S** | Mevcut pozisyonu FEN formatında terminale yazdır. |
| **Q** | Oyundan çık. |
| **F** | Ekranı tam ekran (Fullscreen) moduna al. |

---

## 🛠️ Kurulum ve Dağıtım

### 1. Kütüphaneleri Kurun
\`\`\`bash
pip install pygame python-chess
\`\`\`

### 2. Sisteme Paket Olarak Tanımlayın
Terminale \`chess\` yazınca çalışması için:
\`\`\`bash
pip install -e .
\`\`\`

---

## ⚙️ Yapılandırma Rehberi (config.json)

Ayarlarınız `~/.config/chess-app/config.json` dosyasında şu şekilde görünür:

\`\`\`json
{
  "stockfish_depth": 15,
  "board_theme": "brown",
  "notation_scheme": "algebraic",
  "starting_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "play_sounds": true
}
\`\`\`

---

## 🗑️ Kaldırma Talimatları

1. **Paketi Kaldır:** \`pip uninstall chess-app\`
2. **Ayarları Sil:** \`rm -rf ~/.config/chess-app/\`
3. **Klasörü Sil:** \`rm -rf MyChess/\`

---
**Geliştirici:** [ibotimew](https://github.com/ibotimew) | **Sürüm:** 1.0.0
