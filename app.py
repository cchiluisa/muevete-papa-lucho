import streamlit as st
import urllib.parse

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

# --- INICIALIZACIÓN DE DATOS EN MEMORIA ---
if 'historial_viajes' not in st.session_state: 
    st.session_state.historial_viajes = []

if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Jean", "disponible": True, "telefono": "33612345678"},
        {"nombre": "Marie", "disponible": True, "telefono": "33687654321"}
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
origen = st.text_input("📍 ¿Dónde te recogemos?", placeholder="Ej: Calle, Plaza, Estación...")
destino = st.text_input("🏁 ¿A qué dirección vas?", placeholder="Ej: Destino final")

st.write("") 

if st.button("🚀 SOLICITAR VIAJE NOW"):
    if not nombre_pasajero.strip() or not telefono_pasajero.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif not origen.strip() or not destino.strip():
        st.error("⚠️ Por favor, dinos el punto de recogida y el destino.")
    else:
        # Filtrar conductores libres
        libres = [c for c in st.session_state.conductores if c["disponible"]]
        
        if libres:
            # Asignar al primero que esté libre
            conductor_asignado = libres[0]
            conductor_asignado["disponible"] = False  # Cambia a OCUPADO
            
            # Guardar registro simple en el panel de control
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Origen": origen,
                "Destino": destino,
                "Conductor": conductor_asignado["nombre"]
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            # WhatsApp abre con un saludo básico
            texto_base = f"Hola {conductor_asignado['nombre']}, necesito un viaje con Papá Lucho."
            texto_codificado = urllib.parse.quote(texto_base)
            url_whatsapp = f"https://wa.me/{conductor_asignado['telefono']}?text={texto_codificado}"
            
            # CORRECCIÓN AQUÍ: Evitamos la asignación inline que rompió la app
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Solicitud Procesada!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>Conductor asignado: <b>{conductor_asignado['nombre']}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("🤝 Pulsa el botón de abajo para hablar con tu conductor y acordar el precio del viaje.")
            
            # Botón directo de contacto
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 ACORDAR PRECIO CON {conductor_asignado['nombre'].upper()}
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
                nuevo_c = {"nombre": c_nombre, "disponible": True, "telefono": c_telefono.strip().replace("+", "")}
                st.session_state.conductores.append(nuevo_c)
                st.success(f"¡Conductor {c_nombre} integrado con éxito!")
                st.rerun()

    st.divider()
    st.subheader("🚗 Estado actual de la flota")
    for c in st.session_state.conductores:
        est = "🟢 Disponible" if c["disponible"] else "🔴 En viaje / Ocupado"
        st.write(f"• *{c['nombre']}* ({est}) | WhatsApp registrado: +{c['telefono']}")
    
    st.subheader("📋 Registro de Solicitudes")
    if st.session_state.historial_viajes:
        st.table(st.session_state.historial_viajes)
    else:
        st.write("No hay solicitudes registradas en esta sesión.")
        
    if st.button("🔄 Reiniciar Jornada (Liberar Conductores)"):
        for c in st.session_state.conductores: c["disponible"] = True
        st.session_state.historial_viajes = []
        st.rerun()
