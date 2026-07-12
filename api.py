from fastapi import FastAPI
import cv2

from modules.detector import detect_objects
from modules.ocr import detect_text
from modules.traffic_light import detect_traffic_light
from modules.zebra_crossing import detect_zebra_crossing
from modules.pothole_detection import detect_pothole
from modules.path_planner import find_safe_path
from modules.risk_analyzer import analyze_risk
from modules.emergency import check_emergency

app = FastAPI(
    title="VisionGuide AI API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "project": "VisionGuide AI",
        "status": "Running"
    }


@app.get("/detect")
def detect():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    cap.release()

    if not ret:
        return {
            "error": "Camera not available"
        }

    # -----------------------------
    # Object Detection
    # -----------------------------
    results = detect_objects(frame)

    detected_objects = []

    frame_width = frame.shape[1]

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        object_name = results[0].names[class_id]

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        center_x = (x1 + x2) / 2

        if center_x < frame_width / 3:
            position = "LEFT"

        elif center_x < 2 * frame_width / 3:
            position = "CENTER"

        else:
            position = "RIGHT"

        width = x2 - x1

        if width > 350:
            distance = "VERY CLOSE"

        elif width > 220:
            distance = "NEAR"

        elif width > 100:
            distance = "MEDIUM"

        else:
            distance = "FAR"

        detected_objects.append({
            "object": object_name,
            "confidence": round(confidence, 2),
            "position": position,
            "distance": distance
        })

    # -----------------------------
    # Other Modules
    # -----------------------------

    ocr = detect_text(frame)

    traffic = detect_traffic_light(frame)

    zebra = detect_zebra_crossing(frame)

    pothole = detect_pothole(frame)

    navigation = find_safe_path(detected_objects)

    risk = analyze_risk(detected_objects)

    emergency = check_emergency(detected_objects)

    # -----------------------------
    # Final JSON
    # -----------------------------

    return {

        "objects": detected_objects,

        "navigation": navigation,

        "risk": risk,

        "traffic_light": traffic["status"],

        "ocr": ocr,

        "zebra_crossing": zebra,

        "pothole": pothole,

        "emergency": emergency

    }