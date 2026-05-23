import streamlit as st
import urllib.parse
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

# Inicializar el buscador de direcciones (OpenStreetMap)
@st.cache_resource
def obtener_geolocalizador():
    return Nominatim(user_agent="muevete_papa_lucho_local")

geolocator = obtener_geolocalizador()

# --- FUNCIONES PARA GUARDADO PERMANENTE EN ARCHIVO ---
ARCH_CONDUCTORES = "conductores.txt"

def cargar_conductores_fijos():
    conductores = []
    if os.path.exists(ARCH_CONDUCTORES):
        with open(ARCH_CONDUCTORES, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 3:
                    conductores.append({
                        "nombre": partes[0],
                        "estado": partes[1],
                        "telefono": partes[2]
                    })
    return conductores

def guardar_conductores_fijos(conductores):
    with open(ARCH_CONDUCTORES, "w", encoding="utf-8") as f:
        for c in conductores:
            f.write(f"{c['nombre']}|{c['estado']}|{c['telefono']}\n")

# --- INICIALIZACIÓN DE DATOS ---
if 'historial_viajes' not in st.session_state: 
    st.session_state.historial_viajes = []

# Cargamos los conductores desde el archivo permanente
if 'conductores' not in st.session_state:
    st.session_state.conductores = cargar_conductores_fijos()

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
    elif not st.session_state.conductores:
        st.error("⚠️ No hay conductores registrados en el sistema en este momento.")
    else:
        libres = [c for c in st.session_state.conductores if c["estado"] == "🟢 Disponible"]
        
        if libres:
            conductor_asignado = libres[0]
            conductor_asignado["estado"] = "🟡 Viaje Asignado"
            
            # Guardamos el cambio de estado en el archivo permanente
            guardar_conductores_fijos(st.session_state.conductores)
            
            dir_origen_corta = origen_final.split(",")[0]
            dir_destino_corta = destino_final.split(",")[0]
            
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Origen": dir_origen_corta,
                "Destino": dir_destino_corta,
                "Conductor": conductor_assigned_name := conductor_asignado["nombre"]
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            texto_base = f"Hola {conductor_assigned_name}, necesito un viaje desde {dir_origen_corta} hasta {dir_destino_corta}."
            texto_codificado = urllib.parse.quote(texto_base)
            url_whatsapp = f"https://wa.me/{conductor_asignado['telefono']}?text={texto_codificado}"
            
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Solicitud Procesada!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>Conductor asignado: <b>{conductor_assigned_name}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("🤝 Pulsa el botón de abajo para hablar con tu conductor y acordar el precio.")
            
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 ACORDAR PRECIO CON {conductor_assigned_name.upper()}
                    </button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("Todos los conductores están ocupados en este momento. Inténtalo de nuevo en unos minutos.")

# --- PANEL CENTRAL DE ADMINISTRACIÓN ---
st.write("")
with st.expander("⚙️ Consola interna de Papá Lucho"):
    st.subheader("➕ Registrar Nuevo Conductor")
    with st.form("nuevo_chofer_form", clear_on_submit=True):
        c_nombre = st.text_input("Nombre del Conductor")
        c_telefono = st.text_input("WhatsApp (ej: 33612345678)")
        enviar_registro = st.form_submit_button("💾 Guardar Conductor")
        if enviar_registro:
            if c_nombre.strip() and c_telefono.strip():
                nuevo_c = {"nombre": c_nombre, "estado": "🟢 Disponible", "telefono": c_telefono.strip().replace("+", "")}
                st.session_state.conductores.append(nuevo_c)
                
                # NUEVO: Guardamos inmediatamente en el disco duro del servidor
                guardar_conductores_fijos(st.session_state.conductores)
                st.success(f"¡Conductor {c_nombre} guardado permanentemente!")
                st.rerun()

    st.divider()
    st.subheader("🚗 Gestión y Control de la Flota")
    
    if st.session_state.conductores:
        for idx, c in enumerate(st.session_state.conductores):
            col_datos, col_ini, col_fin, col_borrar = st.columns([1.8, 1.1, 1.1, 1.0])
            
            with col_datos:
                st.write(f"*{c['nombre']}*\n\n`{c['estado']}`")
            
            with col_ini:
                if c["estado"] == "🟡 Viaje Asignado":
                    if st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}_{idx}"):
                        c["estado"] = "🔴 En viaje"
                        guardar_conductores_fijos(st.session_state.conductores)
                        st.rerun()
                else:
                    st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}_{idx}", disabled=True)
                    
            with col_fin:
                if c["estado"] == "🔴 En viaje":
                    if st.button(f"🟢 Fin", key=f"fin_{c['nombre']}_{idx}"):
                        c["estado"] = "🟢 Disponible"
                        guardar_conductores_fijos(st.session_state.conductores)
                        st.rerun()
                else:
                    st.button(f"🟢 Fin", key=f"fin_{c['nombre']}_{idx}", disabled=True)
            
            with col_borrar:
                if st.button(f"🗑️ Borrar", key=f"del_{c['nombre']}_{idx}"):
                    st.session_state.conductores.pop(idx)
                    # Guardamos los cambios tras eliminar
                    guardar_conductores_fijos(st.session_state.conductores)
                    st.rerun()
    else:
        st.write("No hay conductores registrados todavía.")
                
    st.divider()
    st.subheader("📋 Registro de Solicitudes")
    if st.session_state.historial_viajes:
        st.table(st.session_state.historial_viajes)
    else:
        st.write("No hay solicitudes registradas en esta sesión.")
        
    if st.button("🔄 Reiniciar Jornada (Liberar Todos)"):
        for c in st.session_state.conductores: c["estado"] = "🟢 Disponible"
        guardar_conductores_fijos(st.session_state.conductores)
        st.session_state.historial_viajes = []
        st.rerun()
