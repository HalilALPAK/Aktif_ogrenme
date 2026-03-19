<img width="1100" height="600" alt="image" src="https://github.com/user-attachments/assets/0fba874d-661a-4382-bfce-925fb9f6b604" />

# Active Learning with SAM2 — Feedback-Driven Label Refinement

Kısa açıklama

Bu proje, "kalitesiz etiketlenmiş veri" problemini azaltmak için Aktif Öğrenme (Active Learning) ve SAM2 (Segment Anything Model 2 / MobileSAM) teknolojilerini birleştiren uçtan-uça bir pipeline sunar. Sistem, kullanıcı geri bildirimlerini (hatalı tahminler) alır, bu örnekleri piksel hassasiyetinde SAM2 ile rafine eder ve modelin performansını koruyarak küçük bir oran (%10) ile yeniden eğitir (fine-tune).

Amaç

- Gerçek dünyada kullanıcı tarafından işaretlenen hatalara odaklanarak veri kalitesini yükseltmek.
- Rafine edilmiş maskeler/box'lar kullanılarak modelin spesifik hata sınıflarında performansını artırmak.
- Hesaplama maliyetini düşürmek için verimlilik filtreleri uygulamak.

Öne çıkan özellikler

- Feedback-Driven Discovery: Modelin belirsiz olduğu örneklerin yanı sıra kullanıcı tarafından raporlanan gerçek hatalara öncelik verir.
- SAM2 Box Refinement: Kaba (loose) bounding box'ları MobileSAM ile tight (objeyi saran) kutulara dönüştürür.
- Efficiency Layer: Her hata bildirimi SAM2'ye gönderilmez; IoU ve objectness tabanlı filtreleme ile gereksiz hesaplamalar azaltılır.
- Experience Replay (%70 / %30): Fine-tuning sırasında %70 eski (doğru) veri, %30 yeni (rafine edilmiş) veri kullanılarak katastrofik unutma engellenir.

Teknik mimari (yüksek seviye)

1. Prediction: Hazır bir YOLO tabanlı model giriş görüntüsünde tahmin (boxes, scores) üretir.
2. User Correction: Kullanıcı yanlış sınıf veya yanlış box bildiriminde bulunur.
3. Filtering: Bildirilen örnekler IoU / objectness gibi kriterlerle filtrelenir; yalnızca gerekli olanlar SAM2'ye gönderilir.
4. Refinement: MobileSAM (veya SAM2) zero-shot segmentasyon ile maskeler üretir; maskeden tight box çıkarılır.
5. Aggregation: Rafine edilmiş örnekler birikerek ana veri setinin %10'una denk gelecek kadar toplanır.
6. Fine-tuning: Model, düşük öğrenme oranı (örnek: 1e-5) ile 3–5 epoch arasında ince ayar yapılır.

Kurulum

```bash
git clone https://github.com/kullaniciadi/active-learning-sam2.git
cd active-learning-sam2
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# veya conda
# conda create -n al-sam2 python=3.10 -y
# conda activate al-sam2

pip install -r requirements.txt
# Eğer requirements yoksa minimum:
# pip install ultralytics opencv-python matplotlib numpy torch
```

Hızlı kullanım: Box Refinement örneği

Aşağıdaki örnek, kullanıcı tarafından verilen kaba kutuyu MobileSAM ile nasıl rafine edeceğinizi gösterir.

```python
from ultralytics import SAM

# MobileSAM modelini yükle (yolu kendinize göre ayarlayın)
sam_model = SAM('mobile_sam.pt')

# Kullanıcının kaba kutusu [x1, y1, x2, y2]
raw_box = [100, 150, 500, 800]

# SAM ile rafine et (source olarak numpy array veya dosya yolu geçilebilir)
results = sam_model.predict(source='image.jpg', bboxes=[raw_box])

# results nesnesinden maskeyi ve tight box'u çıkarın (scripts/refine.py içinde yardımcı fonksiyonlar bulunur)
```

Pipeline parametreleri ve öneriler

- Fine-tune oranı ve strateji: Deneysel olarak %10 yeni veriyi hedefleyin. Eğitim parametre örneği: lr=1e-5, 3–5 epoch, küçük batch size.
- Efficiency filter: IoU < 0.4 veya objectness < 0.3 gibi eşikler ile SAM çağrılarını sınırlandırabilirsiniz.
- Replay buffer: Yeni rafine veriyi küçük partiler halinde ana veriyle harmanlayıp ardışık fine-tuning turları yapın.

Metodoloji ve referans

- %10'luk veri değişim oranı, incremental/continual learning literatüründe dengeyi korumak amaçlı sık kullanılan bir yaklaşımdır.
- Proje, kullanıcı merkezli veri seçimi (human-in-the-loop) ile modelin hatalı örneklerde daha hızlı düzelmesini hedefler.

Dosya/dizin yapısı (örnek)

- scripts/
  - refine.py # Kaba box -> SAM mask -> tight box dönüşümü yardımcı fonksiyonları
  - train.py # Fine-tuning pipeline
- data/
  - images/
  - labels/
- models/
  - mobile_sam.pt
  - best_yolo.pt
- README_ACTIVE_LEARNING.md

Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
