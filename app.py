import streamlit as st
import urllib.parse

# Configuración de la pantalla del smartphone
st.set_page_config(page_title="Te lo llevo", page_icon="🤝", layout="centered")

# --- TRADUCCIONES INTERFAZ (ESPAÑOL / FRANÇAIS) ---
IDIOMAS = {
    "Español 🇪🇸": {
        "title": "Te lo llevo – Je m'en occupe",
        "subtitle": "Guarda el tiempo para ti",
        "section_datos": "👤 Tus Datos / Vos Coordonnées",
        "placeholder_nombre": "Ej: María Gómez",
        "placeholder_tel": "Ej: +33 6 12 34 56 78",
        "label_nombre": "Tu Nombre y Apellido / Nom et Prénom",
        "label_tel": "Tu Teléfono de Contacto 📞 / Numéro de téléphone",
        "section_central": "📞 ¿A qué central deseas enviar tu solicitud? / Quelle ligne?",
        "label_central": "Selecciona una línea de atención / Ligne d'attention :",
        "btn_llamar": "📞 LLAMAR A LA CENTRAL (PEDIDO ESPECIAL)",
        "section_favor": "📝 ¿Qué favor o recado necesitas? / De quoi avez-vous besoin ?",
        "label_tipo": "Selecciona una opción / Sélectionnez une option :",
        "opciones_favor": [
            "🛒 Hacer la compra / Supermercado (Courses)",
            "📦 Recoger o enviar un paquete (Colis)",
            "💊 Ir a la farmacia (Pharmacie)",
            "📄 Gestiones, papeles o recados (Démarches)",
            "🛠️ Pequeña ayuda en el hogar (Bricolage / Aide)",
            "❓ Otro favor / Autre service"
        ],
        "label_detalles": "Explícanos los detalles de lo que necesitas / Détails :",
        "placeholder_detalles": "Ej: Necesito comprar pan, leche... / J'ai besoin de...",
        "label_dir": "📍 Dirección donde debemos ir / Adresse de livraison ou rendez-vous :",
        "placeholder_dir": "Ej: Rue de la République, Tarascon",
        "btn_enviar": "🚀 ENVIAR SOLICITUD A LA CENTRAL",
        "error_datos": "⚠️ Por favor, introduce tu nombre y teléfono de contacto.",
        "error_detalles": "⚠️ Por favor, dinos detalladamente qué necesitas y la dirección.",
        "alerta_lista": "✨ ¡Solicitud Lista / Demande Prête !",
        "alerta_desc": "Pulsa el botón de abajo para enviar el recado de forma inmediata a la central por WhatsApp.",
        "btn_whatsapp": "💬 ENVIAR A LA CENTRAL POR WHATSAPP",
        "encabezado_wa": "🔔 [TE LO LLEVO - NUEVA SOLICITUD]"
    },
    "Français 🇫🇷": {
        "title": "Te lo llevo – Je m'en occupe",
        "subtitle": "Votre temps est à vous",
        "section_datos": "👤 Vos Coordonnées",
        "placeholder_nombre": "Ex: Marie Dubois",
        "placeholder_tel": "Ex: +33 6 12 34 56 78",
        "label_nombre": "Nom et Prénom",
        "label_tel": "Numéro de téléphone 📞",
        "section_central": "📞 Ligne de la centrale d'appels",
        "label_central": "Sélectionnez une ligne d'attention :",
        "btn_llamar": "📞 APPELER LA CENTRALE (DEMANDE SPÉCIALE)",
        "section_favor": "📝 De quoi avez-vous besoin aujourd'hui ?",
        "label_tipo": "Sélectionnez une option :",
        "opciones_favor": [
            "🛒 Faire les courses / Supermarché",
            "📦 Récupérer ou envoyer un colis",
            "💊 Aller à la pharmacie",
            "📄 Démarches administratives / Courses",
            "🛠️ Petite aide à la maison / Bricolage",
            "❓ Autre service (À préciser ci-dessous)"
        ],
        "label_detalles": "Expliquez-nous les détails de votre demande :",
        "placeholder_detalles": "Ex: J'ai besoin d'acheter du pain, du lait...",
        "label_dir": "📍 Adresse de livraison o rendez-vous :",
        "placeholder_dir": "Ex: Rue de la République, Tarascon",
        "btn_enviar": "🚀 ENVOYER LA DEMANDE À LA CENTRALE",
        "error_datos": "⚠️ Veuillez entrer votre nom et votre numéro de téléphone.",
        "error_detalles": "⚠️ Veuillez préciser les détails de votre demande et l'adresse.",
        "alerta_lista": "✨ Demande Prête !",
        "alerta_desc": "Cliquez sur le bouton ci-dessous pour envoyer immédiatement votre demande à la centrale via WhatsApp.",
        "btn_whatsapp": "💬 ENVOYER À LA CENTRALE VIA WHATSAPP",
        "encabezado_wa": "🔔 [TE LO LLEVO - NOUVELLE DEMANDE]"
    }
}

