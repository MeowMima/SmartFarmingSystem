
from functools import lru_cache
from pathlib import Path
import cv2

MODEL_PATH = Path("model/best (1).pt")

@lru_cache(maxsize=1)
def load_model():
    from ultralytics import YOLO
    if not MODEL_PATH.exists():
        return None
    return YOLO(str(MODEL_PATH))

def preprocess(frame):
    if frame is None:
        return None
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    elif frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def detect(frame, conf=0.3):
    frame = preprocess(frame)
    if frame is None:
        return None, []

    model = load_model()
    if model is None:
        return frame, []

    results = model.predict(frame, conf=conf, verbose=False)
    r = results[0]
    labels = []

    if r.boxes is not None:
        for box in r.boxes:
            cls = int(box.cls[0])
            score = float(box.conf[0])
            label = r.names[cls]
            labels.append(label)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(
                frame,
                f"{label} {score:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2,
            )

    return frame, labels
