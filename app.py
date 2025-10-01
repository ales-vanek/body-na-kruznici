import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF  # fpdf2
from io import BytesIO
import os

st.set_page_config(page_title="Body na kružnici", layout="wide")

# --- Autor / kontakt (pevné) ---
AUTHOR_NAME = "Aleš Vaněk"
AUTHOR_EMAIL = "ales.vanek@example.com"
AUTHOR_DESC = (
    f"{AUTHOR_NAME} – student Fakulty stavební VUT v Brně.\n"
    "Zajímám se o praktické využití matematiky a programování v inženýrské praxi. "
    "Rád kombinuji technické výpočty s vizualizacemi a učím se moderní nástroje "
    "pro sdílení a prezentaci výsledků."
)

# --- Cesta k TTF fontu (pro Unicode v PDF) ---
FONT_PATH = os.path.join("assets", "DejaVuSans.ttf")

st.title("📐 Body na kružnici – Webová aplikace")

# --- Postranní menu pro vstupy ---
st.sidebar.header("Nastavení parametrů")
x0 = st.sidebar.number_input("Souřadnice středu X:", value=0.0)
y0 = st.sidebar.number_input("Souřadnice středu Y:", value=0.0)
r = st.sidebar.number_input("Poloměr kružnice:", value=5.0, min_value=0.1)
n = st.sidebar.number_input("Počet bodů na kružnici:", value=8, min_value=1, step=1)
barva = st.sidebar.color_picker("Vyber barvu bodů:", "#ff0000")

# --- Výpočet souřadnic bodů ---
theta = np.linspace(0, 2*np.pi, int(n), endpoint=False)
x = x0 + r * np.cos(theta)
y = y0 + r * np.sin(theta)

# --- Funkce pro vytvoření grafu (abychom ho pak mohli dát i do PDF) ---
def create_plot():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.scatter(x, y, c=barva, s=100, label="Body na kružnici")
    ax.add_patch(plt.Circle((x0, y0), r, fill=False, linestyle="--", color="gray"))
    ax.plot(x0, y0, "bo", label="Střed")

    # Osy a popisky
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.legend()
    return fig

# --- Záložky ---
tab1, tab2 = st.tabs(["📊 Graf", "ℹ️ Informace"])

with tab1:
    st.subheader("Vykreslení bodů na kružnici")
    fig = create_plot()
    st.pyplot(fig)

with tab2:
    st.subheader("👤 O mně")
    st.markdown(
        f"""
**{AUTHOR_NAME}** – student Fakulty stavební VUT v Brně.  

Zajímám se o praktické využití matematiky a programování v inženýrské praxi.  
Rád kombinuji technické výpočty s vizualizacemi a učím se moderní nástroje pro sdílení a prezentaci výsledků.  

**Kontakt:** {AUTHOR_EMAIL}  
"""
    )

    st.markdown(
        """
### 🧰 Použité technologie
- **Python** – univerzální jazyk pro skripty, vědecké výpočty i aplikace.  
- **Streamlit** – framework pro tvorbu interaktivních webových aplikací v Pythonu, bez nutnosti psát HTML/JS.  
- **NumPy** – práce s poli a vektory; výpočet souřadnic bodů na kružnici.  
- **Matplotlib** – kreslení grafu, os a geometrických prvků.  
- **fpdf2** – generování PDF s podporou Unicode (při použití TTF fontu).  
- **GitHub** – správa verzí a sdílení kódu, integrace se Streamlit Cloudem.  
"""
    )

# --- Export do PDF (s vloženým grafem) ---
st.subheader("📄 Export do PDF")

def build_pdf(fig) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()

    # Přidání fontu (UTF-8)
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(
            f"Nenalezen font '{FONT_PATH}'. Přidej prosím TTF soubor (např. DejaVuSans.ttf) do složky 'assets/'."
        )
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=14)

    # Nadpis
    pdf.cell(0, 10, "Report – Body na kružnici", ln=True, align="C")
    pdf.ln(5)

    # O autorovi
    pdf.set_font("DejaVu", size=11)
    pdf.multi_cell(0, 7, AUTHOR_DESC)
    pdf.ln(5)
    pdf.cell(0, 7, f"Kontakt: {AUTHOR_EMAIL}", ln=True)
    pdf.ln(5)

    # Parametry úlohy
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 8, "Parametry:", ln=True)
    pdf.set_font("DejaVu", size=11)
    pdf.multi_cell(
        0, 7,
        f"- Střed: ({x0}, {y0})\n"
        f"- Poloměr: {r}\n"
        f"- Počet bodů: {int(n)}\n"
        f"- Barva bodů: {barva}"
    )
    pdf.ln(5)

    # Technologie
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 8, "Použité technologie:", ln=True)
    pdf.set_font("DejaVu", size=11)
    pdf.multi_cell(
        0, 7,
        "- Python – univerzální jazyk s velkým ekosystémem knihoven.\n"
        "- Streamlit – rychlý vývoj interaktivních web aplikací.\n"
        "- NumPy – výpočty a práce s poli.\n"
        "- Matplotlib – vizualizace a grafy.\n"
        "- fpdf2 – generování PDF s Unicode.\n"
        "- GitHub – verzování a nasazení aplikace."
    )
    pdf.ln(5)

    # Obrázek grafu
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    pdf.image(img_buffer, x=40, w=130)  # vložení obrázku doprostřed
    img_buffer.close()

    # Výstup do paměti
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

if st.button("Vytvořit PDF"):
    try:
        fig = create_plot()
        pdf_buffer = build_pdf(fig)
        st.download_button(
            label="⬇️ Stáhnout PDF",
            data=pdf_buffer,
            file_name="report.pdf",
            mime="application/pdf"
        )
        st.success("PDF bylo vygenerováno.")
    except Exception as e:
        st.error(f"Nepodařilo se vytvořit PDF: {e}")
