# ♟️ Offline Chess App (Lichess‑Benzeri, Stockfish Destekli)

Bu proje **tamamen offline** çalışan, **Python + Pygame** tabanlı, sade ve performans odaklı bir satranç uygulamasıdır. Arayüz felsefesi olarak **Lichess**’in minimal yaklaşımını benimser: ekranda yalnızca **tahta ve taşlar** bulunur, menü veya buton yoktur.

Uygulama hamle üretimi ve rakip için **Stockfish (UCI)** motorunu kullanır. Tüm ayarlar Linux standartlarına uygun şekilde **`~/.config/chess-app/config.json`** dosyasından yapılır.

---

## ✨ Özellikler

* 📴 **%100 offline** çalışma
* ♜ **Stockfish** motoru ile oynama
* 🎨 Lichess tarzı **tahta & taş temaları**
* 🖱️ **Sürükle‑bırak** ve **tıkla‑tıkla** hamle sistemi
* 🔄 **Undo** (animasyonlu, oyuncu + motor)
* 🔁 **Tahta çevirme / taraf değiştirme**
* ✍️ **Ok çizme & kare işaretleme** (analiz için)
* 🔔 Hamle, yeme, şah, mat vb. **ses efektleri**
* ✍️ **Çoklu notasyon** (Algebraic, ICCF, Coordinate, Descriptive, FEN)
* 🧩 **FEN** ile başlangıç pozisyonu

---

## 🤖 Satranç Motoru (Stockfish)

Uygulama gömülü motor içermez. Sisteminizde kurulu olan **Stockfish** motorunu **UCI protokolü** ile çalıştırır.

### İlgili Ayarlar (`config.json`)

| Ayar              | Açıklama                                               |
| ----------------- | ------------------------------------------------------ |
| `stockfish_path`  | Stockfish ikili dosya yolu (örn. `/usr/bin/stockfish`) |
| `stockfish_depth` | Arama derinliği (zorluk)                               |
| `stockfish_time`  | Hamle başına maksimum süre (sn)                        |

**Zorluk önerisi:** Kolay `1–3`, Orta `6–10`, Güçlü `12+`

---

## ⚙️ Yapılandırma (config.json)

Uygulama ilk çalıştırmada otomatik olarak aşağıdaki dizini oluşturur:

```text
~/.config/chess-app/
```

### Örnek `config.json`

```json
{
  "animation_speed": 0.2,
  "stockfish_path": "/usr/bin/stockfish",
  "stockfish_depth": 1,
  "stockfish_time": 0.001,
  "board_theme": "brown",
  "piece_theme": "cburnett",
  "notation_scheme": "algebraic",
  "starting_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "play_sounds": true
}
```

---

## ✍️ Notasyon Desteği

| Tür           | Açıklama     | Örnek               |
| ------------- | ------------ | ------------------- |
| `algebraic`   | Standart SAN | `Nf3`, `exd5`       |
| `coordinate`  | Koordinat    | `e2e4`              |
| `iccf`        | Sayısal      | `5254`              |
| `descriptive` | Klasik       | `P-K4`              |
| `fen`         | Hamle + FEN  | Terminale FEN basar |

---

## 🧩 Başlangıç Pozisyonu (FEN)

Her oyun `starting_fen` değerine göre başlar. Etütler, problemler ve orta‑oyun/final çalışmaları için idealdir.

---

## 🖱️ Fare Kontrolleri

| Eylem             | İşlev           |
| ----------------- | --------------- |
| Sol tık           | Taş seç / hamle |
| Sol tık + sürükle | Sürükle‑bırak   |
| Sağ tık           | Kare işaretleme |
| Sağ tık + sürükle | Ok çizme        |

---

## ⌨️ Klavye Kısayolları

| Kısayol             | Açıklama                       |
| ------------------- | ------------------------------ |
| **Ctrl + Z**        | Son iki hamleyi geri al        |
| **Ctrl + R**        | Oyunu sıfırla                  |
| **Ctrl + M**        | Tahtayı çevir / taraf değiştir |
| **Pencereyi kapat** | Çıkış                          |

---

## 🛠️ Kurulum (Arch Linux – Önerilen)

> Arch Linux’ta **PEP 668** nedeniyle global `pip` yasaklıdır. Bu proje **pipx** ile güvenli şekilde kurulur.

### Tek Komutla Kurulum

```bash
git clone https://github.com/ibotimew/chess.git
cd chess-app
chmod +x install.sh
./install.sh
```

Kurulumdan sonra:

```bash
chess
```

> Not: Sisteminizde `chess` komut adı çakışıyorsa, `setup.py` içindeki komut adı `offline-chess` olarak değiştirilebilir.

---

## 🗑️ Kaldırma

```bash
cd chess-app
chmod +x uninstall.sh
./uninstall.sh
```

Ayarlar da dahil olmak üzere temiz silme yapar.

---

## 📁 Proje Yapısı

```text
chess-app/
├── chess_app.py        # Ana uygulama
├── setup.py            # Paketleme / console script
├── requirements.txt    # Python bağımlılıkları
├── install.sh          # Arch Linux kurulum scripti
├── uninstall.sh        # Kaldırma scripti
├── assets/
│   ├── pieces/
│   ├── boards/
│   └── sounds/
└── README.md
```

---

## 🎯 Tasarım Felsefesi

* Menü yok
* Ayar ekranı yok
* Dikkat dağıtıcı UI yok
* Sadece **satranç**

Tüm kontrol **dosya + klavye + fare** üzerinden yapılır.

---

## 👤 Geliştirici

**ibrahim**
Offline, sade, Linux‑uyumlu satranç uygulaması

♟️ *Gerçek satranç, dikkat dağıtmadan oynanır.*
