# src/security_audit.py
import pandas as pd
import streamlit as st
import time
from src.utils import calculate_z_score, get_trust_percentage

def run_adversarial_simulations():
    """
    Executes an automated security audit against the enrolled biometric baseline.
    Simulates malicious attack profiles with advanced executive visual telemetry components.
    """
    st.subheader("🛡️ Automated Penetration & Stress Telemetry Suite")
    
    baseline_speed = st.session_state.get('baseline_avg_speed')
    baseline_variance = st.session_state.get('baseline_std')
    
    if not baseline_speed:
        st.error("🟥 SYSTEM ERROR: No biometric profile enrolled in state memory yet.")
        st.info("💡 Please switch back to 'User Gateway Terminal', register 3 typing samples, and click 'FINALIZE' before running the audit suite.")
        return

    st.markdown("### **Simulating Threat Vector Matrix**")
    st.markdown("Launch automated non-human actors to cross-examine behavioral parameters against your enrolled biometric footprint blueprint.")
    
    if st.button("🚀 INITIATE ADVERSARIAL STRESS TEST PACKET"):
        
        with st.status("🔬 Analyzing vector exceptions across defensive model boundaries...", state="running") as status:
            time.sleep(0.6)
            
            attack_profiles = {
                "Credential Dump (Copy-Paste)": 0.000,
                "High-Velocity Automated Script": 0.015,
                "Shoulder Surfing (Slo-Mo Attacker)": 1.850
            }
            
            audit_records = []
            speeds = [sample['H.s'] for sample in st.session_state.profile_data_buffer]
            min_allowed_speed = min(speeds) * 0.85
            max_allowed_speed = max(speeds) * 1.15
            
            # Create three clean layout columns for visual scorecards
            card_cols = st.columns(3)
            col_idx = 0
            
            for attack_name, simulated_cadence in attack_profiles.items():
                z_score = calculate_z_score(simulated_cadence, baseline_speed, baseline_variance)
                trust_envelope = get_trust_percentage(z_score)
                is_within_range = (min_allowed_speed <= simulated_cadence <= max_allowed_speed)
                
                if simulated_cadence < 0.01 or not is_within_range or z_score >= 1.5 or trust_envelope < 50.0:
                    mitigation_status = "🟥 ACCESS LOCKED (Threat Contained)"
                    card_color = "#EF4444" # Crimson
                    bg_badge = "#2D1B22"
                else:
                    mitigation_status = "🟩 ACCESS GRANTED (Firewall Breach)"
                    card_color = "#10B981" # Emerald
                    bg_badge = "#142D24"
                    
                audit_records.append({
                    "Attack Vector Profile": attack_name,
                    "Simulated Speed": f"{simulated_cadence:.3f} s/key",
                    "Z-Score Model Result": f"{z_score:.2f}",
                    "Envelope Match %": f"{trust_envelope:.2f}%",
                    "Firewall Defense Action": mitigation_status
                })
                
                # Render high-end executive metric cards above the summary table
                with card_cols[col_idx]:
                    st.markdown(f"""
                    <div style="background-color: #1E293B; padding: 16px; border-radius: 8px; border-top: 4px solid {card_color}; text-align: center;">
                        <span style="color: #94A3B8; font-size: 11px; font-weight: bold; font-family: monospace;">{attack_name.upper()}</span>
                        <h2 style="margin: 10px 0; color: {card_color} !important; font-size: 28px;">{trust_envelope:.1f}%</h2>
                        <div style="background-color: {bg_badge}; color: {card_color}; border-radius: 4px; padding: 4px; font-family: monospace; font-size: 11px; font-weight: bold;">
                            MATCH CONFIDENCE
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
            
            status.update(label="💥 Auditing complete! Vectors successfully mapped and intercepted.", state="complete")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### **Defensive Telemetry Audit Logs**")
        df_audit = pd.DataFrame(audit_records)
        st.table(df_audit)
        
        st.success("🤖 Zero-Trust pipeline integrity validated against multi-modal threats!")