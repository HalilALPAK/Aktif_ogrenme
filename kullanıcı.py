"""import cv2
import os
import uuid
from tkinter import *
from PIL import Image, ImageTk
from ultralytics import YOLO

# ================= MODEL =================
model = YOLO("best2.pt")

CLASSES = [
    "Tshirt","jacket","long-dress","long-skirt","midi-dress","midi-skirt",
    "pants","shirt","short","short-dress","short-skirt","sweater"
]

# ================= KAMERA =================
cap = cv2.VideoCapture(0)

root = Tk()
root.title("AI Öğrenen Kıyafet Sistemi")
root.geometry("900x700")
root.configure(bg="#1e1e1e")

# ================= STYLES =================
TITLE_FONT = ("Segoe UI", 18, "bold")
TEXT_FONT = ("Segoe UI", 14)
BTN_FONT = ("Segoe UI", 12, "bold")

# ================= BAŞLIK =================
Label(root, text="AI Kıyafet Tanıma & Öğrenme Sistemi",
      font=TITLE_FONT, fg="white", bg="#1e1e1e").pack(pady=10)

# ================= VİDEO ALANI =================
video_frame = Frame(root, bg="#2b2b2b", bd=3, relief="ridge")
video_frame.pack(pady=10)

video_label = Label(video_frame)
video_label.pack()

# ================= TAHMİN PANELİ =================
prediction_frame = Frame(root, bg="#2b2b2b", bd=3, relief="ridge")
prediction_frame.pack(pady=10, fill="x", padx=50)

prediction_label = Label(prediction_frame, text="Tahmin: -",
                         font=("Segoe UI", 16, "bold"),
                         fg="cyan", bg="#2b2b2b")
prediction_label.pack(pady=10)

# ================= BUTON PANELİ =================
button_frame = Frame(root, bg="#1e1e1e")
button_frame.pack(pady=20)

current_frame = None
last_prediction = None
last_boxes = None

# ================= MODEL TAHMİN =================
def predict_frame(frame):
    results = model.predict(frame, imgsz=640, verbose=False)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return "Algılanmadı", 0.0, None

    cls_id = int(boxes.cls[0])
    conf = float(boxes.conf[0])
    xywhn = boxes.xywhn[0].tolist()

    return CLASSES[cls_id], conf, xywhn

# ================= KAMERA AKIŞ =================
def update_frame():
    global current_frame
    ret, frame = cap.read()
    if ret:
        current_frame = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    root.after(10, update_frame)

# ================= FRAME AL =================
def capture_frame():
    global last_prediction, last_boxes

    if current_frame is None:
        return

    pred, conf, xywhn = predict_frame(current_frame)
    last_prediction = pred
    last_boxes = xywhn

    prediction_label.config(
        text=f"Tahmin: {pred}  |  Güven: {conf:.2f}",
        fg="#00ffcc" if conf > 0.6 else "orange"
    )

# ================= DOĞRU =================
def correct_prediction():
    if last_prediction:
        prediction_label.config(text=f"✔ Doğru: {last_prediction}", fg="lightgreen")
        print("Doğru etiket:", last_prediction)

# ================= YANLIŞ =================
def wrong_prediction():
    global last_boxes

    if current_frame is None or last_boxes is None:
        print("Box yok, kaydedilemedi")
        return

    select_window = Toplevel(root)
    select_window.title("Gerçek Etiketi Seç")
    select_window.configure(bg="#1e1e1e")

    Label(select_window, text="Doğru sınıfı seç",
          font=("Segoe UI", 14, "bold"),
          fg="white", bg="#1e1e1e").grid(row=0, column=0, columnspan=3, pady=10)

    def save_label(correct_class_name):
        class_id = CLASSES.index(correct_class_name)

        os.makedirs("hatalı_data/images", exist_ok=True)
        os.makedirs("hatalı_data/labels", exist_ok=True)

        file_id = str(uuid.uuid4())[:8]

        cv2.imwrite(f"hatalı_data/images/{file_id}.jpg", current_frame)

        with open(f"hatalı_data/labels/{file_id}.txt", "w") as f:
            f.write(f"{class_id} {last_boxes[0]} {last_boxes[1]} {last_boxes[2]} {last_boxes[3]}")

        print("Kaydedildi:", correct_class_name)
        select_window.destroy()

    # Grid yerleşim
    row, col = 1, 0
    for cls in CLASSES:
        Button(select_window, text=cls, width=15, height=2,
               font=("Segoe UI", 10, "bold"),
               bg="#333333", fg="white",
               command=lambda c=cls: save_label(c)).grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col == 3:
            col = 0
            row += 1

# ================= BUTONLAR =================
Button(button_frame, text="📸 Frame Al", font=BTN_FONT,
       bg="#007acc", fg="white", width=20, height=2,
       command=capture_frame).grid(row=0, column=0, padx=10)

Button(button_frame, text="✅ Doğru", font=BTN_FONT,
       bg="#2ecc71", fg="white", width=20, height=2,
       command=correct_prediction).grid(row=0, column=1, padx=10)

Button(button_frame, text="❌ Yanlış", font=BTN_FONT,
       bg="#e74c3c", fg="white", width=20, height=2,
       command=wrong_prediction).grid(row=0, column=2, padx=10)

update_frame()
root.mainloop()
cap.release()
"""
import cv2
import os
import uuid
import json
from tkinter import *
from PIL import Image, ImageTk
from ultralytics import YOLO

# ================= MODEL =================
model = YOLO("best2.pt")

CLASSES = [
    "Tshirt","jacket","long-dress","long-skirt","midi-dress","midi-skirt",
    "pants","shirt","short","short-dress","short-skirt","sweater"
]

