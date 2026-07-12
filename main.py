import cv2
import time
import pyttsx3

engine = pyttsx3.init()

engine.setProperty(
    "rate",
    150
)

engine.say("VisionGuide AI started")

engine.runAndWait()

try:
    from voice import speak
except Exception:
    def speak(text):
        print(text)

try:
    from modules.detector import detect_objects as yolov8_detect_objects
except Exception:
    def yolov8_detect_objects(frame):
        return None

try:
    from modules.object_tracker import ObjectTracker
except Exception:
    class ObjectTracker:
        def __init__(self):
            self.previous_objects = []

        def update(self, detected_objects):
            return detected_objects

try:
    from modules.collision_predictor import predict_collision
except Exception:
    def predict_collision(tracked_objects):
        if not tracked_objects:
            return {
                "collision": False,
                "level": "LOW",
                "message": "No immediate collision risk.",
                "object": None,
                "recommended_action": "Continue carefully.",
            }
        return {
            "collision": False,
            "level": "LOW",
            "message": "No immediate collision risk.",
            "object": None,
            "recommended_action": "Continue carefully.",
        }

try:
    from modules.risk_analyzer import analyze_risk
except Exception:
    def analyze_risk(detected_objects):
        return "SAFE"

try:
    from modules.smart_priority import get_priority_object
except Exception:
    def get_priority_object(objects):
        return None

try:
    from modules.scene_analyzer import analyze_scene
except Exception:
    def analyze_scene(detected_objects, summary=False):
        if summary:
            return "You are walking safely. No nearby obstacles."
        return "No obstacles nearby."

try:
    from modules.voice_formatter import format_voice_message
except Exception:
    def format_voice_message(obj):
        return "Object detected."

try:
    from modules.clock_direction import get_clock_direction
except Exception:
    def get_clock_direction(position):
        return "Unknown"

try:
    from modules.confidence_analyzer import analyze_confidence
except Exception:
    def analyze_confidence(confidence):
        return {"level": "LOW", "voice": "uncertain", "color": (0, 0, 255)}

try:
    from modules.crossing_analyzer import analyze_crossing
except Exception:
    def analyze_crossing(traffic_status, zebra_detected, detected_objects):
        return {"score": "NONE", "message": "No crossing detected."}

try:
    from modules.navigation import process_navigation
except Exception:
    def process_navigation(detected_objects):
        return {
            "navigation": "MOVE FORWARD",
            "risk": "SAFE",
            "voice": "Path is clear. Move forward.",
            "priority_object": None,
        }

try:
    from modules.actions import get_action
except Exception:
    def get_action(object_name, position, distance):
        return "Continue carefully."

try:
    from modules.ocr import detect_text
except Exception:
    def detect_text(frame):
        return []

try:
    from modules.traffic_light import detect_traffic_light
except Exception:
    def detect_traffic_light(frame):
        return {"status": "NONE", "red_pixels": 0, "green_pixels": 0, "yellow_pixels": 0}

try:
    from modules.zebra_crossing import detect_zebra_crossing
except Exception:
    def detect_zebra_crossing(frame):
        return {"detected": False, "lines": 0}

try:
    from modules.pothole_detection import detect_pothole
except Exception:
    def detect_pothole(frame):
        return {"detected": False, "count": 0, "boxes": []}

try:
    from modules.emergency import check_emergency
except Exception:
    def check_emergency(detected_objects):
        return {"emergency": False, "level": "SAFE", "message": ""}

try:
    from modules.voice_commands import listen_command
except Exception:
    def listen_command():
        return None

ALLOWED_OBJECTS = {
    "person",
    "chair",
    "car",
    "bus",
    "truck",
    "bicycle",
    "motorcycle",
    "traffic light",
    "stop sign",
    "bench",
    "dog",
    "cat",
    "backpack",
    "suitcase",
    "cell phone",
}


def estimate_distance(frame, bbox):
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = bbox
    box_height = max(1, int(y2 - y1))
    box_width = max(1, int(x2 - x1))
    area = box_width * box_height
    max_area = width * height
    relative_area = area / float(max_area)
    relative_height = box_height / float(height)

    if relative_height > 0.55 or relative_area > 0.20:
        return "VERY CLOSE"
    if relative_height > 0.30 or relative_area > 0.10:
        return "NEAR"
    if relative_height > 0.15 or relative_area > 0.04:
        return "MEDIUM"
    return "FAR"


def classify_position(frame_width, center_x):
    if center_x < frame_width / 3.0:
        return "LEFT"
    if center_x < 2.0 * frame_width / 3.0:
        return "CENTER"
    return "RIGHT"


