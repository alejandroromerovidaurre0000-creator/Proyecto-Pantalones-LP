import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN (ESTILO LIMPIO Y PROFESIONAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES
C_BLACK = "#111111"
C_VIOLET = "#6C3483"
C_WHITE = "#FFFFFF"

# CSS (DISEÑO LIMPIO - SIN MARCOS NEGROS PESADOS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }}
    
    /* HEADER PRINCIPAL (Limpio) */
    .brand-header {{
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #eee;
        background: white;
    }}
    .brand-name {{
        font-size: 3rem;
        font-weight: 900;
        color: {C_BLACK};
        letter-spacing: -1px;
        margin: 0;
        text-transform: uppercase;
    }}
    .brand-sub {{
        font-size: 0.9rem;
        color: #888;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 5px;
    }}
    
    /* SIDEBAR (LIMPIO Y BLANCO - YA NO NEGRO) */
    [data-testid="stSidebar"] {{
        background-color: #fcfcfc;
        border-right: 1px solid #e0e0e0;
    }}
    [data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
    }}
    
    /* TARJETAS DE DATOS */
    .info-card {{
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }}
    
    /* CAJAS DE COLOR (SWATCHES) */
    .color-box {{
        height: 70px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        cursor: pointer;
    }}
    
    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 6px;
        height: 50px;
        font-weight: 700;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: {C_VIOLET}; transform: scale(1.01); }}

    /* OCULTAR ELEMENTOS EXTRA */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebarNav"] {{display: none !important;}} 
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (TRIBUNAL ACADÉMICO)
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
# Medidas estándar ref
STANDARD_DATA = [84, 98, 56, 100, 26]

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'page' not in st.session_state: st.session_state.page = "INICIO"

# ==============================================================================
# 3. BARRA LATERAL (MENU LIMPIO Y CARGOS CORRECTOS)
# ==============================================================================
with st.sidebar:
    # Logo minimalista
    st.markdown("<div style='text-align:center; font-size: 50px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; margin-top:0; color:#333;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navegación con botones limpios
    st.caption("NAVEGACIÓN")
    if st.button("🏠 INICIO"): st.session_state.page = "INICIO"
    if st.button("👤 PERFIL BIOMÉTRICO"): st.session_state.page = "LOCKER"
    if st.button("👖 DISEÑAR PANTALÓN"): st.session_state.page = "CATALOGO"
    if st.button("🛒 BOLSA DE COMPRA"): st.session_state.page = "CARRITO"
    
    st.markdown("---")
    
    # CRÉDITOS ACADÉMICOS EXACTOS
    st.caption("PROYECTO DE GRADO")
    st.markdown("**Postulante:** Alejandro M. Romero")
    
    with st.expander("Tribunal Evaluador", expanded=True):
        st.markdown("**Tutora:** Jessica Daza Morales")
        st.markdown("**Panelista:** Samael Gómez Rúa")
        st.markdown("**Relator:** Miguel Vidal Sejas")

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
    
    # Dashboard
    k1, k2, k3 = st.columns(3)
    k1.metric("Precisión", "99.9%", "Biometría")
    k2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    k3.metric("Calidad", "Certificada", "Alta Gama")
    
    st.divider()
    
    c_txt, c_steps = st.columns([1.5, 1])
    with c_txt:
        st.markdown("### 💎 NUESTRA VISIÓN")
        st.write("""
        Revolucionamos la industria textil masculina. 
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas.
        """)
        # Sin mención a tesis, pero resaltando la calidad
        st.info("✅ **ESTÁNDAR DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón** para garantizar frescura, hipoalergencia y durabilidad superior.")
    
    with c_steps:
        st.success("1. **DIGITAL LOCKER:** Escaneo de medidas.")
        st.info("2. **CONFIGURADOR:** Elige tela y color.")
        st.warning("3. **ENTREGA:** En tu puerta en 48 hrs.")

# --- PÁGINA: DIGITAL LOCKER ---
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
            
            # Encabezado Perfil (Mostrando Cargo correctamente)
            st.markdown(f"""
            <div class="info-card">
                <h2 style="margin:0; color:#5B2C6F;">{u['nombre']}</h2>
                <p style="color:#555; letter-spacing:1px; text-transform:uppercase;">{u['cargo']} | ID: {id_user}</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            # DIAGRAMA DE RADAR
            c_chart, c_metrics = st.columns([1.2, 1])
            
            with c_chart:
                st.markdown("#### 📊 Análisis Morfológico")
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                      r=u['radar_data'], theta=categories, fill='toself', name='Cliente', line_color='#5B2C6F'
                ))
                fig.add_trace(go.Scatterpolar(
                      r=STANDARD_DATA, theta=categories, name='Promedio', line_color='#BDC3C7', line_dash='dot'
                ))
                fig.update_layout(
                  polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
                  showlegend=True, height=350, margin=dict(l=30, r=30, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with c_metrics:
                st.markdown("#### 📐 Medidas (cm)")
                col_a, col_b = st.columns(2)
                col_a.metric("Cintura", f"{u['cintura']}")
                col_b.metric("Largo", f"{u['largo']}")
                col_a.metric("Cadera", f"{u['cadera']}")
                col_b.metric("Tiro", f"{u['tiro']}")
                col_a.metric("Muslo", f"{u['muslo']}")
                col_b.metric("Rodilla", f"{u['rodilla']}")
                
                st.success(f"✅ FIT ASIGNADO: **{u['fit']}**")

        else:
            st.info("🔒 Sistema en espera. Ingrese ID para cargar datos.")

# --- PÁGINA: CATÁLOGO ---
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
            <div class="color-box" style="background-color:{color_hex}; height:180px;"></div>
            <h1 style="color:{C_VIOLET}; margin-top:20px;">{precio} Bs.</h1>
            <p><b>{linea}</b></p>
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
            st.text_area("Dirección Exacta", placeholder="Av. Principal #123, Edificio...")
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
                    st.error("Por favor, identifíquese en 'PERFIL BIOMÉTRICO' antes de comprar.")
    else:
        st.info("Su bolsa de compras está vacía.")
