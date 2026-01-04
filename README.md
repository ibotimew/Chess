# ♟️ Chess App

Modern, sade ve Linux dostu bir satranç uygulaması. Python ve Pygame kullanılarak geliştirilmiştir. Gereksiz hiçbir bağımlılık içermez ve terminal üzerinden doğrudan çalıştırılabilir.

## 🚀 Öne Çıkan Özellikler

* **Sade ve Kompakt:** Kod yapısı anlaşılır ve hafiftir.
* **Linux Uyumluluğu:** Ayar dosyaları Linux standartlarına uygun olarak `~/.config/chess-app/` dizininde saklanır.
* **Merkezi Yapılandırma:** Tüm görsel ve sistemsel ayarlar `config.json` dosyası üzerinden kolayca değiştirilebilir.
* **Terminal Erişimi:** Programı bir kez kurduktan sonra terminale sadece `chess` yazarak başlatabilirsiniz.

## 🛠️ Kurulum ve Çalıştırma

Programı sisteminize entegre etmek için aşağıdaki adımları izleyin:

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/ibotimew/Chess.git
cd Chess
```

### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Sisteme Paket Olarak Kurun
Programı terminalden \`chess\` komutuyla çalıştırmak için projenin ana dizinindeyken:
```bash
pip install -e .
```

### 4. Başlatın
```bash
chess
```

## ⚙️ Yapılandırma (Configuration)

Tüm ayarlar \`~/.config/chess-app/config.json\` dosyasında yer alır. Bazı önemli ayarlar:

| Ayar | Açıklama |
| :--- | :--- |
| \`board_theme\` | Satranç tahtasının renk teması. |
| \`notation_scheme\` | Hamle kayıt sistemi (algebraic, iccf vb.). |
| \`animation_speed\` | Taşların hareket hızı. |
| \`play_sounds\` | Ses efektlerinin durumu (true/false). |

## 📁 Proje Yapısı

* \`chess_app.py\`: Uygulamanın ana giriş noktası ve oyun mantığı.
* \`setup.py\`: Terminal komutu oluşturmak için kullanılan kurulum dosyası.
* \`config.json\`: Varsayılan yapılandırma ayarları.
* \`assets/\`: Görseller ve ses dosyaları.

---
**Geliştirici:** [ibotimew](https://github.com/ibotimew)