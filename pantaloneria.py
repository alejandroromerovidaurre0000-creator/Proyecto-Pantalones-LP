import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO ENTERPRISE - ALTA GAMA)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES (Minimalismo Corporativo)
C_BLACK = "#0f172a"       # Azul noche muy oscuro (Más premium que negro puro)
C_WHITE = "#FFFFFF"       
C_ACCENT = "#5B2C6F"      # Morado Identidad
C_SUCCESS = "#059669"     # Verde Esmeralda (Éxito)
C_BG_LIGHT = "#F8FAFC"    # Gris azulado muy suave

# CSS "QUIRÚRGICO" - SOLUCIÓN TOTAL A MODO OSCURO Y DISEÑO PREMIUM
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');
    
    /* 1. RESET GLOBAL */
    .stApp {{
        background-color: {C_WHITE} !important;
        font-family: 'Inter', sans-serif;
        color: {C_BLACK} !important;
    }}
    
    /* 2. TEXTOS SIEMPRE OSCUROS */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {{
        color: {C_BLACK} !important;
    }}
    
    /* 3. MENÚ LATERAL (SIDEBAR) BLINDADO */
    [data-testid="stSidebar"] {{
        background-color: {C_BG_LIGHT} !important;
        border-right: 1px solid #e2e8f0;
    }}
    [data-testid="stSidebar"] * {{
        color: {C_BLACK} !important;
    }}
    /* Icono de cerrar menú siempre visible */
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: {C_BLACK} !important;
    }}
    
    /* 4. SOLUCIÓN MENÚS DESPLEGABLES (SELECTBOX) EN MÓVIL */
    div[data-baseweb="select"] > div {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="popover"], ul[data-baseweb="menu"] {{
        background-color: {C_WHITE} !important;
        border: 1px solid #e2e8f0 !important;
    }}
    li[data-baseweb="option"] {{
        color: {C_BLACK} !important;
        background-color: {C_WHITE} !important;
    }}
    li[data-baseweb="option"]:hover {{
        background-color: #f1f5f9 !important; /* Highlight suave */
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] span {{
        color: {C_BLACK} !important;
    }}
    
    /* 5. BOTONES PREMIUM (NO SHADOWY, FLAT MODERN) */
    .stButton > button {{
        background-color: {C_BLACK} !important;
        color: {C_WHITE} !important; 
        border-radius: 8px !important;
        height: 55px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }}
    .stButton > button:hover {{
        background-color: {C_ACCENT} !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(91, 44, 111, 0.3) !important;
    }}
    .stButton > button p {{
        color: {C_WHITE} !important; 
    }}
    
    /* 6. INPUTS DE TEXTO LIMPIOS */
    .stTextInput input, .stTextArea textarea {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {C_ACCENT} !important;
        box-shadow: 0 0 0 3px rgba(91, 44, 111, 0.1) !important;
    }}
    
    /* 7. TARJETAS "ENTERPRISE" */
    .enterprise-card {{
        background-color: {C_WHITE} !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }}
    .enterprise-card:hover {{
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }}
    
    /* 8. RECIBO DIGITAL (SUCCESS) */
    .digital-receipt {{
        background-color: #F0FDF4; /* Verde muy claro */
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
    }}
    .receipt-title {{
        color: #15803D !important; /* Verde oscuro */
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }}
    .receipt-text {{
        color: #166534 !important;
        margin: 5px 0;
    }}

    /* Ocultar UI de Streamlit */
    header[data-testid="stHeader"] {{ background: transparent !important; }}
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
# 3. BARRA LATERAL (DISEÑO LIMPIO)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:20px; font-size: 40px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; margin:0; letter-spacing:1px; font-weight:700;'>PANTALONERÍA<br>INTEGRAL</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navegación
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("🔐 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("🎨 CATÁLOGO & DISEÑO"): st.session_state.page = "CATALOGO"
    if st.button("🛍️ BOLSA DE COMPRA"): st.session_state.page = "CARRITO"
    
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
    <div style="text-align:center; padding:40px 20px; border-bottom:1px solid #eee; margin-bottom:40px;">
        <h1 style="font-size: 3.2rem; font-weight: 800; margin:0; line-height:1.1; letter-spacing:-1px;">PANTALONERÍA INTEGRAL</h1>
        <p style="letter-spacing:2px; margin-top:10px; color:#555 !important; font-size:0.9rem; font-weight:500;">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Premium
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    with col_kpi1:
        st.markdown("""
        <div class="enterprise-card" style="text-align:center">
            <h2 style="color:#5B2C6F !important; font-size:2.5rem; margin:0;">99.9%</h2>
            <p style="margin:0; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Precisión Biométrica</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi2:
        st.markdown("""
        <div class="enterprise-card" style="text-align:center">
            <h2 style="color:#0f172a !important; font-size:2.5rem; margin:0;">24-48h</h2>
            <p style="margin:0; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Entrega Express</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi3:
        st.markdown("""
        <div class="enterprise-card" style="text-align:center">
            <h2 style="color:#0f172a !important; font-size:2.5rem; margin:0;">100%</h2>
            <p style="margin:0; font-size:0.8rem; text-transform:uppercase; font-weight:600;">Calidad Certificada</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 LA EVOLUCIÓN DEL PANTALÓN")
        st.write("""
        Reinventamos la industria textil masculina mediante un modelo **Phygital**.
        
        Hemos eliminado los trajes innecesarios y las tallas genéricas para ofrecerte una prenda construida matemática y anatómicamente para ti.
        """)
        st.info("✅ **GARANTÍA DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón**. Esto garantiza frescura y evita alergias, superando el estándar de poliéster del mercado.")
    
    with c_steps:
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="margin-top:0;">FLUJO DEL USUARIO</h4>
            <div style="margin-top:15px;">
                <p><b>1. DIGITAL LOCKER</b><br><span style="font-size:0.85rem; color:#666 !important;">Escaneo biométrico único.</span></p>
                <p><b>2. CATÁLOGO</b><br><span style="font-size:0.85rem; color:#666 !important;">Configuración de tela y diseño.</span></p>
                <p><b>3. ENTREGA</b><br><span style="font-size:0.85rem; color:#666 !important;">En tu puerta en 48 hrs.</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- DIGITAL LOCKER ---
elif st.session_state.page == "LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER")
    st.caption("Gestión de Moldería y Datos Biométricos.")
    
    col_auth, col_info = st.columns([1, 2.5])
    
    with col_auth:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID Cliente", placeholder="Ej: 1004")
        if st.button("ACCEDER AL SISTEMA"):
            if id_user in DB_CLIENTES:
                # Animación de carga técnica
                progreso = st.progress(0, text="Conectando Servidor Seguro...")
                time.sleep(0.3)
                progreso.progress(45, text="Desencriptando parámetros corporales...")
                time.sleep(0.3)
                progreso.progress(80, text="Generando moldería vectorial...")
                time.sleep(0.3)
                progreso.empty()
                
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Bienvenido, {st.session_state.usuario['nombre']}", icon="🔓")
            else:
                st.error("ID No Reconocido.")
    
    with col_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="enterprise-card" style="border-left: 8px solid {C_ACCENT};">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="letter-spacing:2px; text-transform:uppercase; margin-top:5px; font-size:0.8rem; color:#555 !important;">
                    {u['cargo']} • ID: {id_user} • ESTADO: ACTIVO
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            c_chart, c_metrics = st.columns([1.2, 1])
            with c_chart:
                st.markdown("#### 📊 Análisis de Ingeniería")
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=u['radar_data'], theta=categories, fill='toself', name='Cliente', line_color=C_ACCENT))
                fig.add_trace(go.Scatterpolar(r=STANDARD_DATA, theta=categories, name='Promedio', line_color='#94a3b8', line_dash='dot'))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 110]), bgcolor='white'),
                    showlegend=True, height=350, margin=dict(l=40, r=40, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black', family="Inter")
                )
                st.plotly_chart(fig, use_container_width=True)

            with c_metrics:
                st.markdown("#### 📐 Cotas (cm)")
                col_a, col_b = st.columns(2)
                col_a.metric("Cintura", u['cintura'])
                col_b.metric("Largo", u['largo'])
                col_a.metric("Cadera", u['cadera'])
                col_b.metric("Tiro", u['tiro'])
                col_a.metric("Muslo", u['muslo'])
                col_b.metric("Rodilla", u['rodilla'])
                
                st.success(f"✅ FIT ASIGNADO: **{u['fit']}**")
        else:
            st.info("🔒 El sistema está en modo espera. Ingrese un ID válido.")

# --- CATÁLOGO ---
elif st.session_state.page == "CATALOGO":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.caption(f"Diseñando para: **{st.session_state.usuario['nombre']}**")
    
    c_config, c_preview = st.columns([1, 1])
    
    with c_config:
        st.subheader("1. LÍNEA")
        linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
        
        opciones_telas = {}
        desc = ""
        
        if "ESTÁNDAR" in linea:
            opciones_telas = {
                "Gabardina Spandex (97% Alg)": 220,
                "Dril Confort (Algodón)": 240
            }
            desc = "Tejidos resistentes con elastano. Ideales para el uso intensivo."
        else:
            opciones_telas = {
                "Lana Fría Super 100's": 420,
                "Casimir Importado": 450
            }
            desc = "Tejidos nobles importados. Termicidad regulada y caída sastre."
            
        st.info(f"ℹ️ {desc}")
        
        st.subheader("2. MATERIAL")
        nombre_tela_sel = st.radio("Opciones:", list(opciones_telas.keys()))
        precio = opciones_telas[nombre_tela_sel]
        
        st.subheader("3. ACABADO (COLOR)")
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1e293b", "Kaki Oficina": "#cbd5e1", "Verde Olivo": "#3f6212"}
        else:
            colores = {"Gris Oxford": "#334155", "Negro Profundo": "#020617", "Azul Noche": "#0f172a"}
            
        color_nom = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        color_hex = colores[color_nom]

    with c_preview:
        st.subheader("VISTA PREVIA")
        st.markdown(f"""
        <div class="enterprise-card" style="text-align:center;">
            <div style="height:150px; width:100%; background-color:{color_hex}; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:25px; box-shadow:inset 0 0 40px rgba(0,0,0,0.05);"></div>
            <h1 style="color:{C_ACCENT} !important; margin:0; font-size:4rem; line-height:1;">{precio} Bs.</h1>
            <p style="color:#64748b !important; font-size:0.9rem; margin-bottom:20px;">PRECIO FINAL</p>
            <div style="text-align:left; background-color:#f8fafc; padding:15px; border-radius:10px; border:1px solid #e2e8f0;">
                <p style="margin:5px 0;">🏷️ <b>Línea:</b> {linea.split('(')[0]}</p>
                <p style="margin:5px 0;">🧵 <b>Tela:</b> {nombre_tela_sel}</p>
                <p style="margin:5px 0;">🎨 <b>Color:</b> {color_nom}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A MI BOLSA"):
            # Secuencia de Notificaciones de Ingeniería (Toast)
            st.toast("⚙️ Validando stock de materia prima...", icon="🏭")
            time.sleep(0.7)
            st.toast("📐 Vinculando con perfil biométrico...", icon="👤")
            time.sleep(0.7)
            st.toast("✅ ¡Ítem agregado a la orden de producción!", icon="🛍️")
            
            st.session_state.carrito.append({
                "Línea": linea, "Tela": nombre_tela_sel, "Color": color_nom, "Precio": precio
            })

# --- CARRITO ---
elif st.session_state.page == "CARRITO":
    st.markdown("## 🛍️ BOLSA DE COMPRAS")
    
    if len(st.session_state.carrito) > 0:
        # Tabla estilizada
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total = df['Precio'].sum()
        
        # Totalizador visual
        st.markdown(f"""
        <div style="text-align:right; padding:20px; background-color:#F8FAFC; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:30px;">
            <span style="font-size:1.2rem; color:#64748b;">TOTAL A PAGAR:</span>
            <span style="font-size:2.5rem; font-weight:800; color:{C_ACCENT}; margin-left:15px;">{total} Bs.</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚚 DATOS DE LOGÍSTICA")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona de Cobertura", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
            st.text_area("Dirección Exacta", placeholder="Calle, Nro, Edificio, Piso...")
            st.text_input("Referencia Visual", placeholder="Ej: Portón color café, frente a la plaza...")
        with c2:
            st.text_input("Celular / WhatsApp")
            st.selectbox("Método de Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("CONFIRMAR Y PROCESAR PEDIDO"):
                if st.session_state.usuario:
                    with st.spinner("Conectando con Taller... Generando Orden..."):
                        time.sleep(2.5) # Pausa dramática para que se vea que procesa
                    
                    # --- ESTO REEMPLAZA LOS GLOBOS: EL RECIBO DIGITAL ---
                    numero_orden = f"ORD-{random.randint(10000, 99999)}"
                    st.success("¡TRANSACCIÓN EXITOSA!")
                    
                    st.markdown(f"""
                    <div class="digital-receipt">
                        <div class="receipt-title">✅ ORDEN CONFIRMADA</div>
                        <p class="receipt-text" style="font-size:1.2rem; color:#000 !important;">ID DE SEGUIMIENTO: <b>{numero_orden}</b></p>
                        <hr style="border-top: 1px dashed #166534; margin: 15px 0;">
                        <p class="receipt-text"><b>Cliente:</b> {st.session_state.usuario['nombre']}</p>
                        <p class="receipt-text"><b>Total:</b> {total} Bs.</p>
                        <p class="receipt-text"><b>Estado:</b> EN COLA DE CORTE</p>
                        <br>
                        <small style="color:#166534 !important;">Se ha enviado una copia al WhatsApp registrado.</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.carrito = []
                else:
                    st.error("⚠️ ERROR: No se detectó un perfil biométrico activo. Por favor vaya a 'DIGITAL LOCKER' e ingrese su ID.")
    else:
        st.info("Su bolsa de compras está vacía.")
