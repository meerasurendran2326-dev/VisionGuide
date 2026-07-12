"""
Confidence Analyzer
-------------------
Converts YOLO confidence into human-friendly messages.
"""


def analyze_confidence(confidence: float):
    """
    Analyze detection confidence.

    Args:
        confidence (float): YOLO confidence (0-1)

    Returns:
        dict
    """

    if confidence >= 0.95:
        return {
            "level": "HIGH",
            "voice": "confirmed",
            "color": (0, 255, 0)
        }

    elif confidence >= 0.80:
        return {
            "level": "GOOD",
            "voice": "likely",
            "color": (0, 255, 255)
        }

    elif confidence >= 0.60:
        return {
            "level": "LOW",
            "voice": "possible",
            "color": (0, 165, 255)
        }

    else:
        return {
            "level": "VERY LOW",
            "voice": "uncertain",
            "color": (0, 0, 255)
        }