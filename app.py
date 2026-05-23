import streamlit as st
from streamlit_js_eval import streamlit_js_eval

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

# --- INICIALIZACIÓN DE DATOS ---
if 'billetera_plataforma' not in st.session_state: st.session_state.billetera_plataforma = 0.0
if 'historial_viajes' not in st.session_state: st.session_state.historial_viajes = []
if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Jean", "ubicacion": "Tarascon", "disponible": True, "ganancias_netas": 0.0},
        {"nombre": "Marie", "ubicacion": "Beaucaire", "disponible": True, "ganancias_netas": 0.0},
        {"nombre": "Pierre", "ubicacion": "St-Étienne-du-Grès", "disponible": True, "ganancias_netas": 0.0}
    ]

# Matriz de soporte base
pueblos = ["Tarascon", "Beaucaire", "St-Étienne-du-Grès", "Fontvieille", "Boulbon"]

# --- INTERFAZ ---
st.markdown("<h1 class='brand-title'>🚕 ¡Muévete!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>con papá lucho</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Datos del Pasajero")
nombre_pasajero = st.text_input("Tu Nombre y Apellido", placeholder="Ej: Juan Pérez")
telefono_pasajero = st.text_input("Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 🗺️ Ubicación de Recogida")

# BOTÓN DE GPS REAL
origen_gps = None
if st.button("📍 Usar mi ubicación GPS actual"):
    with st.spinner("Obteniendo coordenadas de tu teléfono..."):
        # Esto ejecuta un script real en el navegador del móvil para extraer la latitud y longitud
        loc = streamlit_js_eval(data_string="navigator.geolocation.getCurrentPosition(success => { return success.coords.latitude + ',' + success.coords.longitude; })", want_output=True)
        if loc:
            origen_gps = loc
            st.success(f"Ubicación obtenida por GPS: {origen_gps}")
        else:
            st.warning("Por favor, acepta los permisos de ubicación en tu teléfono móvil.")

# Si no usa el GPS o falla, puede elegir manualmente
origen_manual = st.selectbox("O selecciona punto de recogida manual:", pueblos, index=0)
destino = st.selectbox("🏁 ¿A dónde vas? (Destino)", pueblos, index=1)

origen_final = f"Coordenadas GPS ({origen_gps})" if origen_gps else origen_manual

st.markdown("### 💳 Método de pago")
metodo_pago = st.radio("Pago:", ["💶 Efectivo", "💳 Tarjeta Digital"], horizontal=True)

