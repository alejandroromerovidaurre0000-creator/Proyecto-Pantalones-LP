import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL (MODO "ANTIBUG")
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES
C_BLACK = "#1a1a1a"
C_ACCENT = "#5B2C6F" # Morado oscuro elegante
C_BG_SIDEBAR = "#F7F9F9"
C_WHITE = "#FFFFFF"

# CSS PERSONALIZADO (SOLUCIÓN ERROR TRANSPARENCIA)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');
    
    /* FORZAR MODO CLARO SIEMPRE (Evita bugs de modo oscuro) */
    [data-testid="stAppViewContainer"] {{
        background-color: {C_WHITE};
        color: {C_BLACK};
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* FORZAR TEXTO NEGRO EN TODOS LADOS */
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        color: {C_BLACK} !important;
    }}
    
    /* HEADER LIMPIO */
    .header-box {{
        text-align: center;
        padding: 30px 0;
        margin-bottom: 30px;
        border-bottom: 1px solid #eee;
        background-color: {C_WHITE};
    }}
    .header-title {{
        font-size: 3rem;
        font-weight: 800;
        color: {C_BLACK} !important;
        letter-spacing: -1px;
        margin: 0;
        line-height: 1.1;
    }}
    .header-sub {{
        font-size: 0.9rem;
        color: #666 !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 10px;
    }}
    
    /* AJUSTE PARA MÓVILES */
    @media (max-width: 768px) {{
        .header-title {{ font-size: 2rem; }}
        .header-sub {{ letter-spacing: 1px; font-size: 0.7rem; }}
        .big-price {{ font-size: 2.5rem !important; }}
    }}
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: {C_BG_SIDEBAR};
        border-right: 1px solid #e0e0e0;
    }}
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: {C_BLACK} !important;
    }}
    
    /* TARJETAS */
    .card {{
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        height: 100%;
    }}
    
    /* MUESTRAS DE COLOR */
    .swatch {{
        height: 60px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #ddd;
        cursor: pointer;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    }}
    
    /* PRECIO GRANDE */
    .big-price {{
        font-size: 3.5rem;
        font-weight: 800;
        color: {C_ACCENT} !important;
        line-height: 1;
    }}
    
    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK} !important;
        color: white !important;
        border-radius: 6px;
        height: 55px;
        font-weight: 600;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.2s;
    }}
    .stButton>button:hover {{ background-color: {C_ACCENT} !important; transform: translateY(-2px); }}
    
    /* TEXTO DE MENSAJES (TOAST/SUCCESS) */
    .stToast {{ color: {C_BLACK} !important; }}
    
    /* Ocultar elementos extra */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebarNav"] {{display: none !important;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS DE CLIENTES
# ==============================================================================
DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'cargo': 'Postulante',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42, 'fit': 'Slim Fit',
        'radar_data': [82, 96, 54, 104, 26]
    },
    '1002': { # Panelista
        'nombre': 'Samael Gómez Rúa', 'cargo': 'Panelista',
        'cintura': 94, 'largo': 100, 'cadera': 105, 'muslo': 62, 'tiro': 28, 'rodilla': 46, 'fit': 'Regular Comfort',
        'radar_data': [94, 105, 62, 100, 28]
    },
    '1003': { # Tutora
        'nombre': 'Jessica Susana Daza', 'cargo': 'Tutora',
        'cintura': 70, 'largo': 95, 'cadera': 92, 'muslo': 50, 'tiro': 24, 'rodilla': 38, 'fit': 'Relaxed Fit',
        'radar_data': [70, 92, 50, 95, 24]
    },
    '1004': { # Relator
        'nombre': 'Miguel Vidal Sejas', 'cargo': 'Relator',
        'cintura': 88, 'largo': 102, 'cadera': 100, 'muslo': 58, 'tiro': 27, 'rodilla': 44, 'fit': 'Tailored Fit',
        'radar_data': [88, 100, 58, 102, 27]
    }
}
# Medidas promedio
STANDARD_REF = [85, 100, 58, 100, 27]

