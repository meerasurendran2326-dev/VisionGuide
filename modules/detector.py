"""
VisionGuide AI - Object Detector
YOLOv8 based object detection module
"""

from ultralytics import YOLO


# ----------------------------------------
# Load YOLO Model Only Once
# ----------------------------------------

model = YOLO("models/yolov8n.pt")


# ----------------------------------------
# Required Objects
# ----------------------------------------

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
    "cell phone"
}



def get_position(x1, x2, frame_width):
    """
    Find object position in frame
    """

    center_x = (x1 + x2) / 2


    if center_x < frame_width / 3:
        return "LEFT"

    elif center_x < (frame_width * 2) / 3:
        return "CENTER"

    else:
        return "RIGHT"



def estimate_distance(width):
    """
    Simple distance estimation using bbox width
    """

    if width > 250:
        return "VERY CLOSE"

    elif width > 120:
        return "NEAR"

    else:
        return "MEDIUM"



def detect_objects(frame):

    """
    Detect objects from frame.

    Returns:

    [
        {
            "object":"person",
            "confidence":0.92,
            "position":"CENTER",
            "distance":"NEAR",
            "bbox":[x1,y1,x2,y2]
        }
    ]

    """


    frame_width = frame.shape[1]


    results = model(
        frame,
        conf=0.45,
        iou=0.45,
        verbose=False
    )


    detections = []


    for box in results[0].boxes:


        class_id = int(box.cls[0])

        object_name = model.names[class_id]


        if object_name not in ALLOWED_OBJECTS:
            continue



        confidence = float(box.conf[0])


        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )


        width = x2 - x1



        position = get_position(
            x1,
            x2,
            frame_width
        )


        distance = estimate_distance(
            width
        )



        detections.append({

            "object": object_name,

            "confidence": round(
                confidence,
                2
            ),

            "position": position,

            "distance": distance,

            "bbox": [
                x1,
                y1,
                x2,
                y2
            ]

        })


    return detections