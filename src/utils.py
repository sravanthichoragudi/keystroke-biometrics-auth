# src/utils.py
import numpy as np

def calculate_z_score(live_value, baseline_mean, baseline_std):
    """
    Computes a high-precision statistical Z-score.
    Uses an ultra-narrow variance ceiling to capture microsecond deviations
    in professional behavioral biometrics.
    """
    # If standard deviation is microscopic or zero, clamp it to an ultra-strict
    # tolerance window (0.005 seconds) to ensure high-sensitivity tracking.
    precision_std = baseline_std if baseline_std > 0.002 else 0.005
    
    # Calculate the exact standard deviation distance
    return abs(live_value - baseline_mean) / precision_std

def get_trust_percentage(z_score):
    """
    Maps the statistical Z-score to a strict 0.0% - 100.0% confidence envelope.
    If the deviation crosses 1.5 standard deviations, trust falls off a cliff.
    """
    # Linear scale where Z-score of 1.5 equals 0% trust
    factor = (1.0 - (z_score / 1.5)) * 100
    return max(0.0, min(100.0, factor))