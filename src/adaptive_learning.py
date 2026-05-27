# src/adaptive_learning.py
import numpy as np
import streamlit as st

def update_biometric_blueprint(successful_cadence, alpha=0.15):
    """
    Dynamically updates the user's baseline speed using an Exponential Moving Average (EMA).
    This allows the system to adapt to natural human behavioral drift over time.
    """
    # Fetch current baseline parameters from state memory
    current_avg = st.session_state.get('baseline_avg_speed')
    current_std = st.session_state.get('baseline_std')
    
    if current_avg is not None and current_std is not None:
        # 1. Update the running average speed
        new_avg = (alpha * successful_cadence) + ((1 - alpha) * current_avg)
        
        # 2. Update the variance delta scale safely
        current_variance = current_std ** 2
        new_variance = (alpha * (successful_cadence - current_avg) ** 2) + ((1 - alpha) * current_variance)
        new_std = np.sqrt(new_variance)
        
        # 3. Commit the new adaptive parameters back to memory
        st.session_state.baseline_avg_speed = float(new_avg)
        st.session_state.baseline_std = float(max(0.01, new_std)) # Avoid zero variance division flaws
        
        return True
    return False