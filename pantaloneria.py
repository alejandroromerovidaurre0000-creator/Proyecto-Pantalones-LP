import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO PLATINUM - ANTI DARK MODE TOTAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES PREMIUM
C_BLACK = "#0a0a0a"   
C_WHITE = "#FFFFFF"   
C_ACCENT = "#5B2C6F"  # Morado Corporativo
C_SOFT_BG = "#F9FAFB" # Gris muy tenue para fondos

# CSS NUCLEAR V3: CORRECCIÓN DE NOTIFICACIONES Y MENÚS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* 1. RESET GLOBAL: FUENTE PREMIUM Y COLORES */
    .stApp {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        font-family: 'Inter', sans-serif;
    }}
    
    /* 2. TEXTOS GLOBALES EN NEGRO */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {{
        color: {C_BLACK} !important;
    }}
    
    /* 3. ARREGLO CRÍTICO: NOTIFICACIONES (TOASTS) */
    div[data-testid="stToast"] {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border-left: 6px solid {C_ACCENT} !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
        border-radius: 8px !important;
        opacity: 1 !important;
    }}
    /* Forzar texto dentro del toast a negro */
    div[data-testid="stToast"] p, div[data-testid="stToast"] span {{
        color: {C_BLACK} !important;
    }}
    
    /* 4. ARREGLO CRÍTICO: MENÚS DESPLEGABLES (SELECTBOX) */
    /* El contenedor del menú */
    div[data-baseweb="select"] > div {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
    }}
    /* La lista de opciones que se despliega */
    div[data-baseweb="popover"] {{
        background-color: {C_WHITE} !important;
    }}
    ul[data-baseweb="menu"] {{
        background-color: {C_WHITE} !important;
    }}
    /* Cada opción individual */
    li[data-baseweb="option"] {{
        color: {C_BLACK} !important;
        background-color: {C_WHITE} !important;
    }}
    /* Cuando pasas el dedo por encima de una opción */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {{
        background-color: {C_SOFT_BG} !important;
        font-weight: bold !important;
    }}
    /* El texto seleccionado */
    div[data-baseweb="select"] span {{
        color: {C_BLACK} !important;
    }}
    
    /* 5. SIDEBAR LIMPIO */
    [data-testid="stSidebar"] {{
        background-color: #f8f9fa !important;
        border-right: 1px solid #eee;
    }}
    [data-testid="stSidebar"] * {{
        color: {C_BLACK} !important;
    }}
    /* Arreglo flecha cerrar menú */
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: {C_BLACK} !important;
    }}
    
    /* 6. BOTONES ESTILO SOFTWARE MODERNO */
    .stButton > button {{
        background-color: {C_BLACK} !important;
        color: {C_WHITE} !important; 
        border-radius: 8px !important;
        height: 55px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background-color: {C_ACCENT} !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(91, 44, 111, 0.2) !important;
    }}
    .stButton > button p {{
        color: {C_WHITE} !important; 
    }}
    
    /* 7. TARJETAS CON SOMBRA SUAVE (GLASSMORPHISM LITE) */
    .info-card {{
        background-color: {C_WHITE} !important;
        border: 1px solid #f0f0f0;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }}
    .info-card:hover {{
        transform: translateY(-2px);
    }}
    
    /* 8. INPUTS MEJORADOS */
    .stTextInput input, .stTextArea textarea {{
        background-color: {C_WHITE} !important;
        color: {C_BLACK} !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
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
# 3. BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size: 45px;'>🧵</div>", unsafe_allow_html=True)
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
    <div style="text-align:center; padding:40px 20px; border-bottom:1px solid #eee; margin-bottom:30px;">
        <h1 style="font-size: 3rem; font-weight: 900; margin:0; line-height:1.1; letter-spacing:-1px;">PANTALONERÍA INTEGRAL</h1>
        <p style="letter-spacing:1px; margin-top:15px; color:#555; text-transform:uppercase; font-size:0.9rem;">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
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
        st.markdown("""
        <div class="info-card">
            <h4 style="margin-top:0;">PASOS</h4>
            <p style="margin-bottom:8px;">1️⃣ <b>Escaneo:</b> Visita única a tienda.</p>
            <p style="margin-bottom:8px;">2️⃣ <b>Diseño:</b> Elige tela y color.</p>
            <p style="margin-bottom:0;">3️⃣ <b>Entrega:</b> En tu puerta.</p>
        </div>
        """, unsafe_allow_html=True)

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
                # Simulación de carga "Software Caro"
                progreso = st.progress(0, text="Conectando Servidor Seguro...")
                time.sleep(0.3)
                progreso.progress(30, text="Desencriptando Biometría...")
                time.sleep(0.3)
                progreso.progress(75, text="Renderizando Moldería...")
                time.sleep(0.3)
                progreso.empty()
                
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Acceso concedido a: {st.session_state.usuario['nombre']}", icon="✅")
            else:
                st.error("ID No encontrado.")
    
    with col_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="info-card" style="border-left: 6px solid {C_ACCENT};">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="letter-spacing:1px; text-transform:uppercase; margin-top:5px; color:#666 !important;">{u['cargo']} | ID: {id_user}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
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
        
        opciones_telas = {}
        desc = ""
        
        if "ESTÁNDAR" in linea:
            opciones_telas = {
                "Gabardina Spandex (97% Alg)": 220,
                "Dril Confort (Algodón)": 240
            }
            desc = "Tejidos resistentes con elastano."
        else:
            opciones_telas = {
                "Lana Fría Super 100's": 420,
                "Casimir Importado": 450
            }
            desc = "Tejidos nobles importados. Caída sastre."
            
        st.caption(f"ℹ️ {desc}")
        
        st.subheader("2. MATERIAL")
        nombre_tela_sel = st.radio("Opciones:", list(opciones_telas.keys()))
        precio = opciones_telas[nombre_tela_sel]
        
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
            <div style="height:120px; width:100%; background-color:{color_hex}; border-radius:8px; border:2px solid #e0e0e0; box-shadow: inset 0 0 20px rgba(0,0,0,0.05); margin-bottom:20px;"></div>
            <h1 style="color:{C_ACCENT} !important; margin:0; font-size:3.5rem;">{precio} Bs.</h1>
            <p style="margin-top:10px;"><b>{linea}</b></p>
            <p>{nombre_tela_sel}</p>
            <p>{color_nom}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A LA BOLSA"):
            # Secuencia de Notificaciones de Ingeniería (Estilo Software)
            st.toast("📐 Cargando parámetros biométricos...", icon="👤")
            time.sleep(0.6)
            st.toast("✂️ Calculando consumo de tela...", icon="🧵")
            time.sleep(0.6)
            st.toast("✅ ¡Ítem agregado a la orden de producción!", icon="🛍️")
            
            st.session_state.carrito.append({
                "Línea": linea, "Tela": nombre_tela_sel, "Color": color_nom, "Precio": precio
            })

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
