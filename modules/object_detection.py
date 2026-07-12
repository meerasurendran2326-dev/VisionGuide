import cv2
import pyttsx3
import time
from ultralytics import YOLO

# Load YOLO Model
model = YOLO("yolov8n.pt")

# Voice
engine = pyttsx3.init()
engine.setProperty("rate", 150)

voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)

cap = cv2.VideoCapture(0)

VOICE_DELAY = 3

last_message = ""
last_time = 0

danger_objects = [
    "person",
    "chair",
    "car",
    "bus",
    "truck",
    "motorcycle",
    "bicycle",
    "dog",
    "cat"
]

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    annotated = results[0].plot()

    frame_width = frame.shape[1]

    left_blocked = False
    center_blocked = False
    right_blocked = False

    nearest_object = None
    nearest_distance = 0

    for box in results[0].boxes:

        class_id = int(box.cls[0])
        name = model.names[class_id]

        if name not in danger_objects:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        width = x2 - x1

        center_x = (x1 + x2) / 2

        if center_x < frame_width/3:
            position = "left"
            left_blocked = True

        elif center_x < 2*frame_width/3:
            position = "center"
            center_blocked = True

        else:
            position = "right"
            right_blocked = True

        # Distance
        if width > nearest_distance:
            nearest_distance = width
            nearest_object = (name, position)

        cv2.putText(
            annotated,
            f"{name} ({position})",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    # Navigation Decision
    if nearest_object:

        obj, pos = nearest_object

        if center_blocked:

            if not left_blocked:
                navigation = "Move left."

            elif not right_blocked:
                navigation = "Move right."

            else:
                navigation = "Stop. Path blocked."

        else:
            navigation = "Walk forward."

        message = f"{obj} ahead. {navigation}"

        current = time.time()

        if message != last_message or current-last_time > VOICE_DELAY:

            print(message)

            engine.say(message)
            engine.runAndWait()

            last_message = message
            last_time = current

        cv2.putText(
            annotated,
            navigation,
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255,0,0),
            3
        )

    cv2.imshow("VisionGuide AI", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()