# Estilos CSS Móvil
st.markdown("""
    <style>
    .main .block-container { 
        max-width: 400px; 
        padding-top: 1.5rem; 
        background-color: #fdfdfd; 
        border-radius: 24px; 
        box-shadow: 0 8px 24px rgba(0,0,0,0.12); 
    }
    .stButton>button { 
        width: 100%; 
        border-radius: 14px; 
        height: 3.2em; 
        font-weight: bold; 
        background-color: #6d28d9 !important; 
        color: white !important; 
        border: none; 
    }
    .brand-title { 
        text-align: center; 
        color: #1e293b; 
        font-family: 'Arial Black', sans-serif; 
        font-size: 1.55em; 
        margin-bottom: 0px; 
    }
    .brand-subtitle { 
        text-align: center; 
        color: #6d28d9; 
        font-weight: bold; 
        margin-top: 4px; 
        font-size: 1.05em; 
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica de la app bilingüe
idioma_seleccionado = st.selectbox("🌐 Idioma / Langue", list(IDIOMAS.keys()))
textos = IDIOMAS[idioma_seleccionado]

CENTRALES = {"Central Principal 1": "33745378520", "Central de Apoyo 2": "33745442538"}

st.markdown(f"<h1 class='brand-title'>{textos['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='brand-subtitle'>{textos['subtitle']}</p>", unsafe_allow_html=True)
st.divider()

st.markdown(f"### {textos['section_datos']}")
nombre_cliente = st.text_input(textos['label_nombre'], placeholder=textos['placeholder_nombre'])
telefono_cliente = st.text_input(textos['label_tel'], placeholder=textos['placeholder_tel'])

st.divider()
st.markdown(f"### {textos['section_central']}")
opcion_central = st.selectbox(textos['label_central'], list(CENTRALES.keys()))
telefono_destino = CENTRALES[opcion_central]

st.write("")
st.markdown(f"""
    <a href="tel:+{telefono_destino}">
        <button style="width:100%; background-color:#dc2626; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.05em; cursor:pointer;">
            {textos['btn_llamar']}
        </button>
    </a>
""", unsafe_allow_html=True)

st.divider()
st.markdown(f"### {textos['section_favor']}")
tipo_favor = st.selectbox(textos['label_tipo'], textos['opciones_favor'])
detalles_favor = st.text_area(textos['label_detalles'], placeholder=textos['placeholder_detalles'])
direccion_favor = st.text_input(textos['label_dir'], placeholder=textos['placeholder_dir'])

if st.button(textos['btn_enviar']):
    if not nombre_cliente.strip() or not telefono_cliente.strip():
        st.error(textos['error_datos'])
    elif not detalles_favor.strip() or not direccion_favor.strip():
        st.error(textos['error_detalles'])
    else:
        texto_base = f"{textos['encabezado_wa']}\n\n👤 Client(e): {nombre_cliente}\n📞 Tel: {telefono_cliente}\n📋 Cat: {tipo_favor}\n📝 Details: {detalles_favor}\n📍 Adresse: {direccion_favor}"
        url_whatsapp = f"https://wa.me/{telefono_destino}?text={urllib.parse.quote(texto_base)}"
        
        st.markdown(f"""
            <div style='background-color: #f5f3ff; padding: 15px; border-radius: 16px; border-left: 6px solid #6d28d9;'>
                <h4 style='color: #5b21b6; margin: 0;'>{textos['alerta_lista']}</h4>
                <p style='color: #5b21b6; margin: 6px 0 0 0;'>{textos['alerta_desc']}</p>
            </div>
            <a href="{url_whatsapp}" target="_blank">
                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                    {textos['btn_whatsapp']}
                </button>
            </a>
        """, unsafe_allow_html=True)
