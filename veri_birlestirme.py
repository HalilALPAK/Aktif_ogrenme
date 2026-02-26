import os
import shutil
import random

orig_img = "Main-Fashion-1/train/images"
orig_lbl = "Main-Fashion-1/train/labels"

fb_img = "hatalı_data/images"
fb_lbl = "hatalı_data/labels"

dst_img = "dataset_updated/images"
dst_lbl = "dataset_updated/labels"

os.makedirs(dst_img, exist_ok=True)
os.makedirs(dst_lbl, exist_ok=True)

# Hatalı veri sayısı
fb_files = os.listdir(fb_img)
fb_count = len(fb_files)

# Orijinalden kaç alacağız (%70 kuralı)
orig_target = int((fb_count / 30) * 70)

orig_files = os.listdir(orig_img)
random.shuffle(orig_files)
orig_selected = orig_files[:orig_target]

print(f"Hatalı veri: {fb_count}")
print(f"Orijinalden seçilen: {orig_target}")

# --- Hatalı verileri kopyala ---
for f in fb_files:
    shutil.copy(os.path.join(fb_img, f), os.path.join(dst_img, f))
    lbl = f.replace(".jpg", ".txt")
    shutil.copy(os.path.join(fb_lbl, lbl), os.path.join(dst_lbl, lbl))

# --- Orijinal veriden rastgele kopyala ---
for f in orig_selected:
    shutil.copy(os.path.join(orig_img, f), os.path.join(dst_img, f))
    lbl = f.replace(".jpg", ".txt")
    shutil.copy(os.path.join(orig_lbl, lbl), os.path.join(dst_lbl, lbl))

print("✅ Dengeli dataset hazır!")