if st.button("🚀 PEDIR VIAJE AHORA"):
    if not nombre_pasajero.strip() or not telefono_pasajero.strip():
        st.error("⚠️ Falta tu nombre o teléfono.")
    elif origen_manual == destino and not origen_gps:
        st.error("El origen y el destino no pueden ser iguales.")
    else:
        # Tarifa plana simulada de prueba para ubicación exacta
        precio_total = 8.50 
        comision = round(precio_total * 0.15, 2)
        pago_conductor = round(precio_total - comision, 2)
        
        conductor_asignado = next((c for c in st.session_state.conductores if c["disponible"]), None)
        
        if conductor_asignado:
            st.session_state.billetera_plataforma += comision
            conductor_asignado["ganancias_netas"] += pago_conductor
            conductor_asignado["disponible"] = False
            
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Ubicación Recogida": origen_final,
                "Destino": destino,
                "Conductor": conductor_asignado["nombre"],
                "Total": f"{precio_total:.2f} €"
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Confirmado!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>El conductor <b>{conductor_asignado['nombre']}</b> va hacia tu ubicación.</p>
                </div>
            """, unsafe_allow_html=True)
            st.metric(label="Tarifa Estimada", value=f"{precio_total:.2f} €")
        else:
            st.warning("No hay conductores libres.")

# Consola de administración
with st.expander("⚙️ Consola de Control de Papá Lucho"):
    st.write("### 📋 Pedidos Activos con localización:")
    if st.session_state.historial_viajes:
        st.table(st.session_state.historial_viajes)
    else:
        st.write("No hay solicitudes aún.")
        
    if st.button("🔄 Liberar Flota"):
        for c in st.session_state.conductores: c["disponible"] = True
        st.session_state.historial_viajes = []
        st.rerun()
[03:18, 23/5/2026] cchiluisa: import streamlit as st
import urllib.parse  # Para codificar el texto del mensaje de WhatsApp

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

# --- MATRIZ DE DISTANCIAS COBERTURA LOCAL ---
DISTANCIAS = {
    "Tarascon": {"Beaucaire": 2, "St-Étienne-du-Grès": 8, "Fontvieille": 10, "Boulbon": 9, "Tarascon": 0},
    "Beaucaire": {"Tarascon": 2, "St-Étienne-du-Grès": 10, "Fontvieille": 12, "Boulbon": 11, "Beaucaire": 0},
    "St-Étienne-du-Grès": {"Tarascon": 8, "Beaucaire": 10, "Fontvieille": 9, "Boulbon": 15, "St-Étienne-du-Grès": 0},
    "Fontvieille": {"Tarascon": 10, "Beaucaire": 12, "St-Étienne-du-Grès": 9, "Boulbon": 18, "Fontvieille": 0},
    "Boulbon": {"Tarascon": 9, "Beaucaire": 11, "St-Étienne-du-Grès": 15, "Fontvieille": 18, "Boulbon": 0}
}
pueblos = list(DISTANCIAS.keys())

# --- INICIALIZACIÓN DE ALMACENAMIENTO DINÁMICO ---
if 'billetera_plataforma' not in st.session_state: 
    st.session_state.billetera_plataforma = 0.0
if 'historial_viajes' not in st.session_state: 
    st.session_state.historial_viajes = []

# Lista inicial de conductores de ejemplo (puedes borrarlos o usarlos de guía)
if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Jean", "ubicacion": "Tarascon", "disponible": True, "ganancias_netas": 0.0, "telefono": "33612345678"},
        {"nombre": "Marie", "ubicacion": "Beaucaire", "disponible": True, "ganancias_netas": 0.0, "telefono": "33687654321"}
    ]

# --- INTERFAZ DE USUARIO PRINCIPAL (VISTA CLIENTE) ---
st.markdown("<h1 class='brand-title'>🚕 ¡Muévete!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>con papá lucho</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 👤 Datos del Pasajero")
nombre_pasajero = st.text_input("Tu Nombre y Apellido", placeholder="Ej: Juan Pérez")
telefono_pasajero = st.text_input("Teléfono de Contacto 📞", placeholder="Ej: +33 6 12 34 56 78")

st.divider()
st.markdown("### 🗺️ ¿Hacia dónde viajamos hoy?")
origen = st.selectbox("📍 Punto de recogida", pueblos, index=0)
destino = st.selectbox("🏁 Destino final", pueblos, index=1)

st.markdown("### 💳 Método de pago")
metodo_pago = st.radio("Selecciona cómo prefieres pagar:", ["💶 Efectivo", "💳 Tarjeta Digital"], horizontal=True)

st.write("") 

if st.button("🚀 PEDIR VIAJE AHORA"):
    if not nombre_pasajero.strip() or not telefono_pasajero.strip():
        st.error("⚠️ Por favor, introduce tu nombre y teléfono de contacto.")
    elif origen == destino:
        st.error("El origen y el destino no pueden ser iguales. 😉")
    else:
        distancia = DISTANCIAS[origen][destino]
        precio_total = 3.00 + (distancia * 1.20)
        comision = round(precio_total * 0.15, 2)
        pago_conductor = round(precio_total - comision, 2)
        
        # FILTRAR ÚNICAMENTE LOS CONDUCTORES QUE ESTÁN LIBRES (Disponibles)
        libres = [c for c in st.session_state.conductores if c["disponible"]]
        
        if libres:
            # Lógica inteligente: Encontrar al conductor disponible más cercano al punto de recogida
            conductor_asignado = None
            dist_minima = float('inf')
            for c in libres:
                dist_al_cliente = DISTANCIAS[c["ubicacion"]][origen]
                if dist_al_cliente < dist_minima:
                    dist_minima = dist_al_cliente
                    conductor_asignado = c
            
            # Modificar estados en tiempo real
            st.session_state.billetera_plataforma += comision
            conductor_asignado["ganancias_netas"] += pago_conductor
            conductor_asignado["ubicacion"] = destino
            conductor_asignado["disponible"] = False  # Pasa a estar OCUPADO
            
            # Guardar en el panel central
            registro_viaje = {
                "Pasajero": nombre_pasajero,
                "Teléfono": telefono_pasajero,
                "Origen": origen,
                "Destino": destino,
                "Conductor Asignado": conductor_asignado["nombre"],
                "Total": f"{precio_total:.2f} €"
            }
            st.session_state.historial_viajes.append(registro_viaje)
            
            # Preparar la alerta directa al WhatsApp del conductor asignado
            texto_alerta = (
                f"🚖 ¡NUEVO VIAJE ASIGNADO!\n\n"
                f"👤 Cliente: {nombre_pasajero}\n"
                f"📞 Teléfono: {telefono_pasajero}\n"
                f"📍 Recogida: {origen}\n"
                f"🏁 Destino: {destino}\n"
                f"💰 Tu Ganancia: {pago_conductor:.2f} €\n"
                f"💳 Pago: {metodo_pago}\n\n"
                f"Por favor, ponte en contacto de inmediato con el cliente."
            )
            texto_codificado = urllib.parse.quote(texto_alerta)
            url_whatsapp = f"https://wa.me/{conductor_asignado['telefono']}?text={texto_codificado}"
            
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Viaje Solicitado con Éxito!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>El sistema localizó al conductor libre más cercano: <b>{conductor_asignado['nombre']}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.metric(label="Tarifa Cerrada", value=f"{precio_total:.2f} €")
            
            # BOTÓN DIRECTO QUE VA AL WHATSAPP DEL CONDUCTOR SELECCIONADO
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:14px; font-weight:bold; font-size:1.1em; cursor:pointer; margin-top:10px;">
                        💬 ENVIAR ALERTA A {conductor_asignado['nombre'].upper()}
                    </button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background-color: #fef3c7; padding: 15px; border-radius: 16px; border-left: 6px solid #d97706;'>
                    <h4 style='color: #78350f; margin: 0;'>Todos ocupados ⚠️</h4>
                    <p style='color: #92400e; margin: 5px 0 0 0;'>Nuestros 3 conductores están realizando servicios ahora mismo. Inténtalo en unos minutos.</p>
                </div>
            """, unsafe_allow_html=True)

