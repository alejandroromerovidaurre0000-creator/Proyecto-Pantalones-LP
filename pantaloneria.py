import streamlit as st
import pandas as pd
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN CORPORATIVA (MODO DEFENSA FINAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES "LUJO ACCESIBLE"
C_BLACK = "#101010"
C_VIOLET = "#5B2C6F" # Color de identidad
C_GOLD = "#D4AC0D"
C_BG = "#FFFFFF"

# ESTILOS CSS (DISEÑO LIMPIO Y SIN ERRORES)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap');
    
    .stApp {{
        background-color: {C_BG};
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* LOGO DIGITAL (REEMPLAZA LA IMAGEN PARA QUE NO FALLE) */
    .brand-header {{
        text-align: center;
        padding: 40px 0;
        border-bottom: 4px solid {C_VIOLET};
        margin-bottom: 30px;
        background: linear-gradient(to bottom, #fdfdfd, #f0f0f0);
    }}
    .brand-name {{
        font-size: 3.5rem;
        font-weight: 900;
        color: {C_BLACK};
        letter-spacing: -1px;
        text-transform: uppercase;
        margin: 0;
        line-height: 1;
    }}
    .brand-sub {{
        font-size: 1.2rem;
        color: #666;
        letter-spacing: 3px;
        margin-top: 10px;
        font-weight: 300;
    }}
    
    /* TARJETAS DE DATOS */
    .info-card {{
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        transition: transform 0.2s;
    }}
    .info-card:hover {{ transform: translateY(-3px); border-color: {C_VIOLET}; }}
    
    /* CAJAS DE COLOR (SWATCHES) - NO IMAGENES */
    .color-box {{
        height: 100px;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #ddd;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
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

    /* OCULTAR MENÚS POR DEFECTO */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (TRIBUNAL ACADÉMICO REAL)
# ==============================================================================
DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'cargo': 'Fundador',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42, 'fit': 'Slim Fit'
    },
    '1002': { # Panelista
        'nombre': 'Samael Gómez Rúa', 'cargo': 'Panelista',
        'cintura': 94, 'largo': 100, 'cadera': 105, 'muslo': 62, 'tiro': 28, 'rodilla': 46, 'fit': 'Regular Comfort'
    },
    '1003': { # Tutora
        'nombre': 'Jessica Susana Daza', 'cargo': 'Tutora',
        'cintura': 70, 'largo': 95, 'cadera': 92, 'muslo': 50, 'tiro': 24, 'rodilla': 38, 'fit': 'Relaxed Fit'
    },
    '1004': { # Relator
        'nombre': 'Miguel Vidal Sejas', 'cargo': 'Relator',
        'cintura': 88, 'largo': 102, 'cadera': 100, 'muslo': 58, 'tiro': 27, 'rodilla': 44, 'fit': 'Tailored Fit'
    }
}

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# ==============================================================================
# 3. BARRA LATERAL (CRÉDITOS & NAVEGACIÓN)
# ==============================================================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size: 50px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcion = st.radio("MENÚ", ["INICIO", "DIGITAL LOCKER", "COLECCIÓN & COMPRA", "MI PEDIDO"], label_visibility="collapsed")
    
    st.markdown("---")
    st.caption("Proyecto de Grado UCB 2026")
    st.caption("**Postulante:** Alejandro M. Romero V.")
    
    with st.expander("Tribunal Evaluador", expanded=True):
        st.markdown("**Tutora:** Jessica Daza Morales")
        st.markdown("**Panelista:** Samael Gómez Rúa")
        st.markdown("**Relator:** Miguel Vidal Sejas")

# ==============================================================================
# 4. PÁGINAS DEL SISTEMA
# ==============================================================================

# --- INICIO ---
if opcion == "INICIO":
    # LOGO GRANDE (CSS)
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-name">PANTALONERÍA INTEGRAL</h1>
        <p class="brand-sub">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Precisión", "99.9%", "Biometría 3D")
    c2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    c3.metric("Materiales", "Certificados", "Alta Calidad")
    
    st.divider()
    
    col_txt, col_cta = st.columns([1.5, 1])
    with col_txt:
        st.markdown("### 💎 PROPUESTA DE VALOR")
        st.write("""
        Revolucionamos la industria textil masculina con un modelo **Phygital**.
        
        * **Cero Trajes:** Nos especializamos 100% en el pantalón.
        * **Cero Tallas Genéricas:** Cada prenda se corta con tu moldería digital única.
        """)
        st.info("✅ **GARANTÍA TÉCNICA (Pág. 115):** Todos nuestros pantalones incluyen forrería de **Popelina 100% Algodón** para máxima frescura e higiene.")
    
    with col_cta:
        st.success("1. **DIGITAL LOCKER:** Escaneamos tus medidas una vez.")
        st.info("2. **CONFIGURADOR:** Eliges tela y línea (Estándar/Premium).")
        st.warning("3. **ENTREGA:** En tu puerta en 24-48 horas.")

# --- DIGITAL LOCKER ---
elif opcion == "DIGITAL LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER")
    st.caption("Base de datos de moldería personalizada.")
    
    col_in, col_out = st.columns([1, 2.5])
    
    with col_in:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID Cliente", placeholder="Ej: 1004")
        if st.button("AUTENTICAR"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Bienvenido {st.session_state.usuario['nombre']}", icon="🔓")
            else:
                st.error("ID No encontrado.")
                
    with col_out:
        if st.session_state.usuario:
            u = st.session_state.usuario
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #101010;">
                <h2 style="margin:0; color:#5B2C6F;">{u['nombre']}</h2>
                <p style="text-transform:uppercase; letter-spacing:1px; color:#555;">{u['cargo']} | PERFIL VERIFICADO</p>
                <hr>
                <p><b>FIT ASIGNADO:</b> {u['fit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📐 ESPECIFICACIONES TÉCNICAS (CM)")
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cintura']}</div><div class='metric-lbl'>Cintura</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cadera']}</div><div class='metric-lbl'>Cadera</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-box'><div class='metric-val'>{u['largo']}</div><div class='metric-lbl'>Largo</div></div>", unsafe_allow_html=True)
            m4.markdown(f"<div class='metric-box'><div class='metric-val'>{u['tiro']}</div><div class='metric-lbl'>Tiro</div></div>", unsafe_allow_html=True)
            m5.markdown(f"<div class='metric-box'><div class='metric-val'>{u['muslo']}</div><div class='metric-lbl'>Muslo</div></div>", unsafe_allow_html=True)
            m6.markdown(f"<div class='metric-box'><div class='metric-val'>{u['rodilla']}</div><div class='metric-lbl'>Rodilla</div></div>", unsafe_allow_html=True)
            
            st.success("✅ Patrones digitales listos para corte automático.")
        else:
            st.info("🔒 Sistema protegido. Ingrese un ID válido.")

# --- COLECCIÓN ---
elif opcion == "COLECCIÓN & COMPRA":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.success(f"Diseñando para: **{st.session_state.usuario['nombre']}**")
    
    # 1. LÍNEA
    st.subheader("1. SELECCIONA LA LÍNEA")
    linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
    
    precio = 0
    telas = []
    desc = ""
    
    if "ESTÁNDAR" in linea:
        telas = ["Gabardina Spandex (220 Bs.)", "Dril Confort (240 Bs.)"]
        desc = "Tejidos resistentes con elastano para movilidad diaria."
    else:
        telas = ["Lana Fría Super 100's (420 Bs.)", "Casimir Importado (450 Bs.)"]
        desc = "Tejidos nobles importados. Termicidad regulada y caída perfecta."
        
    st.caption(f"ℹ️ {desc}")
    
    col_conf1, col_conf2 = st.columns(2)
    
    with col_conf1:
        # 2. TELA
        st.markdown("#### 2. MATERIAL")
        tela_sel = st.radio("Opciones:", telas)
        precio = int(''.join(filter(str.isdigit, tela_sel)))
        
    with col_conf2:
        # 3. COLOR (SWATCHES CSS)
        st.markdown("#### 3. COLOR")
        
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1B2631", "Kaki Oficina": "#D0D3D4", "Verde Olivo": "#4D5645"}
        else:
            colores = {"Gris Oxford": "#566573", "Negro Profundo": "#000000", "Azul Noche": "#154360"}
            
        color_nom = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        color_hex = colores[color_nom]
        
        st.markdown(f"<div class='color-box' style='background-color:{color_hex};'></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    c_pr, c_btn = st.columns([1, 1])
    with c_pr:
        st.markdown(f"### PRECIO FINAL: {precio} Bs.")
    with c_btn:
        st.write("")
        if st.button("AÑADIR A LA BOLSA"):
            st.session_state.carrito.append({
                "Línea": linea, "Tela": tela_sel.split("(")[0], "Color": color_nom, "Precio": precio
            })
            st.balloons()
            st.toast("Agregado")

# --- PEDIDO ---
elif opcion == "MI PEDIDO":
    st.markdown("## 🛒 FINALIZAR COMPRA")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:#5B2C6F;'>TOTAL: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Entrega")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona de Entrega", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
            st.text_area("Dirección Exacta", placeholder="Calle, Nro, Edificio...")
            st.text_input("Referencia Visual", placeholder="Ej: Portón café, frente al parque...")
        with c2:
            st.text_input("WhatsApp de Contacto")
            st.selectbox("Método de Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR PEDIDO"):
                with st.spinner("Procesando..."):
                    time.sleep(2)
                st.success("¡PEDIDO CONFIRMADO!")
                st.info("Nos contactaremos vía WhatsApp para coordinar la entrega.")
                st.session_state.carrito = []
    else:
        st.warning("Carrito vacío.")
