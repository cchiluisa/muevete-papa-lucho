import streamlit as st
import urllib.parse
import json
import os

# Configuración de la pantalla del smartphone
st.set_page_config(page_title="Los Muchachos de Papá Lucho", page_icon="🤝", layout="centered")

# Estilos de diseño móvil personalizados (Color Verde Confianza / Azul Asistencia)
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
        background-color: #059669 !important; /* Verde Esmeralda de confianza */
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
        color: #059669;
        font-weight: bold;
        margin-top: 0px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS COMPARTIDA EN ARCHIVO LOCAL ---
DB_FILE = "estado_muchachos.json"

def cargar_equipo_global():
    # El equipo fijo con sus números reales
    equipo_defecto = [
        {"nombre": "Luis", "estado": "⚪ Desconectado", "telefono": "33751865303"},
        {"nombre": "Filipe", "estado": "⚪ Desconectado", "telefono": "33651883295"},
        {"nombre": "Christian", "estado": "⚪ Desconectado", "telefono": "33745378520"}
    ]
    if not os.path.exists(DB_FILE):
        guardar_equipo_global(equipo_defecto)
        return equipo_defecto
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return equipo_defecto

def guardar_equipo_global(equipo):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(equipo, f, ensure_ascii=False, indent=4)

# Carga de datos del equipo
muchachos_actuales = cargar_equipo_global()

if 'historial_favores' not in st.session_state: 
    st.session_state.historial_favores = []

# --- INTERFAZ VISTA CLIENTE ---
st.markdown("<h1 class='brand-title'>🤝 ¡Tus Muchachos!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>Favores y Soluciones de Papá Lucho</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Tus Datos")
nombre_cliente = st.text_input("Tu Nombre y Apellido", placeholder="Ej: María Gómez")
telefono_cliente = st.text_input("Tu Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 📝 ¿Qué favor necesitas hoy?")

tipo_favor = st.selectbox(
    "¿En qué te podemos ayudar?",
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
    "Explícanos los detalles del favor:", 
    placeholder="Ej: Necesito que recojan un paquete en la oficina de correos a nombre de María o comprar 2 litros de leche y pan en el súper..."
)

direccion_favor = st.text_input("📍 Dirección donde debemos ir / entregarlo", placeholder="Ej: Rue de la République, Tarascon")

st.write("") 

if st.button("🚀 SOLICITAR ASISTENCIA NOW"):
    if not nombre_cliente.strip() or not telefono_cliente.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif not detalles_favor.strip() or not direccion_favor.strip():
        st.error("⚠️ Por favor, cuéntanos en detalle qué necesitas y dónde debemos ir.")
    else:
        # Buscar el primer muchacho disponible ("🟢 Activo y Listo")
        disponibles = [m for m in muchachos_actuales if m["estado"] == "🟢 Activo y Listo"]
        
        if disponibles:
            muchacho_asignado = disponibles[0]
            
            # Cambiar estado en la base de datos compartida a "Ocupado"
            for m in muchachos_actuales:
                if m["nombre"] == muchacho_asignado["nombre"]:
                    m["estado"] = "🟡 Haciendo un Favor"
            guardar_equipo_global(muchachos_actuales)
            
            nombre_m = muchacho_asignado["nombre"]
            
            # Registrar en el historial interno
            registro = {
                "Cliente": nombre_cliente,
                "Tipo": tipo_favor,
                "Dirección": direccion_favor,
                "Asignado A": nombre_m
            }
            st.session_state.historial_favores.append(registro)
            
            # Formatear el mensaje de WhatsApp para el muchacho
            texto_base = f"Hola {nombre_m}! Necesito un favor:\n\n" \
                         f"👤 Cliente: {nombre_cliente}\n" \
                         f"📞 Contacto: {telefono_cliente}\n" \
                         f"📋 Qué hacer: {tipo_favor} - {detalles_favor}\n" \
                         f"📍 Dónde: {direccion_favor}"
                         
            texto_codificado = urllib.parse.quote(texto_base)
            url_whatsapp = f"https://wa.me/{muchacho_asignado['telefono']}?text={texto_codificado}"
            
            st.markdown(f"""
                <div style='background-color: #d1fae5; padding: 18px; border-radius: 16px; border-left: 6px solid #059669; margin-bottom: 15px;'>
                    <h4 style='color: #065f46; margin: 0;'>✨ ¡Solicitud Enviada!</h4>
                    <p style='color: #065f46; margin: 6px 0 0 0;'><b>{nombre_m}</b> se encargará de tu recado.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 HABLAR CON {nombre_m.upper()} POR WHATSAPP
                    </button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("🛏️ En este momento todos los muchachos están ocupados o descansando. ¡Inténtalo de nuevo en un rato!")

# --- PANEL DE CONTROL INTERNO ---
st.write("")
with st.expander("⚙️ Consola de Los Muchachos (Uso Interno)"):
    clave_ingresada = st.text_input("🔑 Contraseña de Acceso", type="password")
    
    if clave_ingresada == "lucho123":
        st.success("🔓 Panel de Control Activo")
        st.divider()
        st.subheader("💼 Control de Disponibilidad")
        st.info("Actívate cuando estés listo para hacer recados y desconéctate al terminar tu turno.")
        
        for idx, m in enumerate(muchachos_actuales):
            st.markdown(f"👤 *{m['nombre']}* | Estado: {m['estado']}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🟢 Disponible", key=f"disp_{m['nombre']}_{idx}"):
                    muchachos_actuales[idx]["estado"] = "🟢 Activo y Listo"
                    guardar_equipo_global(muchachos_actuales)
                    st.rerun()
            with col2:
                if m["estado"] == "🟡 Haciendo un Favor":
                    if st.button("✅ Terminado", key=f"fin_{m['nombre']}_{idx}"):
                        muchachos_actuales[idx]["estado"] = "🟢 Activo y Listo"
                        guardar_equipo_global(muchachos_actuales)
                        st.rerun()
                else:
                    st.button("✅ Terminado", key=f"fin_{m['nombre']}_{idx}", disabled=True)
            with col3:
                if st.button("⚪ Desconectarse", key=f"desc_{m['nombre']}_{idx}"):
                    muchachos_actuales[idx]["estado"] = "⚪ Desconectado"
                    guardar_equipo_global(muchachos_actuales)
                    st.rerun()
            st.divider()
            
        st.subheader("📋 Registro de Favores de la Sesión")
        if st.session_state.historial_favores:
            st.table(st.session_state.historial_favores)
        else:
            st.write("No hay solicitudes registradas en esta ventana.")
            
        if st.button("🔄 Resetear todo el Equipo a Desconectado"):
            for m in muchachos_actuales:
                m["estado"] = "⚪ Desconectado"
            guardar_equipo_global(muchachos_actuales)
            st.session_state.historial_favores = []
            st.rerun()
            
    elif clave_ingresada != "":
        st.error("🔒 Clave incorrecta.")