# --- PANEL ADMINISTRATIVO (CONSOLA INTERNA) ---
st.write("")
with st.expander("⚙️ PANEL CENTRAL DE ADMINISTRACIÓN (Papá Lucho)"):
    
    # NUEVO FORMULARIO PARA AGREGAR CONDUCTORES DESDE LA PANTALLA
    st.subheader("➕ Registrar Nuevo Conductor de la Flota")
    with st.form("nuevo_chofer_form", clear_on_submit=True):
        c_nombre = st.text_input("Nombre del Conductor")
        c_telefono = st.text_input("Número de WhatsApp (con prefijo de país, ej: 33612345678 para Francia)")
        c_pueblo = st.selectbox("Ubicación inicial", pueblos)
        
        enviar_registro = st.form_submit_button("💾 Guardar Conductor")
        if enviar_registro:
            if c_nombre.strip() and c_telefono.strip():
                # Agregar el nuevo conductor con sus datos a la memoria viva
                nuevo_c = {
                    "nombre": c_nombre,
                    "ubicacion": c_pueblo,
                    "disponible": True,
                    "ganancias_netas": 0.0,
                    "telefono": c_telefono.strip().replace("+", "") # limpia signos si los ponen
                }
                st.session_state.conductores.append(nuevo_c)
                st.success(f"¡Conductor {c_nombre} integrado con éxito y listo para recibir alertas!")
                st.rerun()
            else:
                st.error("Por favor completa el nombre y el teléfono.")

    st.divider()
    
    # MONITOREO DE FLOTA ACTUAL Y DISPONIBILIDAD
    st.subheader("🚗 Estado e Ingresos de los Conductores en Activo")
    st.caption("Aquí verás quién está libre (🟢) u ocupado (🔴)")
    for c in st.session_state.conductores:
        est = "🟢 Disponible" if c["disponible"] else "🔴 Ocupado en viaje"
        st.write(f"• *{c['nombre']}* ({est}) | En: {c['ubicacion']} | WhatsApp registrado: +{c['telefono']} | Saldo Neto: {c['ganancias_netas']:.2f}€")
    
    st.write("")
    st.metric(label="Comisiones acumuladas de la Central (15%)", value=f"{st.session_state.billetera_plataforma:.2f} €")
    
    # REGISTRO DE PEDIDOS DE LA SESIÓN
    st.subheader("📋 Registro de Carreras")
    if st.session_state.historial_viajes:
        st.table(st.session_state.historial_viajes)
    else:
        st.write("No hay viajes en esta sesión.")
        
    if st.button("🔄 Reiniciar Jornada (Liberar a todos)"):
        for c in st.session_state.conductores:
            c["disponible"] = True
        st.session_state.historial_viajes = []
        st.rerun()
