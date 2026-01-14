# Spirometrie-simulator met klinische flow-volume weergave
# Run met: streamlit run spirometrie_simulator.py

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Spirometrie Simulator", layout="centered")

st.title("🫁 Spirometrie Simulator (klinische weergave)")
st.write("Flow-volume-loop met voorspelde waarden, normaalgebied en gemeten curve – vergelijkbaar met klinische spirometrie-uitdraai.")

# --- Presets ---
presets = {
    "Gezond": {"FVC": 5.0, "PEF": 8.0, "tau": 2.0},
    "COPD": {"FVC": 4.5, "PEF": 4.0, "tau": 1.0},
    "Astma (obstructief)": {"FVC": 5.0, "PEF": 5.0, "tau": 1.3},
    "Restrictief": {"FVC": 3.0, "PEF": 7.0, "tau": 2.5},
}

preset_name = st.selectbox("Kies patroon", presets.keys())
preset = presets[preset_name]

st.subheader("Instelbare parameters (gemeten)")
FVC = st.slider("FVC (L)", 1.5, 7.0, preset["FVC"], 0.1)
PEF = st.slider("PEF (L/s)", 1.0, 12.0, preset["PEF"], 0.1)
tau = st.slider("Expiratoire tijdconstante", 0.5, 4.0, preset["tau"], 0.1)

st.subheader("Voorspelde waarden")
FVC_pred = st.slider("Voorspelde FVC (L)", 2.0, 7.0, 5.0, 0.1)
PEF_pred = st.slider("Voorspelde PEF (L/s)", 3.0, 12.0, 8.0, 0.1)

# --- Simulatie ---
time = np.linspace(0, 6, 600)
volume_meas = FVC * np.exp(-time / tau)
flow_meas = PEF * np.exp(-time) * (volume_meas / FVC)

volume_pred = FVC_pred * np.exp(-time / 2.0)
flow_pred = PEF_pred * np.exp(-time) * (volume_pred / FVC_pred)

# Normaalgebied (80–120%)
flow_upper = 1.2 * flow_pred
flow_lower = 0.8 * flow_pred

# FEV1
idx_1s = np.argmin(np.abs(time - 1.0))
FEV1 = FVC - volume_meas[idx_1s]
ratio = FEV1 / FVC

# --- Plot ---
fig, ax = plt.subplots()

# Normaalgebied
ax.fill_between(volume_pred, flow_lower, flow_upper, alpha=0.3, label="Normaalgebied")

# Voorspeld
ax.plot(volume_pred, flow_pred, linestyle="--", label="Voorspeld")

# Gemeten
ax.plot(volume_meas, flow_meas, linewidth=2, label="Gemeten")

ax.invert_xaxis()
ax.set_xlabel("Volume (L)")
ax.set_ylabel("Flow (L/s)")
ax.set_title("Flow–Volume Loop")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# --- Tabel zoals spirometrie-uitdraai ---
st.subheader("Resultaten")
st.table({
    "Parameter": ["FVC", "FEV1", "FEV1/FVC"],
    "Gemeten": [f"{FVC:.2f} L", f"{FEV1:.2f} L", f"{ratio:.2f}"],
    "% voorspeld": [f"{100*FVC/FVC_pred:.0f}%", "–", "–"],
})

st.caption("Educatieve simulatie – visuele overeenkomst met klinische spirometrie, geen echte longfysiologie")
