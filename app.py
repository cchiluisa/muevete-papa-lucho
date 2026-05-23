import streamlit as st

# Configuración de la pantalla del smartphone
st.set_page_config(page_title="Muévete con papá lucho", page_icon="🚕", layout="centered")

# Estilos de diseño móvil personalizados con el nombre de la marca
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
        background-color: #f59e0b !important; /* Amarillo taxi premium */
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

# --- INICIALIZACIÓN DE DATOS EN LA NUBE ---
DISTANCIAS = {
    "Tarascon": {"Beaucaire": 2, "St-Étienne-du-Grès": 8, "Fontvieille": 10, "Boulbon": 9, "Tarascon": 0},
    "Beaucaire": {"Tarascon": 2, "St-Étienne-du-Grès": 10, "Fontvieille": 12, "Boulbon": 11, "Beaucaire": 0},
    "St-Étienne-du-Grès": {"Tarascon": 8, "Beaucaire": 10, "Fontvieille": 9, "Boulbon": 15, "St-Étienne-du-Grès": 0},
    "Fontvieille": {"Tarascon": 10, "Beaucaire": 12, "St-Étienne-du-Grès": 9, "Boulbon": 18, "Fontvieille": 0},
    "Boulbon": {"Tarascon": 9, "Beaucaire": 11, "St-Étienne-du-Grès": 15, "Fontvieille": 18, "Boulbon": 0}
}
pueblos = list(DISTANCIAS.keys())

# Almacenamiento seguro en la sesión de la nube
if 'billetera_plataforma' not in st.session_state:
    st.session_state.billetera_plataforma = 0.0

if 'conductores' not in st.session_state:
    st.session_state.conductores = [
        {"nombre": "Jean", "ubicacion": "Tarascon", "disponible": True, "ganancias_netas": 0.0},
        {"nombre": "Marie", "ubicacion": "Beaucaire", "disponible": True, "ganancias_netas": 0.0},
        {"nombre": "Pierre", "ubicacion": "St-Étienne-du-Grès", "disponible": True, "ganancias_netas": 0.0}
    ]

# --- INTERFAZ DE USUARIO DE LA APP ---
st.markdown("<h1 class='brand-title'>🚕 ¡Muévete!</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>con papá lucho</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9em;'>Tu transporte de confianza en Tarascon, Beaucaire y alrededores</p>", unsafe_allow_html=True)
st.divider()

st.markdown("### 🗺️ ¿Hacia dónde viajamos hoy?")

origen = st.selectbox("📍 Punto de recogida", pueblos, index=0)
destino = st.selectbox("🏁 Destino final", pueblos, index=1)

st.markdown("### 💳 Método de pago")
metodo_pago = st.radio("Selecciona cómo prefieres pagar:", ["💶 Efectivo al conductor", "💳 Tarjeta Digital"], horizontal=True)

st.write("") 

if st.button("🚀 PEDIR VIAJE AHORA"):
    if origen == destino:
        st.error("¡Papá Lucho te lleva a donde quieras, pero el origen y el destino no pueden ser iguales! 😉")
    else:
        distancia = DISTANCIAS[origen][destino]
        precio_total = 3.00 + (distancia * 1.20)
        comision = round(precio_total * 0.15, 2)
        pago_conductor = round(precio_total - comision, 2)
        
        # Filtrar conductores disponibles en la sesión
        disponibles = [c for c in st.session_state.conductores if c["disponible"]]
        
        if disponibles:
            # Encontrar el coche más cercano
            conductor_asignado = None
            dist_minima = float('inf')
            for c in disponibles:
                dist_al_cliente = DISTANCIAS[c["ubicacion"]][origen]
                if dist_al_cliente < dist_minima:
                    dist_minima = dist_al_cliente
                    conductor_asignado = c
            
            # Registrar movimientos financieros
            st.session_state.billetera_plataforma += comision
            conductor_asignado["ganancias_netas"] += pago_conductor
            conductor_asignado["ubicacion"] = destino
            conductor_asignado["disponible"] = False
            
            # Confirmación de viaje en pantalla estilo App Móvil
            st.markdown(f"""
                <div style='background-color: #e0f2fe; padding: 18px; border-radius: 16px; border-left: 6px solid #0284c7; margin-bottom: 15px;'>
                    <h4 style='color: #0369a1; margin: 0;'>✨ ¡Viaje Confirmado!</h4>
                    <p style='color: #0c4a6e; margin: 6px 0 0 0;'>El conductor <b>{conductor_asignado['nombre']}</b> va en camino a recogerte.</p>
                    <p style='color: #0c4a6e; margin: 2px 0 0 0; font-size: 0.9em;'>Pago seleccionado: <i>{metodo_pago}</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            st.metric(label="Tarifa del viaje con Papá Lucho", value=f"{precio_total:.2f} €")
            st.caption(f"Distancia de ruta: {distancia} km | Conductor se moverá a: {destino}")
        else:
            st.markdown("""
                <div style='background-color: #fef3c7; padding: 15px; border-radius: 16px; border-left: 6px solid #d97706;'>
                    <h4 style='color: #78350f; margin: 0;'>Flota al máximo ⚠️</h4>
                    <p style='color: #92400e; margin: 5px 0 0 0;'>Todos los vehículos de Papá Lucho están ocupados. Por favor, espera unos minutos.</p>
                </div>
            """, unsafe_allow_html=True)

# Panel oculto para pruebas administrativas
with st.expander("⚙️ Consola interna de Papá Lucho"):
    st.metric(label="Ingresos por Comisión App (15%)", value=f"{st.session_state.billetera_plataforma:.2f} €")
    
    for c in st.session_state.conductores:
        est = "🟢 Disponible" if c["disponible"] else "🔴 En viaje"
        st.write(f"• *{c['nombre']}* ({est}) | Zona: {c['ubicacion']} | Saldo: {c['ganancias_netas']:.2f}€")
        
    if st.button("🔄 Inicializar / Liberar Flota"):
        for c in st.session_state.conductores:
            c["disponible"] = True
        st.rerun()