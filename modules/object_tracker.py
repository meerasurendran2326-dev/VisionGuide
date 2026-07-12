"""Lightweight object tracking for VisionGuide AI.

This module provides a simple tracker that links detected objects between
consecutive frames using object class and bounding box center distance.
It is intentionally lightweight and does not depend on external tracking
libraries such as DeepSORT or ByteTrack.
"""

from typing import Dict, List, Optional, Tuple


class ObjectTracker:
    """Track detected objects between frames using simple heuristics."""

    def __init__(self) -> None:
        """Initialize tracker state."""
        self.previous_objects: List[Dict] = []

    def update(self, detected_objects: List[Dict]) -> List[Dict]:
        """
        Match current detections with previous detections and enrich them
        with simple motion information.

        Args:
            detected_objects: A list of dictionaries describing current
                detections. Each item should contain at least:
                - object
                - position
                - distance
                - confidence
                - bbox

        Returns:
            A list of tracked objects enriched with movement and center data.
        """
        current_objects: List[Dict] = []

        for obj in detected_objects:
            bbox = obj.get("bbox")
            if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
                continue

            x1, y1, x2, y2 = [float(value) for value in bbox]
            center_x = (x1 + x2) / 2.0
            center_y = (y1 + y2) / 2.0
            area = max(0.0, (x2 - x1) * (y2 - y1))

            matched_previous: Optional[Dict] = None
            min_distance = None

            for prev_obj in self.previous_objects:
                prev_bbox = prev_obj.get("bbox")
                if not isinstance(prev_bbox, (list, tuple)) or len(prev_bbox) != 4:
                    continue

                prev_name = str(prev_obj.get("object", "")).lower()
                current_name = str(obj.get("object", "")).lower()

                # Match only when object class is the same.
                if prev_name != current_name:
                    continue

                prev_x1, prev_y1, prev_x2, prev_y2 = [
                    float(value) for value in prev_bbox
                ]
                prev_center_x = (prev_x1 + prev_x2) / 2.0
                prev_center_y = (prev_y1 + prev_y2) / 2.0

                # Measure center distance between previous and current boxes.
                distance = ((center_x - prev_center_x) ** 2 + (center_y - prev_center_y) ** 2) ** 0.5

                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    matched_previous = prev_obj

            movement = "STATIONARY"
            if matched_previous is not None:
                prev_bbox = matched_previous.get("bbox")
                if isinstance(prev_bbox, (list, tuple)) and len(prev_bbox) == 4:
                    prev_x1, prev_y1, prev_x2, prev_y2 = [float(value) for value in prev_bbox]
                    prev_area = max(0.0, (prev_x2 - prev_x1) * (prev_y2 - prev_y1))

                    if area > prev_area:
                        movement = "APPROACHING"
                    elif area < prev_area:
                        movement = "MOVING AWAY"

            tracked_obj = {
                "object": obj.get("object"),
                "position": obj.get("position"),
                "distance": obj.get("distance"),
                "confidence": obj.get("confidence"),
                "bbox": [x1, y1, x2, y2],
                "movement": movement,
                "center": [round(center_x, 2), round(center_y, 2)],
            }
            current_objects.append(tracked_obj)

        self.previous_objects = current_objects
        return current_objects
