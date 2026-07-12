import cv2
import pyttsx3
import time
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Open Camera
cap = cv2.VideoCapture(0)

VOICE_DELAY = 3
last_object = ""
last_time = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not found!")
        break

    # Detect objects
    results = model(frame)

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    current_time = time.time()

    # Loop through detected objects
    for box in results[0].boxes:

        # Object name
        class_id = int(box.cls[0])
        object_name = model.names[class_id]

        # Bounding box coordinates
        x1, y1, x2, y2 = box.xyxy[0]

        # Object center
        center_x = (x1 + x2) / 2

        # Frame width
        frame_width = frame.shape[1]

        # Find Left / Center / Right
        if center_x < frame_width / 3:
            position = "left"
        elif center_x < 2 * frame_width / 3:
            position = "ahead"
        else:
            position = "right"

        # Voice message
        message = f"{object_name} {position}"

        print(message)

        # Speak only every 3 seconds
        if object_name != last_object or current_time - last_time > VOICE_DELAY:
            engine.say(message)
            engine.runAndWait()

            last_object = object_name
            last_time = current_time

    # Show camera
    cv2.imshow("VisionGuide AI", annotated_frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()