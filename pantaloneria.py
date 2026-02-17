import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO ALTO CONTRASTE FORZADO)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES
C_BLACK = "#000000"
C_WHITE = "#FFFFFF"
C_ACCENT = "#5B2C6F"

# CSS "NUCLEAR" - FUERZA COLORES SIN IMPORTAR EL MODO DEL DISPOSITIVO
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    
    /* 1. FORZAR FONDO BLANCO GLOBALMENTE */
    .stApp {{
        background-color: {C_WHITE} !important;
    }}
    
    /* 2. FORZAR TEXTO NEGRO EN TODA LA APP (EXCEPTO BOTONES) */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {{
        color: {C_BLACK} !important;
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 3. ARREGLO DEL MENÚ LATERAL (SIDEBAR) */
    [data-testid="stSidebar"] {{
        background-color: #f2f2f2 !important; /* Gris muy claro siempre */
        border-right: 1px solid #ccc;
    }}
    /* Fuerza bruta: TODO dentro del sidebar debe ser negro */
    [data-testid="stSidebar"] * {{
        color: {C_BLACK} !important;
    }}
    
    /* 4. ARREGLO DE BOTONES (FONDO NEGRO - TEXTO BLANCO) */
    /* Aquí usamos !important para sobreescribir la regla universal de texto negro */
    .stButton > button {{
        background-color: {C_BLACK} !important;
        color: {C_WHITE} !important; 
        border-radius: 6px !important;
        height: 55px !important;
        font-weight: 700 !important;
        border: none !important;
    }}
    .stButton > button:hover {{
        background-color: {C_ACCENT} !important;
        color: {C_WHITE} !important;
    }}
    .stButton > button p {{
        color: {C_WHITE} !important; /* Asegura que el texto dentro del botón sea blanco */
    }}
    
    /* 5. ARREGLO DE INPUTS (CUADROS DE TEXTO) */
    /* El fondo del input blanco y el texto que escribes negro */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border: 1px solid #ccc !important;
    }}
    
    /* 6. HEADER */
    .brand-header {{
        background-color: {C_WHITE};
        border-bottom: 3px solid {C_ACCENT};
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }}
    
    /* 7. TARJETAS DE INFORMACIÓN */
    .info-card {{
        background-color: {C_WHITE} !important;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    /* Ocultar elementos nativos */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebarNav"] {{display: none !important;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS
# ==============================================================================
DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'cargo': 'Postulante',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42, 'fit': 'Slim Fit',
        'radar_data': [82, 96, 54, 104, 26]
    },
    '1002': { 
        'nombre': 'Samael Gómez Rúa', 'cargo': 'Panelista', 
        'cintura': 94, 'largo': 100, 'cadera': 105, 'muslo': 62, 'tiro': 28, 'rodilla': 46, 'fit': 'Regular Comfort',
        'radar_data': [94, 105, 62, 100, 28]
    },
    '1003': { 
        'nombre': 'Jessica Susana Daza', 'cargo': 'Tutora',
        'cintura': 70, 'largo': 95, 'cadera': 92, 'muslo': 50, 'tiro': 24, 'rodilla': 38, 'fit': 'Relaxed Fit',
        'radar_data': [70, 92, 50, 95, 24]
    },
    '1004': { 
        'nombre': 'Miguel Vidal Sejas', 'cargo': 'Relator',
        'cintura': 88, 'largo': 102, 'cadera': 100, 'muslo': 58, 'tiro': 27, 'rodilla': 44, 'fit': 'Tailored Fit',
        'radar_data': [88, 100, 58, 102, 27]
    }
}
STANDARD_DATA = [84, 98, 56, 100, 26]

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'page' not in st.session_state: st.session_state.page = "INICIO"

