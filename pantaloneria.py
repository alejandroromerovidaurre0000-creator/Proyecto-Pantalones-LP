import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN (MODO "WHITE BÚNKER" - SOLUCIÓN TOTAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES "CLEAN TECH"
C_TEXT_MAIN = "#111827"   # Negro suave
C_ACCENT = "#5B2C6F"      # Morado Marca
C_BG_APP = "#FFFFFF"      # Blanco Puro
C_BORDER = "#E5E7EB"      # Borde sutil

# CSS MAESTRO: BLINDAJE CONTRA MODO OSCURO EN MÓVILES
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');
    
    /* 1. FORZADO DE ESQUEMA DE COLOR */
    :root {{
        color-scheme: light !important;
    }}
    
    /* 2. RESET GLOBAL */
    .stApp {{
        background-color: {C_BG_APP} !important;
        font-family: 'Manrope', sans-serif;
        color: {C_TEXT_MAIN} !important;
    }}
    
    /* 3. TEXTOS SIEMPRE NEGROS */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {{
        color: {C_TEXT_MAIN} !important;
    }}
    
    /* --- 4. ZONA CRÍTICA: MENÚS DESPLEGABLES (SELECTBOX) --- */
    /* Caja del selector cerrada */
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid {C_BORDER} !important;
    }}
    div[data-baseweb="select"] span {{
        color: #000000 !important;
    }}
    
    /* LA LISTA FLOTANTE (DONDE ESTABA EL ERROR) */
    div[data-baseweb="popover"], ul[data-baseweb="menu"] {{
        background-color: #FFFFFF !important;
        border: 1px solid {C_BORDER} !important;
    }}
    
    /* CADA OPCIÓN DE LA LISTA (SOLUCIÓN FONDO NEGRO) */
    li[data-baseweb="option"] {{
        background-color: #FFFFFF !important; /* Fuerza fondo blanco */
        color: #000000 !important;            /* Fuerza letra negra */
    }}
    
    /* OPCIÓN AL PASAR EL DEDO/MOUSE */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {{
        background-color: #F3F4F6 !important;
        color: {C_ACCENT} !important;
        font-weight: 700 !important;
    }}
    
    /* TEXTO DENTRO DE LA OPCIÓN */
    li[data-baseweb="option"] div {{
        color: inherit !important;
    }}
    
    /* --- 5. ZONA CRÍTICA: NOTIFICACIONES (TOASTS) --- */
    div[data-testid="stToast"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    /* Texto e iconos dentro del toast */
    div[data-testid="stToast"] p, div[data-testid="stToast"] svg {{
        color: #000000 !important;
        fill: {C_ACCENT} !important;
    }}
    
    /* 6. SIDEBAR LIMPIO */
    [data-testid="stSidebar"] {{
        background-color: #FAFAFA !important;
        border-right: 1px solid {C_BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {C_TEXT_MAIN} !important;
    }}
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: {C_TEXT_MAIN} !important;
    }}
    
    /* 7. TARJETAS PREMIUM */
    .pro-card {{
        background-color: #FFFFFF;
        border: 1px solid {C_BORDER};
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.04);
        margin-bottom: 25px;
        transition: transform 0.2s ease;
    }}
    .pro-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.08);
    }}
    
    /* 8. BOTONES HIGH-END (NEGROS) */
    .stButton > button {{
        background-color: {C_TEXT_MAIN} !important;
        color: #FFFFFF !important; 
        border-radius: 12px !important;
        height: 58px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }}
    .stButton > button:hover {{
        background-color: {C_ACCENT} !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(91, 44, 111, 0.25) !important;
    }}
    .stButton > button p {{ color: #FFFFFF !important; }}
    
    /* 9. INPUTS */
    .stTextInput input, .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: {C_TEXT_MAIN} !important;
        border: 1px solid {C_BORDER} !important;
        border-radius: 12px !important;
    }}
    .stTextInput input:focus {{
        border-color: {C_ACCENT} !important;
        box-shadow: 0 0 0 3px rgba(91, 44, 111, 0.1) !important;
    }}
    
    /* 10. RECIBO DIGITAL (TICKET) */
    .receipt-box {{
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }}

    /* OCULTAR UI STREAMLIT */
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
# 3. BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:15px; font-size: 45px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; margin:0; font-weight:800; letter-spacing:-0.5px;'>PANTALONERÍA<br>INTEGRAL</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
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
    <div style="text-align:center; padding:50px 20px; border-bottom:1px solid #F3F4F6; margin-bottom:40px;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin:0; line-height:1.1; letter-spacing:-2px;">PANTALONERÍA INTEGRAL</h1>
        <p style="letter-spacing:2px; margin-top:15px; color:#6B7280 !important; font-weight:600; font-size:0.9rem;">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Biometría 3D")
    k2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    k3.metric("Materiales", "Certificados", "Alta Gama")
    
    st.divider()
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 VISIÓN DEL PRODUCTO")
        st.write("""
        Revolucionamos la industria textil masculina mediante un modelo **Phygital** (Físico + Digital).
        
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas.
        """)
        st.info("✅ **GARANTÍA DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón**. Esto garantiza frescura y evita alergias, superando el estándar de poliéster del mercado.")
    
    with c_steps:
        st.markdown("""
        <div class="pro-card">
            <h4 style="margin-top:0;">FLUJO DE SERVICIO</h4>
            <div style="margin-top:20px;">
                <p style="margin-bottom:12px;"><b>1. DIGITAL LOCKER</b><br><span style="font-size:0.9rem; color:#6B7280 !important;">Escaneo biométrico único.</span></p>
                <p style="margin-bottom:12px;"><b>2. CATÁLOGO</b><br><span style="font-size:0.9rem; color:#6B7280 !important;">Configuración de tela y diseño.</span></p>
                <p style="margin-bottom:0;"><b>3. ENTREGA</b><br><span style="font-size:0.9rem; color:#6B7280 !important;">En tu puerta en 48 hrs.</span></p>
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
            <div class="pro-card" style="border-left: 8px solid {C_ACCENT};">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="letter-spacing:1px; text-transform:uppercase; margin-top:5px; font-size:0.85rem; color:#6B7280 !important;">
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
                fig.add_trace(go.Scatterpolar(r=STANDARD_DATA, theta=categories, name='Promedio', line_color='#9CA3AF', line_dash='dot'))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 110]), bgcolor='white'),
                    showlegend=True, height=350, margin=dict(l=40, r=40, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)', font=dict(color='black', family="Manrope")
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
        <div class="pro-card" style="text-align:center;">
            <div style="height:150px; width:100%; background-color:{color_hex}; border-radius:16px; border:1px solid #E5E7EB; margin-bottom:25px; box-shadow:inset 0 0 40px rgba(0,0,0,0.05);"></div>
            <h1 style="color:{C_ACCENT} !important; margin:0; font-size:4rem; line-height:1; letter-spacing:-2px;">{precio} Bs.</h1>
            <p style="color:#9CA3AF !important; font-size:0.9rem; margin-bottom:20px; font-weight:600; letter-spacing:1px;">PRECIO FINAL</p>
            <div style="text-align:left; background-color:#F9FAFB; padding:20px; border-radius:12px; border:1px solid #E5E7EB;">
                <p style="margin:5px 0;">🏷️ <b>Línea:</b> {linea.split('(')[0]}</p>
                <p style="margin:5px 0;">🧵 <b>Tela:</b> {nombre_tela_sel}</p>
                <p style="margin:5px 0;">🎨 <b>Color:</b> {color_nom}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A MI BOLSA"):
            st.toast("⚙️ Validando stock...", icon="🏭")
            time.sleep(0.5)
            st.toast("📐 Vinculando biometría...", icon="👤")
            time.sleep(0.5)
            st.toast("✅ ¡Ítem agregado!", icon="🛍️")
            
            st.session_state.carrito.append({
                "Línea": linea, "Tela": nombre_tela_sel, "Color": color_nom, "Precio": precio
            })

# --- CARRITO ---
elif st.session_state.page == "CARRITO":
    st.markdown("## 🛍️ BOLSA DE COMPRAS")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total = df['Precio'].sum()
        
        st.markdown(f"""
        <div style="text-align:right; padding:30px; background-color:#F9FAFB; border-radius:16px; border:1px solid #E5E7EB; margin-bottom:40px;">
            <span style="font-size:1.2rem; color:#6B7280; font-weight:500;">TOTAL A PAGAR:</span>
            <span style="font-size:3rem; font-weight:800; color:{C_ACCENT}; margin-left:20px;">{total} Bs.</span>
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
                    with st.spinner("Generando Orden de Corte Automatizada..."):
                        time.sleep(2.5) 
                    
                    numero_orden = f"ORD-{random.randint(10000, 99999)}"
                    st.success("¡TRANSACCIÓN EXITOSA!")
                    
                    st.markdown(f"""
                    <div class="receipt-box">
                        <h2 style="color:#15803D !important; margin:0; font-size:1.5rem;">✅ ORDEN CONFIRMADA</h2>
                        <p style="color:#166534 !important; font-size:1.2rem; font-weight:bold; letter-spacing:1px; margin-top:10px;">ID: {numero_orden}</p>
                        <hr style="border-top:1px dashed #4ADE80; margin:20px 0;">
                        <div style="text-align:left; color:#14532D !important;">
                            <p><b>Cliente:</b> {st.session_state.usuario['nombre']}</p>
                            <p><b>Estado:</b> EN COLA DE PRODUCCIÓN</p>
                            <p><b>Entrega Estimada:</b> 24-48 Horas</p>
                            <p style="font-size:1.2rem; margin-top:10px;"><b>Total:</b> {total} Bs.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.carrito = []
                else:
                    st.error("⚠️ ERROR: No se detectó un perfil biométrico activo. Por favor vaya a 'DIGITAL LOCKER' e ingrese su ID.")
    else:
        st.info("Su bolsa de compras está vacía.")
