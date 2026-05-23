import streamlit as st
import urllib.parse
import json
import os
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

# Inicializar el buscador de direcciones
@st.cache_resource
def obtener_geolocalizador():
    return Nominatim(user_agent="muevete_papa_lucho_local")

geolocator = obtener_geolocalizador()

# --- BASE DE DATOS COMPARTIDA EN ARCHIVO LOCAL ---
DB_FILE = "estado_flota.json"

def cargar_flota_global():
    # Conductores fijos con los números reales corregidos por Christian
    flota_defecto = [
        {"nombre": "Luis", "estado": "⚪ Fuera de Servicio", "telefono": "33751865303"},
        {"nombre": "Filipe", "estado": "⚪ Fuera de Servicio", "telefono": "33651883295"},
        {"nombre": "Christian", "estado": "⚪ Fuera de Servicio", "telefono": "33745378520"}
    ]
    if not os.path.exists(DB_FILE):
        guardar_flota_global(flota_defecto)
        return flota_defecto
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return flota_defecto

def guardar_flota_global(flota):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(flota, f, ensure_ascii=False, indent=4)

# Carga de datos actualizada
conductores_actuales = cargar_flota_global()

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

origen_input = st.text_input("📍 ¿Dónde te recogemos?", placeholder="Ej: Gare de Tarascon")
origen_final = origen_input

if origen_input:
    try:
        ubicaciones = geolocator.geocode(origen_input, exactly_one=False, limit=3, country_codes="fr")
        if ubicaciones:
            lista_direcciones = [u.address for u in ubicaciones]
            origen_final = st.selectbox("🎯 Confirma recogida exacta:", lista_direcciones)
    except:
        origen_final = origen_input

destino_input = st.text_input("🏁 ¿A qué dirección vas?", placeholder="Ej: Chateau de Beaucaire")
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
        st.error("⚠️ Por favor, introduce tu nombre y teléfono.")
    elif not origen_final.strip() or not destino_final.strip():
        st.error("⚠️ Por favor, dinos el punto de recogida y el destino.")
    else:
        # Busca el primer conductor en verde ("🟢 Disponible")
        libres = [c for c in conductores_actuales if c["estado"] == "🟢 Disponible"]
        
        if libres:
            conductor_asignado = libres[0]
            
            # Cambiar estado en la base de datos compartida
            for c in conductores_actuales:
                if c["nombre"] == conductor_asignado["nombre"]:
                    c["estado"] = "🟡 Viaje Asignado"
            guardar_flota_global(conductores_actuales)
            
            dir_origen_corta = origen_final.split(",")[0]
            dir_destino_corta = destino_final.split(",")[0]
            nombre_chofer = conductor_asignado["nombre"]
            
            registro_viaje = {
                "Pasajero": nombre_pasajero,
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
            st.warning("🛏️ En este momento todos los conductores están ocupados o fuera de servicio. Inténtalo de nuevo en unos minutos.")

# --- CONSOLA DE TRABAJO PARA CONDUCTORES Y ADMIN ---
st.write("")
with st.expander("⚙️ Panel de Conductores / Administración"):
    clave_ingresada = st.text_input("🔑 Introduce tu Clave de Acceso", type="password")
    
    if clave_ingresada == "lucho123":
        st.success("🔓 Modo Operador Activo")
        st.divider()
        st.subheader("💼 Control de Tu Estado de Trabajo")
        st.info("Usa estos botones para avisar al sistema si estás despierto para trabajar o si te vas a descansar.")
        
        for idx, c in enumerate(conductores_actuales):
            st.markdown(f"🔹 Conductor: *{c['nombre']}* | Estado actual: {c['estado']}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🟢 Conectarme", key=f"conect_{c['nombre']}_{idx}"):
                    conductores_actuales[idx]["estado"] = "🟢 Disponible"
                    guardar_flota_global(conductores_actuales)
                    st.rerun()
            with col2:
                if c["estado"] == "🟡 Viaje Asignado":
                    if st.button("🏁 Iniciar Viaje", key=f"viaje_{c['nombre']}_{idx}"):
                        conductores_actuales[idx]["estado"] = "🔴 En viaje"
                        guardar_flota_global(conductores_actuales)
                        st.rerun()
                elif c["estado"] == "🔴 En viaje":
                    if st.button("✅ Terminar Viaje", key=f"fin_{c['nombre']}_{idx}"):
                        conductores_actuales[idx]["estado"] = "🟢 Disponible"
                        guardar_flota_global(conductores_actuales)
                        st.rerun()
                else:
                    st.button("🚗 Cambiar Viaje", key=f"dis_{c['nombre']}_{idx}", disabled=True)
            with col3:
                if st.button("⚪ Desconectarme", key=f"desc_{c['nombre']}_{idx}"):
                    conductores_actuales[idx]["estado"] = "⚪ Fuera de Servicio"
                    guardar_flota_global(conductores_actuales)
                    st.rerun()
            st.divider()
            
        st.subheader("📋 Registro de Solicitudes de la Sesión")
        if st.session_state.historial_viajes:
            st.table(st.session_state.historial_viajes)
        else:
            st.write("No hay solicitudes registradas en esta ventana.")
            
        if st.button("🔄 Reiniciar Todos a Fuera de Servicio"):
            for c in conductores_actuales:
                c["estado"] = "⚪ Fuera de Servicio"
            guardar_flota_global(conductores_actuales)
            st.session_state.historial_viajes = []
            st.rerun()
            
    elif clave_ingresada != "":
        st.error("🔒 Clave incorrecta. Solo el equipo de Papá Lucho tiene acceso.")
