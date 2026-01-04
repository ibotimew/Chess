# ♟️ Offline Chess App (Lichess‑Benzeri, Stockfish Destekli)

Bu proje **tamamen offline** çalışan, **Python + Pygame** tabanlı, minimalist ve profesyonel bir satranç uygulamasıdır. Arayüz felsefesi olarak **Lichess** sade yapısını örnek alır: ekranda yalnızca **tahta ve taşlar** bulunur; buton, menü veya dikkat dağıtıcı UI öğeleri yoktur.

Uygulama, hamle üretimi ve yapay zekâ rakip için **Stockfish** motorunu kullanır. Ayarların tamamı Linux standartlarına uygun şekilde **`~/.config/chess-app/config.json`** dosyasından yapılır.

---

## 📌 Genel Özellikler

- ✅ **Tamamen offline** çalışma
- ♜ **Stockfish UCI motoru** entegrasyonu
- 🎨 Lichess tarzı **tahta & taş temaları**
- 📐 **Pencere yeniden boyutlandırma** (kare olmak zorunda değil)
- 🖱️ **Sürükle‑bırak** ve **tıkla‑tıkla** hamle sistemi
- 🔄 **Undo (geri alma)** – animasyonlu
- 🔁 **Tahta çevirme / taraf değiştirme**
- ✍️ **Ok çizme ve kare işaretleme** (analiz için)
- 🔔 Hamle, yeme, şah, mat, rok vb. **ses efektleri**
- 🧠 Çoklu **notasyon desteği** (Algebraic, ICCF, Coordinate, Descriptive, FEN)
- ♟️ **FEN ile başlangıç pozisyonu** belirleme

---

## 🤖 Kullanılan Satranç Motoru (Stockfish)

Uygulama herhangi bir gömülü motor içermez. Bunun yerine sisteminizde kurulu olan **Stockfish** motorunu **UCI protokolü** üzerinden çalıştırır.

### Motorun Görevleri

- Bilgisayara hamle oynatmak
- Oyun sırasında pozisyon değerlendirmesi yapmak
- Oyuncuya karşı rakip olmak

### Motor Ayarları

Aşağıdaki ayarlar `config.json` içinden kontrol edilir:

| Ayar | Açıklama |
|----|----|
| `stockfish_path` | Stockfish ikili dosyasının yolu (`/usr/bin/stockfish`) |
| `stockfish_depth` | Arama derinliği (zorluk seviyesi) |
| `stockfish_time` | Hamle başına maksimum düşünme süresi (saniye) |

**Zorluk önerisi:**
- Kolay: `depth = 1–3`
- Orta: `depth = 6–10`
- Güçlü: `depth = 12+`

---

## ⚙️ Yapılandırma Sistemi (config.json)

Uygulama ilk kez çalıştırıldığında otomatik olarak şu dizini oluşturur:

```text
~/.config/chess-app/
```

ve içine `config.json` dosyasını yazar.

### Örnek config.json

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

## ✍️ Desteklenen Notasyonlar

| Notasyon | Açıklama | Örnek |
|-------|-------|-------|
| `algebraic` | Standart SAN | `Nf3`, `exd5` |
| `coordinate` | Kare koordinatlı | `e2e4` |
| `iccf` | Sayısal | `5254` |
| `descriptive` | Eski İngiliz | `P-K4` |
| `fen` | Hamle + FEN çıktısı | terminale FEN basar |

Notasyon türü `notation_scheme` alanından seçilir.

---

## 🧩 Başlangıç Pozisyonu (FEN)

Her oyun başlangıcında tahta şu ayara göre kurulur:

```json
"starting_fen": "..."
```

Bu sayede:
- Satranç problemleri
- Etütler
- Orta oyun / final pozisyonları

ile doğrudan başlayabilirsiniz.

---

## 🖱️ Fare Kontrolleri

| Eylem | İşlev |
|----|----|
| Sol tık | Taş seç / hamle yap |
| Sol tık + sürükle | Sürükle‑bırak hamle |
| Sağ tık | Kare işaretleme |
| Sağ tık + sürükle | Ok çizme |

---

## ⌨️ Klavye Kısayolları

| Kısayol | Açıklama |
|------|------|
| **Ctrl + Z** | Son iki hamleyi geri al (oyuncu + motor) |
| **Ctrl + R** | Oyunu sıfırla |
| **Ctrl + M** | Tahtayı çevir / taraf değiştir |
| **Pencereyi kapat** | Çıkış |

---

## 🛠️ Kurulum

### 1️⃣ Gereksinimler

- Python **3.10+**
- Stockfish (`sudo pacman -S stockfish` veya `apt install stockfish`)

### 2️⃣ Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 3️⃣ Uygulamayı Kur (önerilen)

```bash
pip install -e .
```

Kurulumdan sonra terminalden:

```bash
chess
```

yazarak çalıştırabilirsiniz.

Alternatif olarak:

```bash
python chess_app.py
```

---

## 🗑️ Kaldırma (Temiz Silme)

### 1️⃣ Python paketini kaldır

```bash
pip uninstall chess-app
```

### 2️⃣ Ayar dosyalarını sil

```bash
rm -rf ~/.config/chess-app
```

### 3️⃣ Proje klasörünü sil

```bash
rm -rf chess-app/
```

---

## 📁 Proje Yapısı

```text
chess-app/
├── chess_app.py        # Ana uygulama
├── setup.py            # Paketleme
├── requirements.txt    # Bağımlılıklar
├── assets/
│   ├── pieces/
│   ├── boards/
│   └── sounds/
└── README.md
```

---

## 🎯 Tasarım Felsefesi

- Menü yok
- Ayar ekranı yok
- UI karmaşası yok
- Sadece **satranç**

Tüm kontrol **dosya + klavye + fare** üzerinden yapılır.

---

## 👤 Geliştirici

**ibrahim**  
Minimalist, offline, Linux‑uyumlu satranç uygulaması

---

♟️ *Gerçek satranç, dikkat dağıtmadan oynanır.*

