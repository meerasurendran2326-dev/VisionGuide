"""
VisionGuide AI - Zebra Crossing Detection

Detects zebra crossing based on:
- Multiple horizontal white stripes
- Road region
- Parallel line pattern
"""

import cv2
import numpy as np



def detect_zebra_crossing(frame):

    """
    Returns:

    {
        "detected": True/False,
        "lines": count
    }

    """


    height, width = frame.shape[:2]



    # ---------------------------------
    # Use road region only
    # ---------------------------------

    roi = frame[
        int(height * 0.55):height,
        0:width
    ]



    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )



    # Blur

    blur = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )



    # White stripe detection

    _, thresh = cv2.threshold(
        blur,
        190,
        255,
        cv2.THRESH_BINARY
    )



    # Remove noise

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (5,5)
    )


    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )



    edges = cv2.Canny(
        thresh,
        50,
        150
    )



    lines = cv2.HoughLinesP(

        edges,

        1,

        np.pi/180,

        threshold=50,

        minLineLength=80,

        maxLineGap=20

    )



    horizontal_lines = []



    if lines is not None:


        for line in lines:


            x1,y1,x2,y2 = line[0]


            angle = abs(
                np.degrees(
                    np.arctan2(
                        y2-y1,
                        x2-x1
                    )
                )
            )



            # Nearly horizontal

            if angle < 10:


                horizontal_lines.append(
                    y1
                )



    # ---------------------------------
    # Check stripe count
    # ---------------------------------

    line_count = len(
        horizontal_lines
    )



    detected = False



    if line_count >= 5:


        horizontal_lines.sort()


        # Check spacing between stripes

        gaps = []


        for i in range(
            1,
            len(horizontal_lines)
        ):

            gaps.append(
                abs(
                    horizontal_lines[i]
                    -
                    horizontal_lines[i-1]
                )
            )



        # Zebra stripes have repeated gaps

        valid_gaps = [

            g for g in gaps
            if 5 < g < 80

        ]



        if len(valid_gaps) >= 4:

            detected = True



    return {

        "detected":
            detected,

        "lines":
            line_count

    }