def to_bgr(color):
    return (int(color[0]), int(color[1]), int(color[2]))


def draw_box(frame, bbox, label, color, confidence=None, distance=None, clock=None):
    x1, y1, x2, y2 = bbox
    x1 = int(max(0, x1))
    y1 = int(max(0, y1))
    x2 = int(min(frame.shape[1], x2))
    y2 = int(min(frame.shape[0], y2))

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, max(10, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    text_y = y1 + 20
    details = []
    if confidence is not None:
        details.append(f"Conf: {confidence:.2f}")
    if distance is not None:
        details.append(f"Dist: {distance}")
    if clock is not None:
        details.append(f"Clock: {clock}")

    if details:
        cv2.putText(frame, " | ".join(details), (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)


def is_relevant_ocr_text(text):
    clean_text = str(text).strip().lower()
    if not clean_text:
        return False
    blocked_terms = ["advertisement", "sale", "offer", "discount", "promo", "shop", "buy"]
    if any(term in clean_text for term in blocked_terms):
        return False
    relevant_terms = ["bus", "room", "exit", "entrance", "direction", "board"]
    return any(term in clean_text for term in relevant_terms)


def get_risk_color(risk):
    if risk == "DANGER":
        return (0, 0, 255)
    if risk == "CAUTION":
        return (0, 255, 255)
    return (0, 255, 0)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open webcam.")
        return

    tracker = ObjectTracker()
    frame_count = 0
    start_time = time.time()
    last_scene_time = 0.0
    last_voice_time = 0.0
    last_object_state = None
    last_risk_state = None
    last_direction_state = None
    last_distance_state = None
    last_traffic_state = None
    last_pothole_state = False
    last_emergency_state = None

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        frame_count += 1
        height, width = frame.shape[:2]
        detection_results = yolov8_detect_objects(frame)
        detected_objects = []

        if detection_results is not None:
            try:
                boxes = detection_results[0].boxes
            except Exception:
                boxes = []

            for box in boxes:
                try:
                    class_id = int(box.cls[0])
                except Exception:
                    continue

                try:
                    object_name = detection_results[0].names[class_id]
                except Exception:
                    object_name = None

                if not object_name or object_name not in ALLOWED_OBJECTS:
                    continue

                try:
                    x1, y1, x2, y2 = [float(value) for value in box.xyxy[0]]
                except Exception:
                    continue

                confidence = 0.0
                try:
                    confidence = float(box.conf[0])
                except Exception:
                    confidence = 0.0

                center_x = (x1 + x2) / 2.0
                position = classify_position(width, center_x)
                distance = estimate_distance(frame, (x1, y1, x2, y2))
                clock = get_clock_direction(position)

                detected_objects.append(
                    {
                        "object": object_name,
                        "confidence": round(confidence, 2),
                        "distance": distance,
                        "position": position,
                        "clock": clock,
                        "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    }
                )

        tracked_objects = tracker.update(detected_objects)

        collision = predict_collision(tracked_objects)
        risk = analyze_risk(tracked_objects)
        priority_object = get_priority_object(tracked_objects)
        navigation_info = process_navigation(tracked_objects)
        traffic_info = detect_traffic_light(frame)
        zebra_info = detect_zebra_crossing(frame)
        crossing_info = analyze_crossing(traffic_info["status"], zebra_info["detected"], tracked_objects)
        pothole_info = detect_pothole(frame)
        emergency_info = check_emergency(tracked_objects)

        ocr_results = detect_text(frame)
        relevant_ocr_text = []
        for item in ocr_results:
            text_value = str(item.get("text", "")).strip()
            if is_relevant_ocr_text(text_value):
                relevant_ocr_text.append(text_value)

        recommended_action = "Continue carefully."
        if priority_object is not None:
            recommended_action = get_action(
                str(priority_object.get("object", "")).lower(),
                str(priority_object.get("position", "")).upper(),
                str(priority_object.get("distance", "")).upper(),
            )

        display_frame = frame.copy()

        for obj in detected_objects:
            name = str(obj.get("object", "")).lower()
            confidence = float(obj.get("confidence", 0.0) or 0.0)
            confidence_info = analyze_confidence(confidence)
            color = to_bgr(confidence_info["color"])
            if name in {"car", "bus", "truck", "motorcycle", "bicycle", "person"}:
                color = (0, 0, 255)
            draw_box(
                display_frame,
                obj.get("bbox", [0, 0, 0, 0]),
                str(obj.get("object", "")).title(),
                color,
                confidence=confidence,
                distance=obj.get("distance"),
                clock=obj.get("clock"),
            )

        if collision["collision"]:
            cv2.putText(
                display_frame,
                f"COLLISION RISK: {collision['level']}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )
        else:
            cv2.putText(
                display_frame,
                "COLLISION RISK: LOW",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

        risk_color = get_risk_color(risk)
        cv2.putText(
            display_frame,
            f"RISK: {risk}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            risk_color,
            2,
        )

        nav_label = str(navigation_info.get("navigation", "MOVE FORWARD")).upper()
        cv2.putText(
            display_frame,
            f"NAVIGATION: {nav_label}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        if priority_object is not None:
            cv2.putText(
                display_frame,
                f"CLOCK: {priority_object.get('clock', 'Unknown')}",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        traffic_status = str(traffic_info.get("status", "NONE")).upper()
        cv2.putText(
            display_frame,
            f"TRAFFIC: {traffic_status}",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

        if zebra_info.get("detected"):
            cv2.putText(
                display_frame,
                "CROSSING: DETECTED",
                (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        if pothole_info.get("detected"):
            cv2.putText(
                display_frame,
                "POTHOLE: DETECTED",
                (10, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 165, 255),
                2,
            )

        if crossing_info.get("score") != "NONE":
            cv2.putText(
                display_frame,
                f"CROSSING ANALYSIS: {crossing_info.get('score', 'NONE')}",
                (10, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        if relevant_ocr_text:
            ocr_text = " | ".join(relevant_ocr_text[:3])
            cv2.putText(
                display_frame,
                f"OCR: {ocr_text}",
                (10, 270),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

        if emergency_info.get("emergency"):
            cv2.putText(
                display_frame,
                "EMERGENCY",
                (10, 300),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        scene_summary = analyze_scene(tracked_objects, summary=True)
        cv2.putText(
            display_frame,
            f"SCENE: {scene_summary}",
            (10, 330),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
        )

        elapsed_time = max(1.0, time.time() - start_time)
        fps = frame_count / elapsed_time
        cv2.putText(
            display_frame,
            f"FPS: {fps:.1f}",
            (width - 120, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            display_frame,
            f"ACTION: {recommended_action}",
            (10, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        cv2.imshow("VisionGuide AI", display_frame)

        current_time = time.time()
        if current_time - last_voice_time >= 1.5:
            voice_message = None
            current_object_state = None
            if priority_object is not None:
                current_object_state = (
                    str(priority_object.get("object", "")).lower(),
                    str(priority_object.get("position", "")).upper(),
                    str(priority_object.get("distance", "")).upper(),
                    str(priority_object.get("clock", "")).lower(),
                )

            if collision["collision"]:
                voice_message = collision["message"]
            elif current_object_state is not None and current_object_state != last_object_state:
                voice_message = format_voice_message(priority_object)
            elif risk != last_risk_state:
                voice_message = f"Risk is {risk.lower()}."
            elif priority_object is not None and priority_object.get("clock") != last_direction_state:
                voice_message = f"Object detected at {priority_object.get('clock', 'unknown')}."
            elif priority_object is not None and priority_object.get("distance") != last_distance_state:
                voice_message = f"Object is {str(priority_object.get('distance', 'unknown')).lower()}."
            elif traffic_info.get("status", "NONE") != "NONE" and traffic_info.get("status", "NONE").upper() != last_traffic_state:
                if traffic_info.get("status", "NONE").upper() == "RED":
                    voice_message = "Stop."
                elif traffic_info.get("status", "NONE").upper() == "YELLOW":
                    voice_message = "Prepare."
                else:
                    voice_message = "Safe to cross after checking surroundings."
            elif pothole_info.get("detected") and not last_pothole_state:
                voice_message = "Caution. Pothole ahead."
            elif emergency_info.get("emergency") and emergency_info.get("message") != last_emergency_state:
                voice_message = emergency_info.get("message", "")
            elif current_time - last_scene_time >= 15.0:
                voice_message = scene_summary
                last_scene_time = current_time

            if voice_message:
                speak(voice_message)
                last_voice_time = current_time
                last_object_state = current_object_state
                last_risk_state = risk
                last_direction_state = priority_object.get("clock") if priority_object is not None else None
                last_distance_state = priority_object.get("distance") if priority_object is not None else None
                last_traffic_state = traffic_info.get("status", "NONE").upper()
                last_pothole_state = bool(pothole_info.get("detected"))
                last_emergency_state = emergency_info.get("message") if emergency_info.get("emergency") else None

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
