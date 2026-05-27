# src/interfaces.py
import streamlit as st
import time
import pandas as pd
import numpy as np
from src.utils import calculate_z_score, get_trust_percentage

def render_enrollment_view(engine):
    st.subheader("👤 Account Biometric Profile Registration")
    st.markdown("Create your account credentials below. The system will map your unique typing cadence.")
    
    username = st.text_input("Create Target User ID Handle:", value="")
    
    if 'enroll_input_key' not in st.session_state: 
        st.session_state.enroll_input_key = 0
        
    current_samples_count = len(st.session_state.profile_data_buffer)
    
    if current_samples_count < 3:
        custom_password = st.text_input(
            "Create Your Custom Password:", 
            key=f"enroll_input_{st.session_state.enroll_input_key}",
            type="password"
        )
        
        # Start tracking total time the moment they type anything
        if custom_password and 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()

        if st.button("💾 SAVE TYPING SAMPLE STEP"):
            if len(custom_password) >= 4:
                
                # --- SINGLE MANDATORY CONDITION ADDED TO PREVENT S1, S2, S3 MISMATCHES ---
                if current_samples_count > 0 and custom_password != st.session_state.get('registered_password'):
                    st.error("❌ STRING MISMATCH: Verification passkey must match your original password input exactly!")
                    del st.session_state['start_time']
                else:
                    # Calculate absolute total velocity over password length
                    total_duration = time.time() - st.session_state.get('start_time', time.time())
                    calculated_unit_speed = total_duration / len(custom_password)
                    calculated_unit_speed = max(0.05, min(2.5, calculated_unit_speed))
                    
                    st.session_state.registered_password = custom_password
                    st.session_state.registered_username = username
                    
                    telemetry_payload = {
                        'H.s': calculated_unit_speed, 'F.s.e': calculated_unit_speed * 1.05,
                        'H.e': calculated_unit_speed * 0.95, 'F.e.c': calculated_unit_speed * 1.10,
                        'H.c': calculated_unit_speed, 'F.c.u': calculated_unit_speed * 1.15,
                        'H.u': calculated_unit_speed * 0.90, 'F.u.r': calculated_unit_speed * 1.20,
                        'H.r': calculated_unit_speed
                    }
                    
                    st.session_state.profile_data_buffer.append(telemetry_payload)
                    del st.session_state['start_time'] # Wipe clock for fresh next sample
                    st.session_state.enroll_input_key += 1
                    st.success(f"⚙️ Vector Logged: Sample #{len(st.session_state.profile_data_buffer)} registered!")
                    time.sleep(0.4)
                    st.rerun()
            else:
                st.error("❌ Password field too short (minimum 4 characters)!")
    else:
        st.info("🎯 Database Quota Reached: Baseline signatures completely mapped.")

    st.markdown("---")
    st.metric(label="Telemetry Vectors Stacked", value=f"{current_samples_count} / 3")
    
    if current_samples_count >= 3:
        if st.button("🔒 FINALIZE ACCOUNT SECURITY ENROLLMENT"):
            st.session_state.compiled_brain = engine.train_user_profile(st.session_state.profile_data_buffer)
            
            speeds = [sample['H.s'] for sample in st.session_state.profile_data_buffer]
            st.session_state.baseline_avg_speed = np.mean(speeds)
            st.session_state.baseline_std = np.std(speeds)
            
            # Reset gateway tracking parameters
            if 'gate_start_time' in st.session_state: del st.session_state['gate_start_time']
            st.success("🔒 Identity signature encrypted! Initializing Firewall...")
            time.sleep(1.2)
            st.rerun()

