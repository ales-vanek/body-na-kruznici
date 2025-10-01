import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Body na kružnici", layout="wide")

st.title("📐 Body na kružnici – Webová aplikace")

# --- Postranní menu pro vstupy ---
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

# --- Záložky ---
tab1, tab2 = st.tabs(["📊 Graf", "ℹ️ Informace"])

with tab1:
    st.subheader("Vykreslení bodů na kružnici")
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.scatter(x, y, c=barva, s=100, label="Body na kružnici")
    ax.add_patch(plt.Circle((x0, y0), r, fill=False, linestyle="--", color="gray"))
    ax.plot(x0, y0, "bo", label="Střed")

    # Osy
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("👤 Informace o autorovi")
    st.markdown("""
    **Jméno:** Aleš Vaněk  
    **Status:** Student Fakulty stavební, VUT v Brně  
    **E-mail:** 278507@vutbr.cz

    ### Použité technologie:
    - **Python** – hlavní programovací jazyk  
    - **Streamlit** – jednoduchý framework pro webové aplikace v Pythonu  
    - **Matplotlib** – knihovna pro kreslení grafů  
    - **NumPy** – práce s maticemi a výpočty (souřadnice bodů)  
    - **FPDF** – generování PDF souborů  
    - **GitHub** – správa verzí a sdílení zdrojového kódu  
    """)

# --- Export do PDF ---
st.subheader("📄 Export do PDF")

if st.button("Vytvořit PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Report – Body na kružnici", ln=True, align="C")
    pdf.ln(10)

    # Informace o autorovi
    pdf.cell(200, 10, txt="Autor: Aleš Vaněk", ln=True)
    pdf.cell(200, 10, txt="Status: Jsem studentem FAST VUT v Brně. Pocházím z menší obce jižně od Znojma a toto je můj pokus o webou aplikaci.", ln=True)
    pdf.cell(200, 10, txt="E-mail: 278507@vutbr.cz", ln=True)
    pdf.ln(10)

    # Parametry úlohy
    pdf.cell(200, 10, txt=f"Střed: ({x0}, {y0})", ln=True)
    pdf.cell(200, 10, txt=f"Poloměr: {r}", ln=True)
    pdf.cell(200, 10, txt=f"Počet bodů: {n}", ln=True)
    pdf.cell(200, 10, txt=f"Barva bodů: {barva}", ln=True)
    pdf.ln(10)

    # Info o technologiích
    pdf.cell(200, 10, txt="Použité technologie:", ln=True)
    pdf.multi_cell(0, 10, 
        "- Python – hlavní jazyk\n"
        "- Streamlit – web aplikace\n"
        "- Matplotlib – grafy\n"
        "- NumPy – výpočty\n"
        "- FPDF – export PDF\n"
        "- GitHub – správa verzí"
    )

    # Uložení do paměti
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="⬇️ Stáhnout PDF",
        data=pdf_buffer,
        file_name="report.pdf",
        mime="application/pdf"
    )
