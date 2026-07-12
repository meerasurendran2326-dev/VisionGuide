"""Clock-direction helpers for navigation guidance.

This module converts simple position labels into voice-friendly clock
references for a computer vision navigation assistant.
"""


def get_clock_direction(position):
    """
    Convert a position label to a clock-direction phrase.

    Args:
        position: One of "LEFT", "CENTER", or "RIGHT".

    Returns:
        A string describing the position as a clock direction.
        Returns "Unknown" for invalid input.
    """
    if position is None:
        return "Unknown"

    normalized_position = str(position).strip().upper()

    if normalized_position == "LEFT":
        return "10 o'clock"

    if normalized_position == "CENTER":
        return "12 o'clock"

    if normalized_position == "RIGHT":
        return "2 o'clock"

    return "Unknown"
