import streamlit as st
import urllib.parse
from geopy.geocoders import Nominatim

# Configuración de la pantalla del smartphone
st.set_page_config(page_title="Muévete con papá lucho", page_icon="🚕", layout="centered")

# Estilos de diseño móvil personalizados
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
        background-color: #f59e0b !important;
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
        color: #f59e0b;
        font-weight: bold;
        margin-top: 0px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar el buscador de direcciones (OpenStreetMap)
@st.cache_resource
def obtener_geolocalizador():
    return Nominatim(user_agent="muevete_papa_lucho_local")

geolocator = obtener_geolocalizador()

# --- CONDUCTORES FIJOS EN EL SISTEMA (NUNCA SE BORRAN) ---
if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Luis", "estado": "🟢 Disponible", "telefono": "33751865303"},
        {"nombre": "Filipe", "estado": "🟢 Disponible", "telefono": "33751865303"},
        {"nombre": "Christian", "estado": "🟢 Disponible", "telefono": "33745358520"}
    ]

if 'historial_viajes' not in st.session_state: 
    st.session_state.historial_viajes = []

# --- INTERFAZ VISTA PASAJERO ---
st.markdown("<h1 class='brand-title'>🚕 ¡Muévete!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>con papá lucho</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Datos del Pasajero")
nombre_pasajero = st.text_input("Tu Nombre y Apellido", placeholder="Ej: Juan Pérez")
telefono_pasajero = st.text_input("Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 🗺️ ¿A dónde nos movemos hoy?")

origen_input = st.text_input("📍 ¿Dónde te recogemos? (Escribe y presiona Enter)", placeholder="Ej: Gare de Tarascon")
origen_final = origen_input

if origen_input:
    try:
        ubicaciones = geolocator.geocode(origen_input, exactly_one=False, limit=3, country_codes="fr")
        if ubicaciones:
            lista_direcciones = [u.address for u in ubicaciones]
            origen_final = st.selectbox("🎯 Confirma la dirección exacta de recogida:", lista_direcciones)
    except:
        origen_final = origen_input

destino_input = st.text_input("🏁 ¿A qué dirección vas? (Escribe y presiona Enter)", placeholder="Ej: Chateau de Beaucaire")
destino_final = destino_input

if destino_input:
    try:
        ubicaciones_dest = geolocator.geocode(destino_input, exactly_one=False, limit=3, country_codes="fr")
        if ubicaciones_dest:
            lista_direcciones_dest = [u.address for u in ubicaciones_dest]
            destino_final = st.selectbox("🎯 Confirma tu destino exacto:", lista_direcciones_dest)
    except:
        destino_final = destino_input

st.write("") 

if st.button("🚀 SOLICITAR VIAJE NOW"):
    if not nombre_pasajero.strip() or not telefono_pasajero.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif not origen_final.strip() or not destino_final.strip():
        st.error("⚠️ Por favor, dinos el punto de recogida y el destino.")
    else:
        libres = [c for c in st.session_state.conductores if c["estado"] == "🟢 Disponible"]
        
        if libres:
            conductor_asignado = libres[0]
            conductor_asignado["estado"] = "🟡 Viaje Asignado"
            
            dir_origen_corta = origen_final.split(",")[0]
            dir_destino_corta = destino_final.split(",")[0]
            nombre_chofer = conductor_asignado["nombre"]
            
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Origen": dir_origen_corta,
                "Destino": dir_destino_corta,
                "Conductor": nombre_chofer
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            texto_base = f"Hola {nombre_chofer}, necesito un viaje desde {dir_origen_corta} hasta {dir_destino_corta}."
            texto_codificado = urllib.parse.quote(texto_base)
            url_whatsapp = f"https://wa.me/{conductor_asignado['telefono']}?text={texto_codificado}"
            
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Solicitud Procesada!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>Conductor asignado: <b>{nombre_chofer}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 ACORDAR PRECIO CON {nombre_chofer.upper()}
                    </button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("Todos los conductores están ocupados en este momento. Inténtalo de nuevo en unos minutos.")

# --- PANEL CENTRAL DE ADMINISTRACIÓN PROTEGIDO ---
st.write("")
with st.expander("⚙️ Consola interna de Papá Lucho"):
    clave_ingresada = st.text_input("🔑 Introduce la Clave de Administrador", type="password")
    
    if clave_ingresada == "lucho123":
        st.success("🔓 Acceso Concedido")
        st.divider()
        
        st.subheader("🚗 Gestión y Control de la Flota")
        
        for idx, c in enumerate(st.session_state.conductores):
            col_datos, col_ini, col_fin = st.columns([2.0, 1.5, 1.5])
            
            with col_datos:
                st.write(f"*{c['nombre']}*\n\n`{c['estado']}`")
            
            with col_ini:
                if c["estado"] == "🟡 Viaje Asignado":
                    if st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}_{idx}"):
                        st.session_state.conductores[idx]["estado"] = "🔴 En viaje"
                        st.rerun()
                else:
                    st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}_{idx}", disabled=True)
                    
            with col_fin:
                if c["estado"] == "🔴 En viaje":
                    if st.button(f"🟢 Fin", key=f"fin_{c['nombre']}_{idx}"):
                        st.session_state.conductores[idx]["estado"] = "🟢 Disponible"
                        st.rerun()
                else:
                    st.button(f"🟢 Fin", key=f"fin_{c['nombre']}_{idx}", disabled=True)
                    
        st.divider()
        st.subheader("📋 Registro de Solicitudes")
        if st.session_state.historial_viajes:
            st.table(st.session_state.historial_viajes)
        else:
            st.write("No hay solicitudes registradas en tu sesión actual.")
            
        if st.button("🔄 Reiniciar Jornada (Liberar Todos)"):
            for c in st.session_state.conductores: 
                c["estado"] = "🟢 Disponible"
            st.session_state.historial_viajes = []
            st.rerun()
            
    elif clave_ingresada != "":
        st.error("🔒 Clave incorrecta. Solo los administradores pueden gestionar la flota.")
