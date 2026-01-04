# ♟️ Chess App - Python

Bu proje, Python ve Pygame kütüphanesi kullanılarak geliştirilmiş, görsel arayüze sahip bir satranç uygulamasıdır. Hem başlangıç düzeyindeki geliştiriciler için bir örnek teşkil eder hem de yerel olarak satranç oynamanıza olanak sağlar.

## 🚀 Özellikler

* **Tam Satranç Kuralları:** Rok, geçerken alma (en passant) ve piyon terfisi dahil.
* **Görsel Arayüz:** Pygame ile optimize edilmiş akıcı taş hareketleri.
* **Konfigürasyon Desteği:** `config.json` üzerinden ayarlanabilir parametreler.
* **Ses Efektleri:** Galibiyet ve hamle durumları için ses desteği.
* **Hata Günlüğü:** `chess_error.log` ile çalışma anındaki hataların takibi.

## 🛠️ Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/ibotimew/Chess.git](https://github.com/ibotimew/Chess.git)
    cd Chess
    ```

2.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Varlıkları (Assets) İndirin:**
    Eğer taş görselleri ve sesler eksikse, yardımcı betiği çalıştırın:
    ```bash
    python download_assets.py
    ```

4.  **Oyunu Başlatın:**
    ```bash
    python chess_app.py
    ```

## 📁 Dosya Yapısı

* `chess_app.py`: Oyunun ana döngüsü ve mantığının bulunduğu dosya.
* `assets/`: Taş görselleri ve ses dosyalarının bulunduğu klasör.
* `config.json`: Oyun ayarları (ekran boyutu, renkler vb.).
* `requirements.txt`: Gerekli Python kütüphanelerinin listesi.

## 📝 Gelecek Planları

- [ ] Yapay zekaya karşı oynama modu (Stockfish entegrasyonu).
- [ ] Online multiplayer desteği.
- [ ] Hamle geçmişini geri alma (Undo) özelliği.

## 🤝 Katkıda Bulunma

1. Bu depoyu çatallayın (Fork).
2. Yeni bir özellik dalı oluşturun (`git checkout -b ozellik/yeniOzellik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`).
4. Dalınıza push yapın (`git push origin ozellik/yeniOzellik`).
5. Bir Çekme İsteği (Pull Request) açın.

---
Geliştiren: [ibotimew](https://github.com/ibotimew)