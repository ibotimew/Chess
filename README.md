# ♟️ Chess App (Linux Optimized)

Python ve Pygame ile geliştirilmiş, hafif (lightweight), sade ve yüksek performanslı bir satranç uygulamasıdır. Lichess estetiğinden ilham alınarak, modern geliştirme standartlarına ve Linux dosya hiyerarşisine tam uyumlu şekilde tasarlanmıştır.

## ✨ Öne Çıkan Özellikler

* **Kompakt ve Hızlı:** Gereksiz hiçbir kütüphane barındırmaz, sistem kaynaklarını tüketmez.
* **Linux Native:** Konfigürasyon dosyalarını `~/.config/chess-app/` dizininde saklar, sisteminizi kirletmez.
* **Esnek Notasyon:** Cebirsel (Algebraic), Tanımlayıcı (Descriptive), ICCF ve Koordinat notasyon sistemlerini destekler.
* **Özelleştirilebilir:** Renkler, sesler, animasyon hızı ve taş temaları tek bir JSON dosyası üzerinden yönetilir.
* **Gelişmiş Analiz Desteği:** Stockfish motoru ile entegrasyon altyapısına sahiptir.

## 🛠️ Kurulum ve Terminal Entegrasyonu

Programın en büyük özelliği, sisteminize bir paket gibi kurulabilmesidir. Böylece terminalde herhangi bir dizindeyken sadece `chess` yazarak oyunu başlatabilirsiniz.

### 1. Bağımlılıkların Yüklenmesi

pip install pygame python-chess

2. Sisteme Kurulum (Global Erişim)

Proje klasörünün içindeyken aşağıdaki komutu çalıştırarak terminal kısayolunu oluşturun:
Bash

pip install -e .

3. Çalıştırma
Bash

chess

⚙️ Yapılandırma (Configuration)

Program, "Sade Tasarım, Esnek Ayar" felsefesini benimser. Tüm ayarlar Linux standartlarına uygun olarak aşağıdaki dizinde tutulur:

~/.config/chess-app/config.json
Önemli Parametreler:
Parametre	Açıklama	Varsayılan
board_theme	Tahtanın renk teması (brown, blue, wood vb.)	brown
animation_speed	Taş hareket hızı (saniye cinsinden)	0.2
notation_scheme	Hamle kayıt sistemi	algebraic
play_sounds	Ses efektleri (Açık/Kapalı)	true
🏗️ Proje Yapısı
Plaintext

├── chess_app.py      # Ana uygulama mantığı ve GUI döngüsü
├── setup.py          # Terminal komutu (entry_point) tanımlaması
├── config.json       # Varsayılan ayar şablonu
├── requirements.txt  # Gerekli kütüphaneler listesi
└── assets/           # Görsel ve ses varlıkları

🗺️ Yol Haritası (Roadmap)

    [ ] Stockfish Entegrasyonu: Tam kapasite yapay zeka analizi.

    [ ] PGN Desteği: Oynanan maçları kaydedip tekrar izleme.

    [ ] Online Mod: WebSocket üzerinden iki kişilik oyun desteği.

Geliştirici: ibotimew

Bu proje açık kaynak topluluğu için geliştirilmiştir.