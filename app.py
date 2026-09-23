import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# ---------- ESTILOS VISUALES ----------
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #f7f9ff 0%, #eef3ff 45%, #f8f5ff 100%);
        color: #172033;
    }

    /* Ocultar menú y footer nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedor principal */
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102a72 0%, #173f9f 100%);
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 12px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #123b9b 0%, #4b55d9 58%, #7a5ce6 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 24px;
        color: white;
        box-shadow: 0 18px 45px rgba(48, 70, 160, .22);
        margin-bottom: 1.8rem;
    }
    .hero h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        letter-spacing: -.04em;
    }
    .hero p {
        color: rgba(255,255,255,.88);
        font-size: 1.05rem;
        margin: .65rem 0 0;
    }
    .badge {
        display: inline-block;
        padding: .35rem .75rem;
        border-radius: 999px;
        background: rgba(255,255,255,.15);
        border: 1px solid rgba(255,255,255,.22);
        font-size: .82rem;
        margin-bottom: .8rem;
    }

    /* Tarjetas */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px;
        border: 1px solid #e5e9f4;
        background: rgba(255,255,255,.82);
        box-shadow: 0 8px 28px rgba(32, 48, 90, .07);
    }

    /* Títulos */
    h2, h3 {
        color: #172a63;
        letter-spacing: -.02em;
    }

    /* Área de texto */
    textarea {
        border-radius: 16px !important;
        border: 1px solid #d9e0f2 !important;
        background: white !important;
        box-shadow: inset 0 1px 3px rgba(30,45,90,.04);
    }
    textarea:focus {
        border-color: #4b63db !important;
        box-shadow: 0 0 0 3px rgba(75,99,219,.12) !important;
    }

    /* Botones */
    .stButton > button {
        width: 100%;
        border: 0;
        border-radius: 13px;
        padding: .72rem 1rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(135deg, #3159d8, #654dd7);
        box-shadow: 0 8px 18px rgba(69, 82, 190, .22);
        transition: all .2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(69, 82, 190, .28);
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid #e7eaf3;
    }

    /* Expander */
    details {
        background: rgba(255,255,255,.78);
        border: 1px solid #e3e7f2 !important;
        border-radius: 15px !important;
    }

    /* File uploader */
    section[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #b9c5e8;
        border-radius: 18px;
        background: rgba(255,255,255,.7);
    }

    /* Separadores */
    hr {
        border: none;
        border-top: 1px solid #dde3f1;
        margin: 1.5rem 0;
    }

    .section-caption {
        color: #68738f;
        font-size: .92rem;
        margin-top: -.45rem;
        margin-bottom: 1rem;
    }

    .footer-custom {
        text-align: center;
        color: #7b849b;
        font-size: .85rem;
        padding: 1.5rem 0 .5rem;
    }
</style>
""")

st.markdown("""
<div class="hero">
    <div class="badge">✦ ANÁLISIS DE LENGUAJE</div>
    <h1>📝 Analizador de Texto</h1>
    <p>Descubre el sentimiento, la subjetividad y las palabras que más destacan en tu texto.</p>
</div>
""")


st.markdown("""
<div class="section-caption">
    Analiza textos en español mediante traducción al inglés y procesamiento con TextBlob.
    Explora sentimiento, subjetividad, frecuencia de palabras y frases detectadas.
</div>
""")

# Barra lateral
st.sidebar.markdown("## ✦ Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# Función para contar palabras sin depender de NLTK
def contar_palabras(texto):
    # Lista básica de palabras vacías en español e inglés
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
        # Inglés
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
        "we'd", "we'll", "we're", "we've", "were",         "weren't", "what", "what's", "when", 
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", 
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])
    
    # Limpiar y tokenizar texto
    palabras = re.findall(r'\b\w+\b', texto.lower())
    
    # Filtrar palabras vacías y contar frecuencias
    palabras_filtradas = [palabra for palabra in palabras 
                         if palabra not in stop_words and len(palabra) > 2]
    
    # Contar frecuencias
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    # Ordenar por frecuencia
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    
    return contador_ordenado, palabras_filtradas

# Inicializar el traductor
translator = Translator()

# Función para traducir texto del español al inglés
def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto  # Devolver el texto original si falla la traducción

# Función para procesar el texto con TextBlob (versión con traducción)
def procesar_texto(texto):
    # Guardar el texto original
    texto_original = texto
    
    # Traducir el texto al inglés para mejor análisis
    texto_ingles = traducir_texto(texto)
    
    # Analizar el texto traducido con TextBlob
    blob = TextBlob(texto_ingles)
    
    # Análisis de sentimiento (esto no requiere corpus adicionales)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Extraer frases de manera simplificada (del texto original)
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    
    # Extraer frases del texto traducido
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    
    # Combinar frases originales y traducidas
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
    
    # Contar palabras con nuestra función simplificada (en el texto traducido)
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

# Función para crear visualizaciones usando componentes nativos de Streamlit
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    # Visualización de sentimiento y subjetividad con barras de progreso de Streamlit
    with col1:
        st.subheader("💭 Sentimiento y subjetividad")
        
        # Normalizar valores para mostrarlos en barras de progreso
        # Sentimiento va de -1 a 1, lo normalizamos a 0-1 para la barra
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        
        st.write("**Sentimiento:**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
        
        # Subjetividad ya está en el rango 0-1
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes usando chart de Streamlit
    with col2:
        st.subheader("🔎 Palabras más frecuentes")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)
    
    # Mostrar texto traducido
    st.subheader("🌐 Texto traducido")
    with st.expander("Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Texto Original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Texto Traducido (Inglés):**")
            st.text(resultados["texto_traducido"])
    
    # Análisis de frases
    st.subheader("💬 Frases detectadas")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity
                
                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "😟"
                else:
                    emoji = "😐"
                
                st.write(f"{i}. {emoji} **Original:** *\"{frase_original}\"*")
                st.write(f"   **Traducción:** *\"{frase_traducida}\"* (Sentimiento: {sentimiento:.2f})")
                st.write("---")
            except:
                st.write(f"{i}. **Original:** *\"{frase_original}\"*")
                st.write(f"   **Traducción:** *\"{frase_traducida}\"*")
                st.write("---")
    else:
        st.write("No se detectaron frases.")

# Lógica principal según el modo seleccionado
if modo == "Texto directo":
    st.subheader("Ingresa tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")
    
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando texto..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor, ingresa algún texto para analizar.")

elif modo == "Archivo de texto":
    st.subheader("📂 Carga un archivo")
    st.markdown('<div class="section-caption">Admite archivos .txt, .csv y .md.</div>', unsafe_allow_html=True)
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("Ver contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            
            if st.button("Analizar archivo"):
                with st.spinner("Analizando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

# Información adicional
with st.expander("📚 Información sobre el análisis"):
    st.markdown("""
    ### Sobre el análisis de texto
    
    - **Sentimiento**: Varía de -1 (muy negativo) a 1 (muy positivo)
    - **Subjetividad**: Varía de 0 (muy objetivo) a 1 (muy subjetivo)
    
    ### Requisitos mínimos
    
    Esta aplicación utiliza únicamente:
    ```
    streamlit
    textblob
    pandas
    ```
    """)

# Pie de página
st.markdown("---")
st.markdown('<div class="footer-custom">Hecho con ❤️ usando Streamlit, TextBlob y Google Translate</div>', unsafe_allow_html=True)