def render_security_gate_view():
    st.subheader("🔒 Continuous Verification Firewall Gateway")
    st.markdown("### **Zero-Trust Input Pipeline Challenge**")
    
    # Fetch registration parameters safely from state memory
    expected_user = st.session_state.get('registered_username', 'NOT_FOUND')
    expected_pass = st.session_state.get('registered_password', 'NOT_FOUND')
    baseline_speed = st.session_state.get('baseline_avg_speed', 0.15)
    baseline_variance = st.session_state.get('baseline_std', 0.05)

    login_user = st.text_input("Account Identity User ID Handle:").strip()
    
    if 'auth_character_times' not in st.session_state: st.session_state.auth_character_times = []
    if 'last_char_count' not in st.session_state: st.session_state.last_char_count = 0

    login_pass = st.text_input("Enter Profile Access Key Password:", type="password")
    current_len = len(login_pass)
    
    if login_pass and 'gate_start_time' not in st.session_state:
        st.session_state.gate_start_time = time.time()
        
    if len(login_pass) == 0 and 'gate_start_time' in st.session_state:
        del st.session_state['gate_start_time']
        
    if st.button("🛡️ EXECUTE AUTHENTICATION SCAN"):
        # Pull historical enrollment min/max speeds
        speeds = [sample['H.s'] for sample in st.session_state.profile_data_buffer]
        min_allowed_speed = min(speeds) * 0.85
        max_allowed_speed = max(speeds) * 1.15
        
        # --- FIXED COPY-PASTE HOLE HERE ---
        if len(login_pass) >= 1 and 'gate_start_time' in st.session_state:
            total_gate_duration = time.time() - st.session_state.gate_start_time
            
            # If duration is under 10 milliseconds, it is an instant copy-paste/bot injection
            if total_gate_duration < 0.01:
                inferred_cadence = 0.000
            else:
                inferred_cadence = total_gate_duration / len(login_pass)
        else:
            inferred_cadence = 0.000 # If no timing tracked, it defaults to zero (Locked Out)
            
        z_score = calculate_z_score(inferred_cadence, baseline_speed, baseline_variance)
        trust_percentage = get_trust_percentage(z_score)
        
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Verification Gate Decision")
            
            is_username_match = (login_user == expected_user)
            is_password_match = (login_pass == expected_pass)
            is_credential_valid = (is_username_match and is_password_match)
            is_rhythm_within_range = (min_allowed_speed <= inferred_cadence <= max_allowed_speed)
            
            # STRATEGIC SEPARATION OF SYSTEM CHECKS
            if not is_credential_valid:
                st.error("🟥 **ACCESS LOCKED**")
                if not is_username_match:
                    st.warning(f"❌ User ID Handle Mismatch. Typed: '{login_user}', Target: '{expected_user}'")
                if not is_password_match:
                    st.warning("❌ Access Key Password String Mismatch.")
                st.status("⚠️ Threat Containment Status: **INVALID CREDENTIAL SIGNATURE**", state="error")
                
            elif not is_rhythm_within_range or z_score >= 1.5 or trust_percentage < 50.0:
                st.error("🟥 **ACCESS LOCKED**")
                st.warning(f"⚠️ Biometric Anomaly: Cadence profile failed range checks (Z-Score: {z_score:.2f}).")
                st.status("⚠️ Threat Containment Status: **BIOMETRIC SIGNATURE REJECTED**", state="error")
                
            else:
                st.success(f"🟩 **ACCESS GRANTED**\n\nBehavioral telemetry aligns cleanly. Session token issued for user: `{login_user}`.")
                st.status("🛡️ Core Firewall Status: **SECURE & OPERATIONAL**", state="complete")
                
        with col2:
            st.markdown("### 🔍 Real-Time Biometric Diagnostics")
            
            metrics_data = {
                "Biometric Parameter": ["Mean Cadence Interval", "Neuromuscular Variance Delta", "Biometric Deviation Model Profile"],
                "Enrolled Blueprint": [f"{baseline_speed:.3f} sec/key", f"{baseline_variance:.3f} sec (Allowed Var)", "100.00% Verification Rate"],
                "Live Access Attempt": [f"{inferred_cadence:.3f} sec/key", f"{abs(inferred_cadence - baseline_speed):.3f} sec", f"{trust_percentage:.2f}% Envelope Match"]
            }
            st.table(pd.DataFrame(metrics_data))
            st.progress(int(trust_percentage), text="Trust Envelope Confidence Gauge")

        if 'gate_start_time' in st.session_state: 
            del st.session_state['gate_start_time']
        # Conceptual execution flow:
# if access_granted:
#     from src.adaptive_learning import update_biometric_blueprint
#     update_biometric_blueprint(inferred_cadence)
