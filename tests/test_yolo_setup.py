"""Sanity check: verify YOLOv8 loads and runs on a single image."""
from ultralytics import YOLO

def main():
    print("Loading YOLOv8n pretrained weights...")
    model = YOLO("yolov8n.pt")  # auto-downloads first time (~6 MB)
    print("Model loaded.\n")

    print("Running inference on sample image...")
    results = model("https://ultralytics.com/images/bus.jpg")

    for r in results:
        print(f"\nDetected {len(r.boxes)} objects:")
        for box in r.boxes:
            cls_id = int(box.cls)
            conf = float(box.conf)
            cls_name = model.names[cls_id]
            print(f"  - {cls_name}: {conf:.2f}")

    print("\nSetup verified.")

if __name__ == "__main__":
    main()