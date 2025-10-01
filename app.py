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

# --- Záložky ---
tab1, tab2 = st.tabs(["📊 Graf", "ℹ️ Informace"])

with tab1:
    st.subheader("Vykreslení bodů na kružnici")
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
    st.pyplot(fig)

with tab2:
    st.subheader("👤 O mně")
    st.markdown(
        f"""
**{AUTHOR_NAME}** – student Fakulty informačních technologií VUT v Brně.  
Zajímám se o praktické využití matematiky v programování, zejména o vizualizaci dat a jednoduché
geometrické úlohy v Pythonu. Baví mě stavět malé, ale čisté aplikace, které mají jasný účel a
dobře se ovládají. Ve volném čase se zlepšuji v Pythonu, verzovacích systémech a nasazování
projektů do cloudu.  
**Kontakt:** {AUTHOR_EMAIL}
"""
    )

    st.markdown(
        """
### 🧰 Použité technologie (stručně, ale věcně)
- **Python** – hlavní jazyk aplikace. Díky bohatému ekosystému knihoven se hodí na rychlý vývoj prototypů i seriózní projekty.  
- **Streamlit** – framework pro tvorbu interaktivních webových aplikací v Pythonu bez potřeby psát HTML/JS. Umožňuje snadný **deploy** a sdílení.  
- **NumPy** – efektivní práce s poli a vektory; v aplikaci slouží k výpočtu souřadnic bodů na kružnici pomocí funkcí `cos`/`sin`.  
- **Matplotlib** – vykreslení grafu, os a zvýraznění bodů/středu/kružnice; jednoduchá a stabilní knihovna pro 2D grafy.  
- **fpdf2** – generování **PDF** přímo v aplikaci; s TTF fontem (DejaVu Sans) bez problémů zvládá češtinu.  
- **GitHub** – hostování kódu, verzování a snadná integrace se Streamlit Cloudem pro veřejnou demonstraci aplikace.
"""
    )

# --- Export do PDF (Unicode-safe) ---
st.subheader("📄 Export do PDF")

def build_pdf() -> BytesIO:
    pdf = FPDF()
    pdf.add_page()

    # Důležité: přidat Unicode font (TTF) – vyžaduje fpdf2
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(
            f"Nenalezen font '{FONT_PATH}'. Přidej prosím TTF soubor (např. DejaVuSans.ttf) do složky 'assets/'."
        )
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=14)

    # Nadpis
    pdf.cell(0, 10, "Report – Body na kružnici", ln=True, align="C")
    pdf.ln(4)

    # O autorovi (plný popis)
    pdf.set_font("DejaVu", size=11)
    pdf.multi_cell(
        0, 7,
        f"{AUTHOR_NAME} – student Fakulty informačních technologií VUT v Brně.\n"
        "Zajímám se o praktické využití matematiky v programování, zejména o vizualizaci dat a "
        "geometrické úlohy v Pythonu. Baví mě stavět malé, ale čisté aplikace s jasným účelem.\n"
        f"Kontakt: {AUTHOR_EMAIL}"
    )
    pdf.ln(2)

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
    pdf.ln(2)

    # Technologie – trochu podrobněji
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 8, "Použité technologie:", ln=True)
    pdf.set_font("DejaVu", size=11)
    pdf.multi_cell(
        0, 7,
        "- Python – univerzální skriptovací jazyk s velkou komunitou a balíčky.\n"
        "- Streamlit – rychlá tvorba interaktivních webových aplikací v Pythonu.\n"
        "- NumPy – výpočty s poli a vektory; výpočet souřadnic bodů po kružnici.\n"
        "- Matplotlib – vykreslení grafu (body, střed, kružnice) a os s jednotkami.\n"
        "- fpdf2 – generování PDF s podporou Unicode při použití TTF fontu.\n"
        "- GitHub – verzování a sdílení kódu; snadný deploy přes Streamlit Cloud."
    )

    # Výstup do paměti
    buffer = BytesIO()
    pdf.output(buffer)          # fpdf2 umí zapisovat přímo do file-like objektu
    buffer.seek(0)
    return buffer

if st.button("Vytvořit PDF"):
    try:
        pdf_buffer = build_pdf()
        st.download_button(
            label="⬇️ Stáhnout PDF",
            data=pdf_buffer,
            file_name="report.pdf",
            mime="application/pdf"
        )
        st.success("PDF bylo vygenerováno.")
    except Exception as e:
        st.error(f"Nepodařilo se vytvořit PDF: {e}")
