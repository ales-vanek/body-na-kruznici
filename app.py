import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Body na kružnici", layout="wide")

st.title("📐 Body na kružnici – Webová aplikace")

# --- Vstupy od uživatele ---
st.sidebar.header("Nastavení parametrů")

x0 = st.sidebar.number_input("Souřadnice středu X:", value=0.0)
y0 = st.sidebar.number_input("Souřadnice středu Y:", value=0.0)
r = st.sidebar.number_input("Poloměr kružnice:", value=5.0, min_value=0.1)
n = st.sidebar.number_input("Počet bodů na kružnici:", value=8, min_value=1, step=1)
barva = st.sidebar.color_picker("Vyber barvu bodů:", "#ff0000")

# --- Výpočet souřadnic bodů ---
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
x = x0 + r * np.cos(theta)
y = y0 + r * np.sin(theta)

# --- Vykreslení ---
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.scatter(x, y, c=barva, s=100, label="Body na kružnici")
ax.add_patch(plt.Circle((x0, y0), r, fill=False, linestyle="--", color="gray"))
ax.plot(x0, y0, "bo", label="Střed")

# Osy s čísly a jednotkami
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(0, color="black", linewidth=0.5)
ax.legend()

st.pyplot(fig)

# --- Informace o vás a technologiích ---
st.subheader("👤 Informace o autorovi")
jmeno = st.text_input("Vaše jméno:", "Jan Novák")
kontakt = st.text_input("Kontakt (e-mail):", "novak@example.com")
technologie = ["Python", "Streamlit", "Matplotlib", "FPDF", "GitHub"]
st.write("Použité technologie:", ", ".join(technologie))

# --- Export do PDF ---
if st.button("📄 Vygenerovat PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Report – Body na kružnici", ln=True, align="C")

    pdf.cell(200, 10, txt=f"Autor: {jmeno}", ln=True)
    pdf.cell(200, 10, txt=f"Kontakt: {kontakt}", ln=True)
    pdf.cell(200, 10, txt=f"Střed: ({x0}, {y0})", ln=True)
    pdf.cell(200, 10, txt=f"Poloměr: {r}", ln=True)
    pdf.cell(200, 10, txt=f"Počet bodů: {n}", ln=True)
    pdf.cell(200, 10, txt=f"Barva bodů: {barva}", ln=True)

    # Uložení PDF do dočasného souboru
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)

    with open(tmp_file.name, "rb") as f:
        st.download_button("⬇️ Stáhnout PDF", f, file_name="report.pdf")

    os.remove(tmp_file.name)

# --- GitHub info ---
st.subheader("🌐 GitHub")
st.markdown(
    """
    - Pokud ještě nemáš účet, vytvoř si ho na [GitHub.com](https://github.com/)  
    - Nahraj zdrojový kód této aplikace do svého repozitáře  
    - Odkaz na aplikaci (pokud ji nasadíš přes [Streamlit Cloud](https://streamlit.io/cloud)) vlož sem do odevzdání  
    """
)
