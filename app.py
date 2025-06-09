
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="UN-EX Fusion - Live Smart Mode", layout="wide")
st.title("🔁 UN-EX Fusion Live Tuning Simulator")

# Constants
a = 1.0
delta = 0.01

# UI
col1, col2 = st.columns(2)
with col1:
    st.header("⚙️ Base Plasma Settings")
    T = st.slider("Temperature (keV)", 1.0, 20.0, 5.0)
    B = st.slider("Magnetic Field (T)", 1.0, 10.0, 3.0)
    S_local = st.slider("Local Entropy", 0.1, 10.0, 1.0)

with col2:
    st.header("🎯 Smart Tuning Controls")
    run_tuning = st.toggle("Run Smart Mode (live loop)", value=False)
    pause = st.toggle("Pause Loop", value=False)
    steps = st.slider("Sweep Depth", 5, 25, 10)
    show_plot = st.checkbox("Show Q Ratio Sweep Graph", value=True)

placeholder = st.empty()
log = []

# Smart loop runner
if run_tuning and not pause:
    best_q = 0
    best_params = {}
    q_series = []

    for E_harm in np.linspace(10, 100, steps):
        for alpha in np.linspace(0.5, 3.5, steps):
            for beta in np.linspace(0.5, 2.0, steps):
                i = alpha * (E_harm / (S_local + delta)) ** beta
                D = T / (B * i)
                tau_E = a**2 / D
                tau_bohm = a**2 * B / T
                Q_ratio = tau_E / tau_bohm
                q_series.append(Q_ratio)
                if Q_ratio > best_q:
                    best_q = Q_ratio
                    best_params = {
                        "E_harm": round(E_harm, 3),
                        "Alpha": round(alpha, 3),
                        "Beta": round(beta, 3),
                        "Q_ratio": round(Q_ratio, 3),
                        "Tau_E": round(tau_E, 3)
                    }

    log.append(best_params)
    placeholder.success(f"🔥 Max Q Ratio: {best_q:.2f}x (Best config logged)")
    if show_plot:
        fig, ax = plt.subplots()
        ax.plot(q_series, color='lime')
        ax.set_title("Q Ratio Sweep (Smart Loop)")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Q Ratio")
        st.pyplot(fig)

    # Save best to CSV if needed
    df = pd.DataFrame(log)
    df.to_csv("live_best_log.csv", index=False)
