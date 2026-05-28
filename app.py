import streamlit as st
import urllib.parse

# Configuración de la pantalla del smartphone
st.set_page_config(page_title="Aleska ¡Ayúdame con esto!", page_icon="🤝", layout="centered")

# Estilos de diseño móvil personalizados (Color Morado/Magenta para la central de Aleska)
st.markdown("""
    <style>
    .main .block-container {
        max-width: 400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #fdfdfd;
        border-radius: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 3.2em;
        font-weight: bold;
        background-color: #7c3aed !important; /* Morado moderno y profesional */
        color: white !important;
        border: none;
    }
    .brand-title {
        text-align: center;
        color: #1e293b;
        font-family: 'Arial Black', sans-serif;
        margin-bottom: 0px;
    }
    .brand-subtitle {
        text-align: center;
        color: #7c3aed;
        font-weight: bold;
        margin-top: 0px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LOS NÚMEROS DE LA CENTRAL ---
CENTRALES = {
    "Central Princpal 1": "33745378520",
    "Central de Apoyo 2": "33745442538"
}

# --- INTERFAZ VISTA CLIENTE ---
st.markdown("<h1 class='brand-title'>🤝 Aleska</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>¡Ayúdame con esto!</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Tus Datos")
nombre_cliente = st.text_input("Tu Nombre y Apellido", placeholder="Ej: María Gómez")
telefono_cliente = st.text_input("Tu Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 📞 ¿A qué central deseas enviar tu solicitud?")
opcion_central = st.selectbox("Selecciona una línea de atención:", list(CENTRALES.keys()))
telefono_destino = CENTRALES[opcion_central]

st.divider()
st.markdown("### 📝 ¿Qué favor o recado necesitas?")

tipo_favor = st.selectbox(
    "Selecciona una opción:",
    [
        "🛒 Hacer la compra / Supermercado",
        "📦 Recoger o enviar un paquete",
        "💊 Ir a la farmacia",
        "📄 Gestiones, papeles o recados",
        "🛠️ Pequeña ayuda en el hogar",
        "❓ Otro favor (Escríbelo abajo)"
    ]
)

detalles_favor = st.text_area(
    "Explícanos los detalles de lo que necesitas:", 
    placeholder="Ej: Necesito comprar pan, leche y manzanas en el súper..."
)

direccion_favor = st.text_input("📍 Dirección donde debemos ir / entregarlo", placeholder="Ej: Rue de la République, Tarascon")

st.write("") 

if st.button("🚀 ENVIAR SOLICITUD A LA CENTRAL"):
    if not nombre_cliente.strip() or not telefono_cliente.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif not detalles_favor.strip() or not direccion_favor.strip():
        st.error("⚠️ Por favor, dinos detalladamente qué necesitas y la dirección.")
    else:
        # Formatear el mensaje de WhatsApp que recibirá la central seleccionada
        texto_base = f"¡Hola! Nueva solicitud de asistencia ingresada por la app:\n\n" \
                     f"👤 Cliente: {nombre_cliente}\n" \
                     f"📞 Contacto: {telefono_cliente}\n" \
                     f"📋 Tipo: {tipo_favor}\n" \
                     f"📝 Detalles: {detalles_favor}\n" \
                     f"📍 Dirección: {direccion_favor}"
                     
        texto_codificado = urllib.parse.quote(texto_base)
        url_whatsapp = f"https://wa.me/{telefono_destino}?text={texto_codificado}"
        
        st.markdown(f"""
            <div style='background-color: #f5f3ff; padding: 18px; border-radius: 16px; border-left: 6px solid #7c3aed; margin-bottom: 15px;'>
                <h4 style='color: #5b21b6; margin: 0;'>✨ ¡Solicitud Lista!</h4>
                <p style='color: #5b21b6; margin: 6px 0 0 0;'>Pulsa el botón de abajo para enviar el reporte de forma inmediata a la <b>{opcion_central}</b>.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <a href="{url_whatsapp}" target="_blank">
                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                    💬 ENVIAR A LA CENTRAL POR WHATSAPP
                </button>
            </a>
        """, unsafe_allow_html=True)
