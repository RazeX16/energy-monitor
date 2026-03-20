# backend/services/dsm.py

def calculate_deviation(generation: float, schedule: float) -> float:
    """
    Calculates deviation between actual generation and scheduled generation.

    Deviation = Generation - Schedule
    """
    return generation - schedule


def calculate_penalty(deviation: float, rate: float) -> float:
    """
    Calculates DSM penalty based on deviation.

    Penalty = Deviation * Rate
    """
    return deviation * rate


def compute_dsm(generation: float, schedule: float, rate: float) -> dict:
    """
    Complete DSM calculation.

    Returns:
        {
            "generation": float,
            "schedule": float,
            "deviation": float,
            "rate": float,
            "penalty": float
        }
    """
    deviation = calculate_deviation(generation, schedule)
    penalty = calculate_penalty(deviation, rate)

    return {
        "generation": generation,
        "schedule": schedule,
        "deviation": deviation,
        "rate": rate,
        "penalty": penalty
    }