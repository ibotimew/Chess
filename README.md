# ♟️ Offline Chess Application (Lichess‑benzeri)

Bu proje, **tamamen offline çalışan**, sade arayüzlü ve **Lichess deneyimini temel alan** bir satranç uygulamasıdır. Python ile geliştirilmiştir ve herhangi bir internet bağlantısına ihtiyaç duymaz.

Uygulama; **python‑chess** kütüphanesi, **Stockfish satranç motoru** ve **pygame** tabanlı bir grafik arayüz kullanır. Amaç; minimum buton, maksimum odak prensibiyle yalnızca satranç oynamaktır.

---

## 📌 Temel Özellikler

- 📴 %100 **offline** çalışır
- ♞ **Stockfish** motoru ile oynama
- 🎨 **Lichess taş ve tahta temaları**
- ⚙️ Tüm ayarlar **config dosyası** üzerinden yapılır
- 🖥️ Minimal arayüz (buton, menü, reklam yok)
- ♻️ Geri alma / yeniden yapma (undo / redo)
- 💾 Oyun kaydetme & yükleme (PGN)
- 🧠 Farklı zorluk seviyeleri

---

## 🧠 Kullanılan Satranç Motoru

Uygulama, **Stockfish** satranç motorunu kullanır.

### Neden Stockfish?
- Açık kaynak
- Dünyanın en güçlü satranç motorlarından biri
- Offline çalışabilir
- python‑chess ile doğrudan entegre edilebilir

Motor, `python-chess` üzerinden **UCI protokolü** ile çalıştırılır.

> ⚠️ Not: Stockfish ikili dosyası (binary) sisteminizde yüklü olmalıdır.

---

## ⚙️ Ayarlar (Config Sistemi)

Uygulamadaki **tüm ayarlar** tek bir dosyadan yönetilir.

### 📁 Config Dosyasının Konumu

```text
~/.config/chess-app/config.json
```

(İlk çalıştırmada otomatik oluşturulur)

---

### 🧩 Yapılabilen Ayarlar

```json
{
  "engine_path": "/usr/bin/stockfish",
  "engine_skill": 10,
  "engine_depth": 15,
  "board_theme": "lichess_default",
  "piece_theme": "lichess_default",
  "fullscreen": false,
  "sound": true,
  "autosave": true
}
```

#### Açıklamalar

| Ayar | Açıklama |
|----|----|
| `engine_path` | Stockfish binary yolu |
| `engine_skill` | Zorluk seviyesi (0‑20) |
| `engine_depth` | Hesaplama derinliği |
| `board_theme` | Tahta teması |
| `piece_theme` | Taş teması |
| `fullscreen` | Tam ekran modu |
| `sound` | Sesler açık / kapalı |
| `autosave` | Otomatik PGN kaydı |

---

## 🎮 Kontroller

| Tuş | İşlev |
|---|---|
| Mouse | Taş sürükleme |
| `Z` | Geri al (Undo) |
| `Y` | İleri al (Redo) |
| `S` | Oyunu kaydet |
| `L` | Oyun yükle |
| `ESC` | Çıkış |

---

## 🛠️ Kurulum

### 1️⃣ Gerekli Paketler

```bash
sudo pacman -S python python-pip stockfish
```

(Dağıtımınıza göre uyarlayabilirsiniz)

---

### 2️⃣ Projeyi Klonla

```bash
git clone https://github.com/yourname/chess-app.git
cd chess-app
```

---

### 3️⃣ Python Bağımlılıkları

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Çalıştırma

```bash
python chess_app.py
```

veya

```bash
chess
```

---

## 🗑️ Kaldırma (Silme)

### 1️⃣ Python Paketi

```bash
pip uninstall chess-app
```

### 2️⃣ Ayar Dosyaları

```bash
rm -rf ~/.config/chess-app
```

### 3️⃣ Kaydedilmiş Oyunlar

```bash
rm -rf ~/Documents/chess-games
```

---

## 📂 Proje Yapısı

```text
chess-app/
│── chess_app.py        # Ana uygulama
│── requirements.txt    # Python bağımlılıkları
│── setup.py            # Paketleme dosyası
│── assets/
│   ├── pieces/         # Lichess taşları
│   ├── boards/         # Tahta temaları
│   └── sounds/         # Ses dosyaları
│── README.md
```

---

## 🧪 Test Edilen Sistemler

- Arch Linux + Hyprland
- Python 3.11+
- Stockfish 16+

---

## 📜 Lisans

Bu proje **kişisel ve eğitim amaçlıdır**.

- Stockfish → GPL
- Lichess assetleri → Lichess lisansı

Ticari kullanım için ilgili lisansları inceleyiniz.

---

## ✨ Amaç

Bu proje;
- sade satranç deneyimi
- offline kullanım
- öğrenme ve geliştirme

amacıyla hazırlanmıştır.

---

♟️ **İyi oyunlar!**

