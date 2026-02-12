import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN E IDENTIDAD (OFICIAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES
C_BLACK = "#101010"
C_VIOLET = "#6C3483"
C_GRAY_BG = "#FAFAFA"

# CSS (DISEÑO LIMPIO)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }}
    
    /* LOGO GRANDE */
    .brand-header {{
        text-align: center;
        padding: 40px 0;
        margin-bottom: 30px;
        background: radial-gradient(circle, #f8f9fa 0%, #ffffff 100%);
        border-bottom: 1px solid #ddd;
    }}
    .brand-name {{
        font-size: 3.5rem;
        font-weight: 900;
        color: {C_BLACK};
        letter-spacing: -2px;
        text-transform: uppercase;
        margin: 0;
    }}
    .brand-sub {{
        font-size: 1.1rem;
        color: #666;
        letter-spacing: 4px;
        margin-top: 5px;
    }}
    
    /* TARJETAS DE DATOS */
    .info-card {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #eee;
    }}
    
    /* CAJAS DE COLOR (SWATCHES) */
    .color-box {{
        height: 80px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
        cursor: pointer;
    }}
    
    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 4px;
        height: 55px;
        font-weight: 700;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{ background-color: {C_VIOLET}; }}

    /* OCULTAR ELEMENTOS EXTRA */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebarNav"] {{display: none !important;}} /* Ocultar nav automática */
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (TRIBUNAL ACADÉMICO)
# ==============================================================================
# Datos biométricos + Datos para el Gráfico Radar (Values vs Standard)
DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'cargo': 'Fundador',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42, 'fit': 'Slim Fit',
        'radar_data': [82, 96, 54, 104, 26] # Datos reales
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
# Medidas estándar de referencia (Talla M Promedio) para comparar en el gráfico
STANDARD_DATA = [84, 98, 56, 100, 26]

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'page' not in st.session_state: st.session_state.page = "INICIO"

