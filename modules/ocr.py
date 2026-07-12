"""
VisionGuide AI - OCR Module

Detects useful text:
- Sign boards
- Bus names
- Exit boards
- Room numbers
"""

import easyocr



# ---------------------------------------
# Load OCR Model Only Once
# ---------------------------------------

reader = easyocr.Reader(
    ['en'],
    gpu=False
)



last_texts = set()



def detect_text(frame):

    """
    Detect text from image.

    Returns:

    [
        {
            "text":"EXIT",
            "confidence":0.92,
            "bbox":[x1,y1,x2,y2]
        }
    ]

    """



    results = reader.readtext(
        frame,
        detail=1
    )



    detected_texts = []



    for bbox, text, confidence in results:



        confidence = float(confidence)



        # Ignore low confidence

        if confidence < 0.60:
            continue



        text = str(text).strip()



        # Ignore very small text

        if len(text) < 2:
            continue



        # Limit huge sentences

        if len(text) > 40:
            continue



        x1 = int(
            bbox[0][0]
        )

        y1 = int(
            bbox[0][1]
        )


        x2 = int(
            bbox[2][0]
        )

        y2 = int(
            bbox[2][1]
        )



        detected_texts.append({

            "text": text,

            "confidence":
                round(confidence,2),

            "bbox":
                [
                    x1,
                    y1,
                    x2,
                    y2
                ]

        })



    # Highest confidence first

    detected_texts.sort(

        key=lambda x:
        x["confidence"],

        reverse=True

    )



    return detected_texts



def get_main_text(text_results):

    """
    Returns most important text
    for voice output.
    """

    global last_texts



    if not text_results:
        return None



    current_texts = set()



    for item in text_results:

        current_texts.add(
            item["text"]
        )



    # Remove repeated OCR

    new_texts = current_texts - last_texts



    last_texts = current_texts



    if new_texts:

        return list(new_texts)[0]


    return None