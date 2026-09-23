import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Analizador de Texto",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS VISUALES
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =========================
   FONDO GENERAL
   ========================= */

.stApp {
    background: #f5f7fc;
}

.main {
    background: #f5f7fc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* =========================
   OCULTAR ELEMENTOS STREAMLIT
   ========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* =========================
   SIDEBAR
   ========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a72 0%, #172f79 100%);
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.2rem;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 8px;
}

.sidebar-description {
    font-size: 13px;
    line-height: 1.6;
    color: #dce5ff !important;
    margin-bottom: 25px;
}

/* =========================
   HERO
   ========================= */

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        135deg,
        #123c9b 0%,
        #315bd7 48%,
        #6854dc 100%
    );
    border-radius: 26px;
    padding: 42px 45px;
    margin-bottom: 25px;
    box-shadow: 0 18px 40px rgba(32, 62, 145, 0.20);
}

.hero::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    right: -80px;
    top: -100px;
}

.hero::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
    right: 130px;
    bottom: -110px;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-label {
    color: #dce7ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    color: white;
    font-size: 43px;
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
}

.hero-description {
    color: #edf2ff;
    font-size: 16px;
    line-height: 1.6;
    max-width: 700px;
    margin-top: 13px;
}

/* =========================
   INTRO
   ========================= */

.intro {
    background: white;
    border: 1px solid #e3e8f3;
    border-radius: 18px;
    padding: 18px 22px;
    margin-bottom: 28px;
    color: #5f6c86;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 5px 18px rgba(30, 47, 90, 0.04);
}

/* =========================
   TÍTULOS
   ========================= */

h1, h2, h3 {
    color: #193477 !important;
    font-weight: 800 !important;
}

h2 {
    margin-top: 25px !important;
}

h3 {
    margin-top: 20px !important;
}

/* =========================
   TEXT AREA
   ========================= */

.stTextArea textarea {
    background: white !important;
    color: #172033 !important;
    border: 2px solid #dce3f2 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    box-shadow: 0 5px 18px rgba(30, 47, 90, 0.04) !important;
    transition: all 0.2s ease !important;
}

.stTextArea textarea:hover {
    border-color: #b8c6ea !important;
}

.stTextArea textarea:focus {
    border-color: #4968d8 !important;
    box-shadow: 0 0 0 3px rgba(73,104,216,0.12) !important;
}

/* =========================
   BOTONES
   ========================= */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border: none !important;
    border-radius: 14px !important;
    background: linear-gradient(
        135deg,
        #315bd7,
        #6854dc
    ) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    box-shadow: 0 9px 20px rgba(69,82,190,0.20) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 13px 25px rgba(69,82,190,0.28) !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* =========================
   FILE UPLOADER
   ========================= */

section[data-testid="stFileUploaderDropzone"] {
    background: white !important;
    border: 2px dashed #b8c6ea !important;
    border-radius: 18px !important;
    padding: 20px !important;
}

section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #4968d8 !important;
    background: #fafbff !important;
}

section[data-testid="stFileUploaderDropzone"] * {
    color: #4c5870 !important;
}

/* =========================
   EXPANDERS
   ========================= */

div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid #e1e6f1 !important;
    border-radius: 16px !important;
    overflow: hidden;
    box-shadow: 0 5px 18px rgba(30,47,90,0.04);
}

div[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #263b70 !important;
}

/* =========================
   ALERTAS
   ========================= */

div[data-testid="stAlert"] {
    border-radius: 14px !important;
}

/* =========================
   PROGRESS BAR
   ========================= */

div[data-testid="stProgress"] {
    margin-top: 7px;
    margin-bottom: 12px;
}

div[data-testid="stProgress"] > div {
    border-radius: 50px !important;
}

div[data-testid="stProgress"] > div > div {
    border-radius: 50px !important;
}

/* =========================
   TARJETAS
   ========================= */

.card {
    background: white;
    border: 1px solid #e1e6f1;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 7px 22px rgba(32,48,90,0.06);
    height: 100%;
}

.card-title {
    color: #193477;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 18px;
}