# ================= KAMERA =================
cap = cv2.VideoCapture(1)  # Kamera 1 kullan
if not cap.isOpened():
    raise Exception("Kamera açılamadı. Lütfen cihazınızı kontrol edin.")

root = Tk()
root.title("AI Öğrenen Kıyafet Sistemi")
root.geometry("900x700")
root.configure(bg="#1e1e1e")

# ================= STYLES =================
TITLE_FONT = ("Segoe UI", 18, "bold")
TEXT_FONT = ("Segoe UI", 14)
BTN_FONT = ("Segoe UI", 12, "bold")

# ================= BAŞLIK =================
Label(root, text="AI Kıyafet Tanıma & Öğrenme Sistemi",
      font=TITLE_FONT, fg="white", bg="#1e1e1e").pack(pady=10)

# ================= VİDEO ALANI =================
video_frame = Frame(root, bg="#2b2b2b", bd=3, relief="ridge")
video_frame.pack(pady=10)
video_label = Label(video_frame)
video_label.pack()

# ================= TAHMİN PANELİ =================
prediction_frame = Frame(root, bg="#2b2b2b", bd=3, relief="ridge")
prediction_frame.pack(pady=10, fill="x", padx=50)

prediction_label = Label(prediction_frame, text="Tahmin: -",
                         font=("Segoe UI", 16, "bold"),
                         fg="cyan", bg="#2b2b2b")
prediction_label.pack(pady=10)

# ================= BUTON PANELİ =================
button_frame = Frame(root, bg="#1e1e1e")
button_frame.pack(pady=20)

current_frame = None
last_prediction = None
last_boxes = None
last_confidence = None
imgtk = None  # Tkinter için global ref

# ================= MODEL TAHMİN =================
def predict_frame(frame):
    results = model.predict(frame, imgsz=640, verbose=False)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return "Algılanmadı", 0.0, None

    cls_id = int(boxes.cls[0])
    conf = float(boxes.conf[0])
    xywhn = boxes.xywhn[0].tolist()

    return CLASSES[cls_id], conf, xywhn

# ================= KAMERA AKIŞ =================
def update_frame():
    global current_frame, imgtk
    ret, frame = cap.read()
    if ret:
        current_frame = frame.copy()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    root.after(10, update_frame)

# ================= FRAME AL =================
def capture_frame():
    global last_prediction, last_boxes, last_confidence
    if current_frame is None:
        return

    pred, conf, xywhn = predict_frame(current_frame)
    last_prediction = pred
    last_boxes = xywhn
    last_confidence = conf

    prediction_label.config(
        text=f"Tahmin: {pred}  |  Güven: {conf:.2f}",
        fg="#00ffcc" if conf > 0.6 else "orange"
    )

# ================= DOĞRU =================
def correct_prediction():
    if last_prediction:
        prediction_label.config(text=f"✔ Doğru: {last_prediction}", fg="lightgreen")
        print("Doğru etiket:", last_prediction)

# ================= YANLIŞ =================
def wrong_prediction():
    global last_boxes, current_frame, last_prediction, last_confidence
    if current_frame is None or last_boxes is None:
        print("Box yok, kaydedilemedi")
        return

    select_window = Toplevel(root)
    select_window.title("Gerçek Etiketi Seç")
    select_window.configure(bg="#1e1e1e")

    Label(select_window, text="Doğru sınıfı seç",
          font=("Segoe UI", 14, "bold"),
          fg="white", bg="#1e1e1e").grid(row=0, column=0, columnspan=3, pady=10)

    def save_label(correct_class_name):
        class_id = CLASSES.index(correct_class_name)

        # Klasörler
        os.makedirs("hatalı_data/images", exist_ok=True)
        os.makedirs("hatalı_data/labels", exist_ok=True)

        file_id = str(uuid.uuid4())[:8]

        # Görsel ve label kaydı
        cv2.imwrite(f"hatalı_data/images/{file_id}.jpg", current_frame)
        with open(f"hatalı_data/labels/{file_id}.txt", "w") as f:
            f.write(f"{class_id} {last_boxes[0]} {last_boxes[1]} {last_boxes[2]} {last_boxes[3]}")

        # JSON log kaydı
        matris_path = "hatalı_data/matris.json"
        if os.path.exists(matris_path):
            with open(matris_path, "r") as f:
                try:
                    matris = json.load(f)
                except:
                    matris = []
        else:
            matris = []

        matris.append({
            "file_id": file_id,
            "predicted_class": last_prediction if last_prediction else "Unknown",
            "true_class": correct_class_name,
            "confidence": float(last_confidence) if last_confidence else None,
            "bbox": [float(x) for x in last_boxes[:4]] if last_boxes else None
        })

        with open(matris_path, "w") as f:
            json.dump(matris, f, indent=2)

        print("Kaydedildi:", correct_class_name)
        select_window.destroy()

    # Grid yerleşim
    row, col = 1, 0
    for cls in CLASSES:
        Button(select_window, text=cls, width=15, height=2,
               font=("Segoe UI", 10, "bold"),
               bg="#333333", fg="white",
               command=lambda c=cls: save_label(c)).grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col == 3:
            col = 0
            row += 1

# ================= BUTONLAR =================
Button(button_frame, text="📸 Frame Al", font=BTN_FONT,
       bg="#007acc", fg="white", width=20, height=2,
       command=capture_frame).grid(row=0, column=0, padx=10)

Button(button_frame, text="✅ Doğru", font=BTN_FONT,
       bg="#2ecc71", fg="white", width=20, height=2,
       command=correct_prediction).grid(row=0, column=1, padx=10)

Button(button_frame, text="❌ Yanlış", font=BTN_FONT,
       bg="#e74c3c", fg="white", width=20, height=2,
       command=wrong_prediction).grid(row=0, column=2, padx=10)

update_frame()
root.mainloop()
cap.release()
