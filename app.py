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

# Inicializar el buscador de direcciones gratuito (OpenStreetMap)
geolocator = Nominatim(user_agent="muevete_papa_lucho_app")

# --- INICIALIZACIÓN DE DATOS EN MEMORIA ---
if 'historial_viajes' not in st.session_state: 
    st.session_state.historial_viajes = []

if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Jean", "estado": "🟢 Disponible", "telefono": "33612345678"},
        {"nombre": "Marie", "estado": "🟢 Disponible", "telefono": "33687654321"}
    ]

# --- INTERFAZ VISTA PASAJERO ---
st.markdown("<h1 class='brand-title'>🚕 ¡Muévete!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>con papá lucho</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Datos del Pasajero")
nombre_pasajero = st.text_input("Tu Nombre y Apellido", placeholder="Ej: Juan Pérez")
telefono_pasajero = st.text_input("Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 🗺️ ¿A dónde nos movemos hoy?")

# --- BUSCADOR ASISTIDO DE DIRECCIÓN INICIAL ---
origen_input = st.text_input("📍 Punto de recogida (Escribe y presiona Enter para buscar)", placeholder="Ej: Gare de Tarascon")
origen_seleccionado = "No seleccionado"
if origen_input:
    try:
        # Busca en tiempo real las direcciones que coincidan en la región
        locations = geolocator.geocode(origen_input, exactly_one=False, limit=3, country_codes="fr")
        if locations:
            opciones_origen = [loc.address for loc in locations]
            origen_seleccionado = st.selectbox("🎯 Confirma tu ubicación exacta encontrada:", opciones_origen)
        else:
            st.warning("🔍 No encontramos esa dirección exacta, pero puedes continuar.")
            origen_seleccionado = origen_input
    except:
        origen_seleccionado = origen_input

# --- BUSCADOR ASISTIDO DE DESTINO FINAL ---
destino_input = st.text_input("🏁 ¿A qué dirección vas? (Escribe y presiona Enter)", placeholder="Ej: Mairie de Beaucaire")
destino_seleccionado = "No seleccionado"
if destino_input:
    try:
        locations_dest = geolocator.geocode(destino_input, exactly_one=False, limit=3, country_codes="fr")
        if locations_dest:
            opciones_destino = [loc.address for loc in locations_dest]
            destino_seleccionado = st.selectbox("🎯 Confirma tu destino exacto encontrado:", opciones_destino)
        else:
            st.warning("🔍 No encontramos la dirección exacta, pero puedes continuar.")
            destino_seleccionado = destino_input
    except:
        destino_seleccionado = destino_input

st.write("") 

if st.button("🚀 SOLICITAR VIAJE NOW"):
    if not nombre_pasajero.strip() or not telefono_pasajero.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif origen_seleccionado == "No seleccionado" or destino_seleccionado == "No seleccionado":
        st.error("⚠️ Por favor, introduce y confirma el origen y el destino.")
    else:
        # Filtrar conductores que estén totalmente libres
        libres = [c for c in st.session_state.conductores if c["estado"] == "🟢 Disponible"]
        
        if libres:
            conductor_asignado = libres[0]
            # El conductor cambia automáticamente a estado "Solicitado"
            conductor_asignado["estado"] = "🟡 Viaje Asignado"
            
            # Guardar registro de la carrera en la base central
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Origen": origen_seleccionado.split(",")[0], # Guarda el nombre corto del lugar
                "Destino": destino_seleccionado.split(",")[0],
                "Conductor": conductor_asignado["nombre"],
                "Estado Carrera": "Asignado"
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            # WhatsApp abre con los datos resumidos para el acuerdo rápido
            texto_base = f"Hola {conductor_asignado['nombre']}, necesito un viaje desde {origen_seleccionado.split(',')[0]} hasta {destino_seleccionado.split(',')[0]}."
            texto_codificado = urllib.parse.quote(texto_base)
            url_whatsapp = f"https://wa.me/{conductor_asignado['telefono']}?text={texto_codificado}"
            
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Solicitud Procesada!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>Conductor asignado: <b>{conductor_asignado['nombre']}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("🤝 Pulsa abajo para abrir WhatsApp, el conductor te dará el precio de inmediato.")
            
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 ACORDAR PRECIO CON {conductor_asignado['nombre'].upper()}
                    </button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("Todos los conductores están ocupados en este momento. Inténtalo de nuevo en unos minutos.")

# --- PANEL CENTRAL DE ADMINISTRACIÓN Y CONTROL DE CONDUCTORES ---
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
                st.success(f"¡Conductor {c_nombre} integrado!")
                st.rerun()

    st.divider()
    
    # SECCIÓN CRÍTICA: BOTONES DE INICIAR Y FINALIZAR VIAJE PARA EL CONDUCTOR
    st.subheader("🚗 Control de Viajes en Tiempo Real")
    for c in st.session_state.conductores:
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        
        with col1:
            st.write(f"*{c['nombre']}* ({c['estado']})")
        
        with col2:
            # Botón para iniciar el viaje físico
            if c["estado"] == "🟡 Viaje Asignado":
                if st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}"):
                    c["estado"] = "🔴 En viaje"
                    st.rerun()
            else:
                st.button(f"🏁 Iniciar", key=f"ini_{c['nombre']}", disabled=True)
                
        with col3:
            # Botón para finalizar el viaje y quedar libre otra vez
            if c["estado"] == "🔴 En viaje":
                if st.button(f"🟢 Finalizar", key=f"fin_{c['nombre']}"):
                    c["estado"] = "🟢 Disponible"
                    st.rerun()
            else:
                st.button(f"🟢 Finalizar", key=f"fin_{c['nombre']}", disabled=True)
                
    st.divider()
    st.subheader("📋 Historial General de Solicitudes")
    if st.session_state.historial_viajes:
        st.table(st.session_state.historial_viajes)
    else:
        st.write("No hay solicitudes registradas.")
        
    if st.button("🔄 Reiniciar Toda la Jornada"):
        for c in st.session_state.conductores: c["estado"] = "🟢 Disponible"
        st.session_state.historial_viajes = []
        st.rerun()
