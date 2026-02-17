import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO "MIDNIGHT LUXURY")
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES (DARK MODE NATIVO)
C_BG_MAIN = "#0E1117"     # Negro Profundo (Fondo)
C_BG_CARD = "#161B22"     # Gris Oscuro (Tarjetas)
C_TEXT_MAIN = "#FFFFFF"   # Blanco Puro (Texto)
C_TEXT_SEC = "#A1A1AA"    # Gris Plata (Subtítulos)
C_ACCENT = "#8B5CF6"      # Morado Neón Brillante
C_BORDER = "#30363D"      # Bordes sutiles oscuros

# CSS "DARK PREMIUM" - SOLUCIÓN DEFINITIVA DE VISIBILIDAD
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* 1. FORZADO DE MODO OSCURO (DARK SCHEME) */
    :root {{
        color-scheme: dark !important;
    }}
    
    /* 2. RESET GLOBAL */
    .stApp {{
        background-color: {C_BG_MAIN} !important;
        font-family: 'Inter', sans-serif;
        color: {C_TEXT_MAIN} !important;
    }}
    
    /* 3. TEXTOS BLANCOS */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {{
        color: {C_TEXT_MAIN} !important;
    }}
    .small-text {{ color: {C_TEXT_SEC} !important; }}
    
    /* 4. SOLUCIÓN MENÚS DESPLEGABLES (SELECTBOX) - VERSIÓN OSCURA */
    /* La caja cerrada */
    div[data-baseweb="select"] > div {{
        background-color: {C_BG_CARD} !important;
        color: {C_TEXT_MAIN} !important;
        border: 1px solid {C_BORDER} !important;
        border-radius: 12px !important;
    }}
    /* El texto dentro de la caja */
    div[data-baseweb="select"] span {{
        color: {C_TEXT_MAIN} !important;
    }}
    /* La flechita */
    div[data-baseweb="select"] svg {{
        fill: {C_TEXT_MAIN} !important;
    }}
    
    /* LA LISTA DESPLEGABLE (POPOVER) */
    div[data-baseweb="popover"], ul[data-baseweb="menu"] {{
        background-color: #1F242C !important; /* Un poco más claro que el fondo */
        border: 1px solid {C_ACCENT} !important; /* Borde neón */
    }}
    /* Las opciones */
    li[data-baseweb="option"] {{
        color: {C_TEXT_MAIN} !important;
        background-color: #1F242C !important;
    }}
    /* Hover en opción */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {{
        background-color: {C_ACCENT} !important;
        color: {C_TEXT_MAIN} !important;
    }}
    
    /* 5. INPUTS DE TEXTO (DARK MODE) */
    .stTextInput input, .stTextArea textarea {{
        background-color: {C_BG_CARD} !important;
        color: {C_TEXT_MAIN} !important;
        border: 1px solid {C_BORDER} !important;
        border-radius: 12px !important;
    }}
    .stTextInput input:focus {{
        border-color: {C_ACCENT} !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
    }}
    
    /* 6. SIDEBAR (Elegancia Oscura) */
    [data-testid="stSidebar"] {{
        background-color: {C_BG_CARD} !important;
        border-right: 1px solid {C_BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {C_TEXT_MAIN} !important;
    }}
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: {C_TEXT_MAIN} !important;
    }}
    
    /* 7. TARJETAS PREMIUM (GLASSMORPHISM OSCURO) */
    .premium-card {{
        background-color: {C_BG_CARD};
        border: 1px solid {C_BORDER};
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); /* Sombra negra profunda */
        margin-bottom: 20px;
    }}
    
    /* 8. BOTONES NEÓN */
    .stButton > button {{
        background: linear-gradient(135deg, #6D28D9, {C_ACCENT}) !important;
        color: {C_TEXT_MAIN} !important; 
        border-radius: 10px !important;
        height: 55px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6) !important;
        transform: scale(1.02);
    }}
    .stButton > button p {{ color: {C_TEXT_MAIN} !important; }}
    
    /* 9. RECIBO DIGITAL (DARK TICKET) */
    .digital-receipt {{
        background-color: #064E3B; /* Verde muy oscuro */
        border: 1px solid #10B981;
        border-radius: 15px;
        padding: 30px;
        color: #D1FAE5 !important;
        font-family: 'Courier New', monospace;
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
# 3. BARRA LATERAL (DARK SIDEBAR)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; margin-bottom:15px; font-size: 45px; filter: drop-shadow(0 0 10px rgba(139,92,246,0.5));'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; margin:0; font-weight:700; letter-spacing:1px; color:#fff !important;'>PANTALONERÍA<br>INTEGRAL</h4>", unsafe_allow_html=True)
    st.markdown(f"<hr style='border-color:{C_BORDER}'>", unsafe_allow_html=True)
    
    # Navegación
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("🔐 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("🎨 CATÁLOGO & DISEÑO"): st.session_state.page = "CATALOGO"
    if st.button("🛍️ BOLSA DE COMPRA"): st.session_state.page = "CARRITO"
    
    st.markdown(f"<hr style='border-color:{C_BORDER}'>", unsafe_allow_html=True)
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
    <div style="text-align:center; padding:50px 20px; border-bottom:1px solid #30363D; margin-bottom:40px;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin:0; line-height:1.1; letter-spacing:-1px; background: -webkit-linear-gradient(45deg, #FFF, #A1A1AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PANTALONERÍA INTEGRAL</h1>
        <p style="letter-spacing:3px; margin-top:15px; color:#A1A1AA !important; font-weight:500;">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Estilo Dark Mode
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Biometría 3D")
    k2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    k3.metric("Materiales", "Certificados", "Alta Gama")
    
    st.divider()
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 VISIÓN DEL PRODUCTO")
        st.write("""
        Revolucionamos la industria textil masculina mediante un modelo **Phygital**.
        
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas.
        """)
        # Nota técnica oscura
        st.info("✅ **GARANTÍA DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón**. Esto garantiza frescura y evita alergias, superando el estándar de poliéster del mercado.")
    
    with c_steps:
        st.markdown(f"""
        <div class="premium-card">
            <h4 style="margin-top:0; color:{C_ACCENT} !important;">FLUJO DE SERVICIO</h4>
            <div style="margin-top:20px;">
                <p style="margin-bottom:12px;"><b>1. DIGITAL LOCKER</b><br><span class="small-text">Escaneo biométrico único.</span></p>
                <p style="margin-bottom:12px;"><b>2. CATÁLOGO</b><br><span class="small-text">Configuración de tela y diseño.</span></p>
                <p style="margin-bottom:0;"><b>3. ENTREGA</b><br><span class="small-text">En tu puerta en 48 hrs.</span></p>
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
                # Animación de carga High Tech
                progreso = st.progress(0, text="Handshake seguro...")
                time.sleep(0.2)
                progreso.progress(45, text="Desencriptando parámetros...")
                time.sleep(0.2)
                progreso.progress(80, text="Renderizando vectores...")
                time.sleep(0.2)
                progreso.empty()
                
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Acceso concedido", icon="🔓")
            else:
                st.error("ID No Reconocido.")
    
    with col_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="premium-card" style="border-left: 6px solid {C_ACCENT};">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="letter-spacing:1px; text-transform:uppercase; margin-top:5px; font-size:0.85rem;" class="small-text">
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
                fig.add_trace(go.Scatterpolar(r=STANDARD_DATA, theta=categories, name='Promedio', line_color='#4B5563', line_dash='dot'))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 110], color='white'), 
                        bgcolor='rgba(0,0,0,0)' # Fondo transparente
                    ),
                    showlegend=True, height=350, margin=dict(l=40, r=40, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', family="Inter")
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
        <div class="premium-card" style="text-align:center;">
            <div style="height:150px; width:100%; background-color:{color_hex}; border-radius:12px; border:1px solid #30363D; margin-bottom:25px; box-shadow: 0 0 20px {color_hex}40;"></div>
            <h1 style="color:{C_ACCENT} !important; margin:0; font-size:4rem; line-height:1; letter-spacing:-2px;">{precio} Bs.</h1>
            <p class="small-text" style="font-size:0.9rem; margin-bottom:20px; font-weight:600; letter-spacing:1px;">PRECIO FINAL</p>
            <div style="text-align:left; background-color:{C_BG_MAIN}; padding:20px; border-radius:12px; border:1px solid {C_BORDER};">
                <p style="margin:5px 0;">🏷️ <b>Línea:</b> {linea.split('(')[0]}</p>
                <p style="margin:5px 0;">🧵 <b>Tela:</b> {nombre_tela_sel}</p>
                <p style="margin:5px 0;">🎨 <b>Color:</b> {color_nom}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A MI BOLSA"):
            # Notificaciones con estilo Oscuro
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
        # Tabla estilizada
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total = df['Precio'].sum()
        
        # Totalizador visual
        st.markdown(f"""
        <div style="text-align:right; padding:30px; background-color:{C_BG_CARD}; border-radius:16px; border:1px solid {C_BORDER}; margin-bottom:40px;">
            <span style="font-size:1.2rem;" class="small-text">TOTAL A PAGAR:</span>
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
                    
                    # --- RECIBO DIGITAL TIPO TICKET DARK MODE ---
                    numero_orden = f"ORD-{random.randint(10000, 99999)}"
                    st.success("¡TRANSACCIÓN EXITOSA!")
                    
                    st.markdown(f"""
                    <div class="digital-receipt">
                        <h2 style="color:#10B981 !important; margin:0; font-size:1.5rem;">✅ ORDEN CONFIRMADA</h2>
                        <p style="color:#D1FAE5 !important; font-size:1.2rem; font-weight:bold; letter-spacing:1px; margin-top:10px;">ID: {numero_orden}</p>
                        <hr style="border-top:1px dashed #10B981; margin:20px 0;">
                        <div style="text-align:left; color:#D1FAE5 !important;">
                            <p><b>Cliente:</b> {st.session_state.usuario['nombre']}</p>
                            <p><b>Estado:</b> EN COLA DE PRODUCCIÓN</p>
                            <p><b>Entrega Estimada:</b> 24-48 Horas</p>
                            <p><b>Total:</b> {total} Bs.</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.carrito = []
                else:
                    st.error("⚠️ ERROR: No se detectó un perfil biométrico activo. Por favor vaya a 'DIGITAL LOCKER' e ingrese su ID.")
    else:
        st.info("Su bolsa de compras está vacía.")
