import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simplified Deuterium-Tritium fusion model
# Based on approximate reaction rate formula and energy balance

E_REACTION = 17.6e6 * 1.602e-19  # J per D-T fusion reaction

# compute fusion power and related quantities

def dt_fusion_simulation(n, T_keV, volume, tau_E, time_steps=100):
    """Run a simple D-T fusion simulation.

    Parameters
    ----------
    n : float
        Plasma density in m^-3.
    T_keV : float
        Plasma temperature in keV.
    volume : float
        Plasma volume in m^3.
    tau_E : float
        Energy confinement time in seconds.
    time_steps : int
        Number of time steps for the output array.

    Returns
    -------
    energy_values : ndarray
        Cumulative fusion energy over time (Joules).
    p_fusion : float
        Instantaneous fusion power (Watts).
    p_heating : float
        Required heating power for given parameters (Watts).
    q_ratio : float
        Ratio of fusion power to heating power (Q).
    """
    # very rough cross-section approximation (m^3/s)
    sigma_v = 1e-22 * (T_keV**2) * np.exp(-19.94 / T_keV)
    reaction_rate = 0.25 * n**2 * sigma_v * volume
    p_fusion = reaction_rate * E_REACTION

    # Heating power needed to maintain temperature (simplified)
    # Convert T_keV to Joules per particle
    thermal_energy = n * T_keV * 1e3 * 1.602e-19 * volume
    p_heating = thermal_energy / tau_E

    q_ratio = p_fusion / p_heating if p_heating > 0 else 0.0

    times = np.linspace(0, tau_E, time_steps)
    energy_values = p_fusion * times
    return energy_values, p_fusion, p_heating, q_ratio


st.title("UN-EX Fusion Real Model")

n = st.slider('Plasma Density (m^-3)', 1e19, 1e22, 1e20)
T_keV = st.slider('Temperature (keV)', 1.0, 25.0, 10.0)
volume = st.slider('Plasma Volume (m^3)', 10.0, 500.0, 100.0)
tau_E = st.slider('Confinement Time (s)', 0.1, 5.0, 1.0)

energy_values, p_fusion, p_heating, q_ratio = dt_fusion_simulation(
    n, T_keV, volume, tau_E
)

st.subheader("Energy over Time")
fig, ax = plt.subplots()
ax.plot(energy_values)
ax.set_xlabel("Time Step")
ax.set_ylabel("Fusion Energy (J)")
st.pyplot(fig)

results = pd.DataFrame({
    "Fusion Power (W)": [p_fusion],
    "Heating Power (W)": [p_heating],
    "Q Ratio": [q_ratio],
    "nTtau (keV s / m^3)": [n * T_keV * tau_E]
})

st.subheader("Simulation Results")
st.dataframe(results)

csv = results.to_csv(index=False)
st.download_button("Download Results", csv, "fusion_results.csv", "text/csv")
