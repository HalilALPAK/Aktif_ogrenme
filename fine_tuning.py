from ultralytics import YOLO

model = YOLO("best2.pt")
model.train(
    data="data_updated.yaml",
    epochs=30,
    imgsz=640,
    batch=16,
    lr0=1e-4,
    freeze=10,
    project="fashion_project",
    name="fine_tune_v1"
)