# ==============================================================================
# 3. BARRA LATERAL (MENU BLINDADO)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size: 50px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; margin-top:0;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navegación
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("🔐 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("👖 DISEÑAR PANTALÓN"): st.session_state.page = "CATALOGO"
    if st.button("🛒 BOLSA DE COMPRA"): st.session_state.page = "CARRITO"
    
    st.markdown("---")
    st.caption("**Postulante:** Alejandro M. Romero")
    
    with st.expander("Tribunal Evaluador", expanded=True):
        st.markdown("• Tutora: Jessica Daza Morales")
        st.markdown("• Panelista: Samael Gómez Rúa")
        st.markdown("• Relator: Miguel Vidal Sejas")

# ==============================================================================
# 4. PÁGINAS DEL SISTEMA
# ==============================================================================

# --- INICIO ---
if st.session_state.page == "INICIO":
    st.markdown("""
    <div class="brand-header">
        <h1 style="font-size: 3rem; font-weight: 900; margin:0;">PANTALONERÍA INTEGRAL</h1>
        <p style="letter-spacing:2px; margin-top:10px;">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Biometría")
    k2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    k3.metric("Materiales", "Certificados", "Alta Gama")
    
    st.divider()
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 NUESTRA VISIÓN")
        st.write("""
        Revolucionamos la industria textil masculina. 
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas.
        """)
        st.info("✅ **ESTÁNDAR DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón** para garantizar frescura, hipoalergencia y durabilidad superior.")
    
    with c_steps:
        st.success("1. **DIGITAL LOCKER:** Escaneo de medidas.")
        st.info("2. **CONFIGURADOR:** Elige tela y color.")
        st.warning("3. **ENTREGA:** En tu puerta en 48 hrs.")

# --- DIGITAL LOCKER ---
elif st.session_state.page == "LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER")
    st.caption("Base de Datos y Perfil Biométrico.")
    
    col_auth, col_info = st.columns([1, 2.5])
    
    with col_auth:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID Cliente", placeholder="Ej: 1004")
        if st.button("CONSULTAR PERFIL"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Perfil Cargado Correctamente", icon="✅")
            else:
                st.error("ID No encontrado.")
    
    with col_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="info-card" style="border-left: 5px solid {C_ACCENT};">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="letter-spacing:1px; text-transform:uppercase;">{u['cargo']} | ID: {id_user}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            # Radar Chart
            c_chart, c_metrics = st.columns([1.2, 1])
            with c_chart:
                st.markdown("#### 📊 Análisis Morfológico")
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=u['radar_data'], theta=categories, fill='toself', name='Cliente', line_color=C_ACCENT))
                fig.add_trace(go.Scatterpolar(r=STANDARD_DATA, theta=categories, name='Promedio', line_color='#BDC3C7', line_dash='dot'))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 110]), bgcolor='white'),
                    showlegend=True, height=350, margin=dict(l=30, r=30, t=20, b=20),
                    paper_bgcolor='white', font=dict(color='black') 
                )
                st.plotly_chart(fig, use_container_width=True)

            with c_metrics:
                st.markdown("#### 📐 Medidas (cm)")
                col_a, col_b = st.columns(2)
                col_a.metric("Cintura", u['cintura'])
                col_b.metric("Largo", u['largo'])
                col_a.metric("Cadera", u['cadera'])
                col_b.metric("Tiro", u['tiro'])
                col_a.metric("Muslo", u['muslo'])
                col_b.metric("Rodilla", u['rodilla'])
                st.success(f"✅ FIT ASIGNADO: **{u['fit']}**")
        else:
            st.info("🔒 Sistema en espera. Ingrese ID para cargar datos.")

# --- CATÁLOGO ---
elif st.session_state.page == "CATALOGO":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.caption(f"Diseñando para: **{st.session_state.usuario['nombre']}**")
    
    c_config, c_preview = st.columns([1, 1])
    
    with c_config:
        st.subheader("1. LÍNEA")
        linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
        
        precio = 0
        telas = []
        if "ESTÁNDAR" in linea:
            telas = ["Gabardina Spandex (200 Bs.)", "Dril Confort (240 Bs.)"]
            desc = "Algodón + Elastano. Resistencia diaria."
        else:
            telas = ["Lana Fría Super 100's (420 Bs.)", "Casimir Importado (450 Bs.)"]
            desc = "Telas importadas. Caída perfecta."
        
        st.caption(f"ℹ️ {desc}")
        
        st.subheader("2. MATERIAL")
        tela_sel = st.radio("Opciones:", telas)
        precio = int(''.join(filter(str.isdigit, tela_sel)))
        
        st.subheader("3. COLOR")
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1B2631", "Kaki Oficina": "#D0D3D4", "Verde Olivo": "#4D5645"}
        else:
            colores = {"Gris Oxford": "#566573", "Negro Profundo": "#000000", "Azul Noche": "#154360"}
            
        color_nom = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        color_hex = colores[color_nom]

    with c_preview:
        st.subheader("VISTA PREVIA")
        st.markdown(f"""
        <div class="info-card" style="text-align:center;">
            <div style="height:100px; width:100%; background-color:{color_hex}; border-radius:8px; border:2px solid #ccc;"></div>
            <h1 style="color:{C_ACCENT} !important; margin-top:20px; font-size:3rem;">{precio} Bs.</h1>
            <p><b>{linea}</b></p>
            <p>{tela_sel.split('(')[0]}</p>
            <p>{color_nom}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A LA BOLSA"):
            st.session_state.carrito.append({
                "Línea": linea, "Tela": tela_sel.split("(")[0], "Color": color_nom, "Precio": precio
            })
            st.balloons()
            st.toast("Agregado")

# --- CARRITO ---
elif st.session_state.page == "CARRITO":
    st.markdown("## 🛒 FINALIZAR PEDIDO")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:{C_ACCENT} !important;'>TOTAL: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Logística de Entrega")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
            st.text_area("Dirección Exacta", placeholder="Av. Principal #123, Edificio...")
            st.text_input("Referencia Visual", placeholder="Frente a la Farmacia...")
        with c2:
            st.text_input("Celular / WhatsApp")
            st.selectbox("Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR PEDIDO"):
                if st.session_state.usuario:
                    with st.spinner("Procesando Orden de Corte..."):
                        time.sleep(2)
                    st.success("¡PEDIDO CONFIRMADO!")
                    st.info(f"Gracias {st.session_state.usuario['nombre']}. Nos contactaremos para coordinar la entrega.")
                    st.session_state.carrito = []
                else:
                    st.error("Por favor, identifíquese en 'PERFIL BIOMÉTRICO' antes de comprar.")
    else:
        st.info("Su bolsa de compras está vacía.")