.card-subtitle {
    color: #7a849a;
    font-size: 13px;
    margin-top: -12px;
    margin-bottom: 20px;
}

/* =========================
   MÉTRICAS
   ========================= */

.metric-card {
    background: white;
    border: 1px solid #e1e6f1;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 7px 22px rgba(32,48,90,0.05);
}

.metric-icon {
    font-size: 25px;
    margin-bottom: 5px;
}

.metric-label {
    color: #748099;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #193477;
    font-size: 27px;
    font-weight: 800;
    margin-top: 4px;
}

/* =========================
   FRASES
   ========================= */

.phrase-card {
    background: white;
    border: 1px solid #e2e7f2;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 5px 15px rgba(30,47,90,0.04);
}

.phrase-number {
    color: #536bd8;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 7px;
}

.phrase-original {
    color: #24314d;
    font-size: 15px;
    line-height: 1.5;
}

.phrase-translation {
    color: #768198;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 7px;
}

/* =========================
   TEXTO TRADUCIDO
   ========================= */

.translation-box {
    background: #f7f9ff;
    border: 1px solid #e1e7f5;
    border-radius: 14px;
    padding: 17px;
    color: #35415b;
    line-height: 1.6;
    min-height: 100px;
}

/* =========================
   CAPTION
   ========================= */

.section-caption {
    color: #6d7892;
    font-size: 14px;
    line-height: 1.5;
    margin-top: -8px;
    margin-bottom: 15px;
}

/* =========================
   DIVISOR
   ========================= */

hr {
    border: none !important;
    border-top: 1px solid #e0e5ef !important;
    margin: 35px 0 !important;
}

/* =========================
   FOOTER
   ========================= */

.footer-custom {
    text-align: center;
    color: #8791a5;
    font-size: 13px;
    padding: 20px 0 5px;
}

/* =========================
   TABLA / DATAFRAME
   ========================= */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* =========================
   RESPONSIVE
   ========================= */