# ==============================================================================
# 3. BARRA LATERAL (NUEVA NAVEGACIÓN LIMPIA)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size: 50px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Botones de navegación manual para control total
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("👤 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("👖 CATÁLOGO & DISEÑO"): st.session_state.page = "CATALOGO"
    if st.button("🛒 BOLSA DE COMPRAS"): st.session_state.page = "CARRITO"
    
    st.markdown("---")
    st.caption("**Postulante:** Alejandro M. Romero V.")
    
    with st.expander("Tribunal Evaluador", expanded=True):
        st.markdown("• Tutora: Jessica Daza Morales")
        st.markdown("• Panelista: Samael Gómez Rúa")
        st.markdown("• Relator: Miguel Vidal Sejas")

# ==============================================================================
# 4. PÁGINAS DEL SISTEMA
# ==============================================================================

# --- PÁGINA: INICIO ---
if st.session_state.page == "INICIO":
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-name">PANTALONERÍA INTEGRAL</h1>
        <p class="brand-sub">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Escáner 3D")
    k2.metric("Entrega", "24 - 48 Hrs", "Express")
    k3.metric("Materiales", "Certificados", "Alta Gama")
    
    st.divider()
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 LA PROPUESTA DE VALOR")
        st.write("""
        Revolucionamos la industria textil masculina. 
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas.
        """)
        st.info("✅ **GARANTÍA TÉCNICA (Pág. 115):** Todos nuestros pantalones incluyen forrería de **Popelina 100% Algodón** para máxima frescura e higiene.")
    
    with c_steps:
        st.success("1. **DIGITAL LOCKER:** Escaneo de medidas.")
        st.info("2. **CONFIGURADOR:** Elige tela y color.")
        st.warning("3. **ENTREGA:** En tu puerta en 48 hrs.")

# --- PÁGINA: DIGITAL LOCKER (GRÁFICO DE INGENIERÍA) ---
elif st.session_state.page == "LOCKER":
    st.markdown("## 🔐 PERFIL BIOMÉTRICO (DIGITAL LOCKER)")
    
    col_auth, col_info = st.columns([1, 2.5])
    
    with col_auth:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID Cliente", placeholder="Ej: 1004")
        if st.button("CONSULTAR BASE DE DATOS"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Perfil Cargado", icon="✅")
            else:
                st.error("ID No encontrado.")
    
    with col_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Encabezado Perfil
            st.markdown(f"""
            <div class="info-card">
                <h2 style="margin:0; color:#5B2C6F;">{u['nombre']}</h2>
                <p style="color:#555; letter-spacing:1px; text-transform:uppercase;">{u['cargo']} | ID: {id_user}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            # DIAGRAMA DE RADAR (GRÁFICO DE INGENIERÍA)
            c_chart, c_metrics = st.columns([1.2, 1])
            
            with c_chart:
                st.markdown("#### 📊 Análisis de Morfología vs Estándar")
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                
                fig = go.Figure()
                # Linea del Cliente
                fig.add_trace(go.Scatterpolar(
                      r=u['radar_data'],
                      theta=categories,
                      fill='toself',
                      name=u['nombre'],
                      line_color='#5B2C6F'
                ))
                # Linea Estándar (Comparativa)
                fig.add_trace(go.Scatterpolar(
                      r=STANDARD_DATA,
                      theta=categories,
                      name='Talla M (Ref)',
                      line_color='#BDC3C7',
                      line_dash='dot'
                ))
                fig.update_layout(
                  polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
                  showlegend=True,
                  height=350,
                  margin=dict(l=30, r=30, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("*Este diagrama muestra por qué la ropa estándar no le queda bien al cliente.*")

            with c_metrics:
                st.markdown("#### 📐 Especificaciones Técnicas (cm)")
                # Métricas detalladas
                col_a, col_b = st.columns(2)
                col_a.metric("Cintura", f"{u['cintura']}", "cm")
                col_b.metric("Largo", f"{u['largo']}", "cm")
                col_a.metric("Cadera", f"{u['cadera']}", "cm")
                col_b.metric("Tiro", f"{u['tiro']}", "cm")
                col_a.metric("Muslo", f"{u['muslo']}", "cm")
                col_b.metric("Rodilla", f"{u['rodilla']}", "cm")
                
                st.success(f"✅ FIT ASIGNADO: **{u['fit']}**")

        else:
            st.info("🔒 Sistema en espera. Ingrese ID para cargar moldería.")

# --- PÁGINA: CATÁLOGO ---
elif st.session_state.page == "CATALOGO":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.caption(f"Configurando para: **{st.session_state.usuario['nombre']}**")
    
    # SELECCIÓN
    c_config, c_preview = st.columns([1, 1])
    
    with c_config:
        st.subheader("1. LÍNEA Y PRECIO")
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
        # Visualización abstracta del color
        st.markdown(f"""
        <div class="info-card" style="text-align:center;">
            <div class="color-box" style="background-color:{color_hex}; height:200px;"></div>
            <h1 style="color:{C_VIOLET}; margin-top:20px;">{precio} Bs.</h1>
            <p>{linea}</p>
            <p>{tela_sel.split('(')[0]}</p>
            <p>{color_nom}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("AÑADIR A LA BOLSA"):
            st.session_state.carrito.append({
                "Línea": linea, "Tela": tela_sel.split("(")[0], "Color": color_nom, "Precio": precio
            })
            st.balloons()
            st.toast("Agregado")

# --- PÁGINA: CARRITO ---
elif st.session_state.page == "CARRITO":
    st.markdown("## 🛒 FINALIZAR PEDIDO")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:{C_VIOLET};'>TOTAL: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Logística de Entrega")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
            st.text_area("Dirección Exacta", placeholder="Av. Principal #123, Edificio Azul...")
            st.text_input("Referencia Visual", placeholder="Frente a la Farmacia...")
        with c2:
            st.text_input("Celular / WhatsApp")
            st.selectbox("Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR PEDIDO"):
                if st.session_state.usuario:
                    with st.spinner("Procesando..."):
                        time.sleep(2)
                    st.success("¡PEDIDO CONFIRMADO!")
                    st.info(f"Orden generada para: {st.session_state.usuario['nombre']}. Entrega en 24-48 hrs.")
                    st.session_state.carrito = []
                else:
                    st.error("Por favor, autentíquese en 'PERFIL BIOMÉTRICO' antes de comprar.")
    else:
        st.warning("Bolsa vacía.")