# Estado de la sesión
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'page' not in st.session_state: st.session_state.page = "INICIO"

# ==============================================================================
# 3. BARRA LATERAL (NAVEGACIÓN)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size: 50px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#333; margin:0;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menú limpio
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("🔐 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("🛠️ DISEÑAR PRODUCTO"): st.session_state.page = "CATALOGO"
    if st.button("🛒 BOLSA DE COMPRA"): st.session_state.page = "CARRITO"
    
    st.markdown("---")
    
    # Créditos Académicos (Formato Oficial)
    st.caption("**Postulante:** Alejandro M. Romero")
    with st.expander("Tribunal Evaluador", expanded=True):
        st.markdown("**Tutora:** Jessica Daza Morales")
        st.markdown("**Panelista:** Samael Gómez Rúa")
        st.markdown("**Relator:** Miguel Vidal Sejas")

# ==============================================================================
# 4. PÁGINAS
# ==============================================================================

# --- PÁGINA 1: INICIO ---
if st.session_state.page == "INICIO":
    st.markdown("""
    <div class="header-box">
        <h1 class="header-title">PANTALONERÍA INTEGRAL</h1>
        <p class="header-sub">Ingeniería de Confort & Sastrería Digital</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Modernos
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Biometría 3D")
    k2.metric("Producción", "24 - 48 Hrs", "Local")
    k3.metric("Materiales", "Certificados", "Alta Gama")
    
    st.divider()
    
    c_left, c_right = st.columns([1.5, 1])
    with c_left:
        st.markdown("### 💎 NUESTRA VISIÓN")
        st.write("""
        Hemos digitalizado la sastrería tradicional.
        
        **1. Cero Trajes:** Nos especializamos 100% en el pantalón masculino.
        **2. Ajuste Perfecto:** Eliminamos las tallas S/M/L usando moldería paramétrica.
        """)
        
        st.info("✅ **ESTÁNDAR DE CALIDAD:** Todos nuestros pantalones, sin excepción, incluyen forrería interna de **Popelina 100% Algodón**. Esto garantiza frescura y evita alergias (a diferencia del poliéster comercial).")
        
    with c_right:
        st.markdown("""
        <div class="card">
            <h4>PASOS SIMPLES</h4>
            <p>1️⃣ <b>Escaneo:</b> Visita única a tienda.</p>
            <p>2️⃣ <b>Diseño:</b> Elige tela desde tu móvil.</p>
            <p>3️⃣ <b>Entrega:</b> En tu puerta en 48 hrs.</p>
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA 2: DIGITAL LOCKER ---
elif st.session_state.page == "LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER")
    st.caption("Base de Datos y Perfil Biométrico.")
    
    c_login, c_dash = st.columns([1, 2.5])
    
    with c_login:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID Cliente", placeholder="Ej: 1004")
        if st.button("BUSCAR PERFIL"):
            if id_user in DB_CLIENTES:
                # Simulación de carga tecnológica
                progress_text = "Conectando con base de datos..."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text="Escaneando parámetros biométricos...")
                time.sleep(0.5)
                my_bar.empty()
                
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.success("¡Acceso Concedido!")
            else:
                st.error("ID No Encontrado.")
    
    with c_dash:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Header del Cliente
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid {C_ACCENT}; margin-bottom: 20px;">
                <h2 style="margin:0; color:{C_ACCENT} !important;">{u['nombre']}</h2>
                <p style="color:#555; margin:0;">{u['cargo'].upper()} | PERFIL VERIFICADO</p>
                <hr>
                <p><b>FIT ASIGNADO:</b> {u['fit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c_chart, c_data = st.columns([1.2, 1])
            
            with c_chart:
                st.markdown("#### 📊 Análisis de Ingeniería")
                # Gráfico Radar
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                      r=u['radar_data'], theta=categories, fill='toself', name='Cliente', line_color=C_ACCENT
                ))
                fig.add_trace(go.Scatterpolar(
                      r=STANDARD_REF, theta=categories, name='Estándar', line_color='#ccc', line_dash='dot'
                ))
                fig.update_layout(
                  polar=dict(
                      radialaxis=dict(visible=True, range=[0, 120]),
                      bgcolor='white' # Fondo blanco forzado para el gráfico
                  ),
                  showlegend=True, height=300, margin=dict(l=40, r=40, t=20, b=20),
                  paper_bgcolor='rgba(0,0,0,0)',
                  font=dict(color='black') # Texto negro forzado en gráfico
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with c_data:
                st.markdown("#### 📐 Medidas (cm)")
                m1, m2 = st.columns(2)
                m1.metric("Cintura", u['cintura'])
                m2.metric("Largo", u['largo'])
                m1.metric("Cadera", u['cadera'])
                m2.metric("Tiro", u['tiro'])
                m1.metric("Muslo", u['muslo'])
                m2.metric("Rodilla", u['rodilla'])
                
                st.success("✅ Patrones DXF listos.")

        else:
            st.info("🔒 Ingrese ID a la izquierda para cargar datos.")

# --- PÁGINA 3: CATÁLOGO ---
elif st.session_state.page == "CATALOGO":
    st.markdown("## 🛠️ DISEÑO DE PRODUCTO")
    
    if st.session_state.usuario:
        st.caption(f"Diseñando para: **{st.session_state.usuario['nombre']}**")
    
    col_conf, col_view = st.columns([1, 1])
    
    with col_conf:
        st.subheader("1. SELECCIONA LÍNEA")
        linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
        
        # Mapeo de Precios EXACTOS
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
        # Selector de llaves (Nombres de tela)
        nombre_tela = st.radio("Opciones:", list(opciones_telas.keys()))
        
        # Obtener precio del diccionario
        precio_final = opciones_telas[nombre_tela]
        
        st.subheader("3. COLOR")
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1B2631", "Kaki Oficina": "#D0D3D4", "Verde Olivo": "#4D5645"}
        else:
            colores = {"Gris Oxford": "#566573", "Negro Profundo": "#000000", "Azul Noche": "#154360"}
            
        nombre_color = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        hex_color = colores[nombre_color]

    with col_view:
        st.subheader("RESUMEN")
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div class="swatch" style="background-color:{hex_color};"></div>
            <p style="margin-top:20px; color:#888;">PRECIO FINAL</p>
            <div class="big-price">{precio_final} Bs.</div>
            <hr>
            <p style="font-weight:bold;">{linea}</p>
            <p>{nombre_tela}</p>
            <p>{nombre_color}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("AÑADIR A BOLSA DE COMPRA"):
            st.session_state.carrito.append({
                "Línea": linea, "Tela": nombre_tela, "Color": nombre_color, "Precio": precio_final
            })
            st.balloons()
            st.toast("Producto Agregado")

# --- PÁGINA 4: CARRITO ---
elif st.session_state.page == "CARRITO":
    st.markdown("## 🛒 BOLSA DE COMPRA")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:{C_ACCENT} !important;'>TOTAL: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Envío")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
            st.text_area("Dirección Exacta", placeholder="Calle, Nro, Edificio...")
            st.text_input("Referencia Visual", placeholder="Color de puerta, tienda cercana...")
        with c2:
            st.text_input("Celular de Contacto")
            st.selectbox("Método de Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR PEDIDO"):
                if st.session_state.usuario:
                    with st.spinner("Procesando Orden de Corte..."):
                        time.sleep(2)
                    st.success("¡PEDIDO CONFIRMADO!")
                    st.info(f"Gracias {st.session_state.usuario['nombre']}. Nos contactaremos para coordinar la entrega.")
                    st.session_state.carrito = []
                else:
                    st.error("Por favor, identifíquese en 'PERFIL BIOMÉTRICO' antes de finalizar.")
    else:
        st.info("Su bolsa está vacía.")