@media (max-width: 768px) {

    .hero {
        padding: 30px 25px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-description {
        font-size: 14px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-label">✦ ANÁLISIS DE LENGUAJE</div>
        <div class="hero-title">📝 Analizador de Texto</div>
        <div class="hero-description">
            Descubre el sentimiento, la subjetividad y las palabras
            que más destacan en tu texto.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="intro">
    Analiza textos en español mediante traducción al inglés y procesamiento
    con <b>TextBlob</b>. Explora sentimiento, subjetividad, frecuencia de
    palabras y frases detectadas.
</div>
""", unsafe_allow_html=True)


# ============================================================
# BARRA LATERAL
# ============================================================

st.sidebar.markdown("""
<div class="sidebar-title">✦ Opciones</div>
<div class="sidebar-description">
Selecciona cómo quieres introducir el texto que deseas analizar.
</div>
""", unsafe_allow_html=True)

modo = st.sidebar.selectbox(
    "Modo de entrada",
    ["Texto directo", "Archivo de texto"]
)


# ============================================================
# FUNCIÓN PARA CONTAR PALABRAS
# ============================================================

def contar_palabras(texto):

    stop_words = set([
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os",
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que",
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin",
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo",
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti",
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos",
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras",
        "vuestro", "vuestros", "y", "ya", "yo",

        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not",
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll",
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])

    palabras = re.findall(r'\b\w+\b', texto.lower())

    palabras_filtradas = [
        palabra for palabra in palabras
        if palabra not in stop_words and len(palabra) > 2
    ]

    contador = {}

    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1

    contador_ordenado = dict(
        sorted(
            contador.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return contador_ordenado, palabras_filtradas


# ============================================================
# TRADUCTOR
# ============================================================

translator = Translator()


def traducir_texto(texto):

    try:
        traduccion = translator.translate(
            texto,
            src="es",
            dest="en"
        )

        return traduccion.text

    except Exception as e:

        st.error(f"Error al traducir: {e}")

        return texto


# ============================================================
# PROCESAMIENTO DEL TEXTO
# ============================================================

def procesar_texto(texto):

    texto_original = texto

    texto_ingles = traducir_texto(texto)

    blob = TextBlob(texto_ingles)

    sentimiento = blob.sentiment.polarity

    subjetividad = blob.sentiment.subjectivity

    frases_originales = [
        frase.strip()
        for frase in re.split(r'[.!?]+', texto_original)
        if frase.strip()
    ]

    frases_traducidas = [
        frase.strip()
        for frase in re.split(r'[.!?]+', texto_ingles)
        if frase.strip()
    ]

    frases_combinadas = []

    for i in range(
        min(
            len(frases_originales),
            len(frases_traducidas)
        )
    ):

        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })

    contador_palabras, palabras = contar_palabras(texto_ingles)

    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }


# ============================================================
# VISUALIZACIONES
# ============================================================

def crear_visualizaciones(resultados):

    st.markdown("## 📊 Resultados del análisis")

    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    sentimiento = resultados["sentimiento"]
    subjetividad = resultados["subjetividad"]

    if sentimiento > 0.05:
        sentimiento_label = "Positivo"
        sentimiento_emoji = "😊"
    elif sentimiento < -0.05:
        sentimiento_label = "Negativo"
        sentimiento_emoji = "😟"
    else:
        sentimiento_label = "Neutral"
        sentimiento_emoji = "😐"

    if subjetividad > 0.5:
        subjetividad_label = "Alta"
    else:
        subjetividad_label = "Baja"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{sentimiento_emoji}</div>
            <div class="metric-label">Sentimiento</div>
            <div class="metric-value">{sentimiento:.2f}</div>
            <div class="metric-label">{sentimiento_label}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💭</div>
            <div class="metric-label">Subjetividad</div>
            <div class="metric-value">{subjetividad:.2f}</div>
            <div class="metric-label">{subjetividad_label}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🔤</div>
            <div class="metric-label">Palabras analizadas</div>
            <div class="metric-value">{len(resultados["palabras"])}</div>
            <div class="metric-label">Palabras relevantes</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SENTIMIENTO + PALABRAS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card">
            <div class="card-title">
                💭 Sentimiento y subjetividad
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("**Sentimiento**")

        sentimiento_norm = (sentimiento + 1) / 2

        st.progress(sentimiento_norm)

        if sentimiento > 0.05:
            st.success(
                f"📈 Positivo ({sentimiento:.2f})"
            )

        elif sentimiento < -0.05:
            st.error(
                f"📉 Negativo ({sentimiento:.2f})"
            )

        else:
            st.info(
                f"📊 Neutral ({sentimiento:.2f})"
            )

        st.write("**Subjetividad**")

        st.progress(subjetividad)

        if subjetividad > 0.5:
            st.warning(
                f"💭 Alta subjetividad ({subjetividad:.2f})"
            )
        else:
            st.info(
                f"📋 Baja subjetividad ({subjetividad:.2f})"
            )

    with col2:

        st.markdown("""
        <div class="card">
            <div class="card-title">
                🔎 Palabras más frecuentes
            </div>
            <div class="card-subtitle">
                Palabras relevantes encontradas en el texto
            </div>
        """, unsafe_allow_html=True)

        if resultados["contador_palabras"]:

            palabras_top = dict(
                list(
                    resultados["contador_palabras"].items()
                )[:10]
            )

            df_palabras = pd.DataFrame(
                {
                    "Palabra": list(palabras_top.keys()),
                    "Frecuencia": list(palabras_top.values())
                }
            )

            st.bar_chart(
                df_palabras.set_index("Palabra")
            )

        else:
            st.info("No se encontraron palabras relevantes.")

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # TEXTO ORIGINAL Y TRADUCIDO
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🌐 Traducción")

    with st.expander("Ver texto original y traducción"):

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🇪🇸 Español")

            st.markdown(
                f"""
                <div class="translation-box">
                    {resultados["texto_original"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown("### 🇺🇸 Inglés")

            st.markdown(
                f"""
                <div class="translation-box">
                    {resultados["texto_traducido"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # FRASES
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 💬 Frases detectadas")

    if resultados["frases"]:

        for i, frase_dict in enumerate(
            resultados["frases"][:10],
            1
        ):

            frase_original = frase_dict["original"]

            frase_traducida = frase_dict["traducido"]

            try:

                blob_frase = TextBlob(
                    frase_traducida
                )

                sentimiento_frase = (
                    blob_frase.sentiment.polarity
                )

                if sentimiento_frase > 0.05:
                    emoji = "😊"
                    estado = "Positivo"

                elif sentimiento_frase < -0.05:
                    emoji = "😟"
                    estado = "Negativo"

                else:
                    emoji = "😐"
                    estado = "Neutral"

                st.markdown(
                    f"""
                    <div class="phrase-card">

                        <div class="phrase-number">
                            {emoji} FRASE {i} · {estado}
                        </div>

                        <div class="phrase-original">
                            <b>Original:</b>
                            "{frase_original}"
                        </div>

                        <div class="phrase-translation">
                            <b>Traducción:</b>
                            "{frase_traducida}"
                            · Sentimiento: {sentimiento_frase:.2f}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception:

                st.markdown(
                    f"""
                    <div class="phrase-card">

                        <div class="phrase-number">
                            💬 FRASE {i}
                        </div>

                        <div class="phrase-original">
                            <b>Original:</b>
                            "{frase_original}"
                        </div>

                        <div class="phrase-translation">
                            <b>Traducción:</b>
                            "{frase_traducida}"
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("No se detectaron frases.")


# ============================================================
# MODO: TEXTO DIRECTO
# ============================================================

if modo == "Texto directo":

    st.markdown("## ✏️ Escribe tu texto")

    st.markdown(
        """
        <div class="section-caption">
            Introduce el texto que deseas analizar. Puedes escribir
            varias frases o pegar un texto completo.
        </div>
        """,
        unsafe_allow_html=True
    )

    texto = st.text_area(
        "Texto",
        height=220,
        placeholder="Escribe o pega aquí el texto que deseas analizar...",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Analizar texto"):

        if texto.strip():

            with st.spinner("Analizando texto..."):

                resultados = procesar_texto(texto)

                crear_visualizaciones(resultados)

        else:

            st.warning(
                "Por favor, ingresa algún texto para analizar."
            )


# ============================================================
# MODO: ARCHIVO
# ============================================================

elif modo == "Archivo de texto":

    st.markdown("## 📂 Carga tu archivo")

    st.markdown(
        """
        <div class="section-caption">
            Admite archivos <b>.txt</b>, <b>.csv</b> y <b>.md</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    archivo = st.file_uploader(
        "Selecciona un archivo",
        type=["txt", "csv", "md"]
    )

    if archivo is not None:

        try:

            contenido = archivo.getvalue().decode("utf-8")

            with st.expander("👁️ Vista previa del archivo"):

                st.text(
                    contenido[:1000]
                    + (
                        "..."
                        if len(contenido) > 1000
                        else ""
                    )
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔍 Analizar archivo"):

                with st.spinner("Analizando archivo..."):

                    resultados = procesar_texto(
                        contenido
                    )

                    crear_visualizaciones(
                        resultados
                    )

        except Exception as e:

            st.error(
                f"Error al procesar el archivo: {e}"
            )


# ============================================================
# INFORMACIÓN
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📚 Información sobre el análisis"):

    st.markdown("""
    ### Sobre el análisis de texto

    **💭 Sentimiento**

    Varía de **-1 (muy negativo)** a **1 (muy positivo)**.

    **🧠 Subjetividad**

    Varía de **0 (muy objetivo)** a **1 (muy subjetivo)**.

    **🔎 Palabras frecuentes**

    Muestra las palabras relevantes que aparecen con mayor frecuencia
    después de eliminar palabras vacías.

    **🌐 Traducción**

    El texto en español se traduce al inglés para realizar el análisis
    mediante TextBlob.

    ### Requisitos

    Esta aplicación utiliza:

    - `streamlit`
    - `textblob`
    - `pandas`
    - `googletrans`
    - `re`
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer-custom">
        Hecho con ❤️ usando Streamlit, TextBlob y Google Translate
    </div>
    """,
    unsafe_allow_html=True
)
