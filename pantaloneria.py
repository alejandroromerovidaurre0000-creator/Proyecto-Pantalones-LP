import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN E IDENTIDAD DE MARCA (COMMERCIAL MODE)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COLORES CORPORATIVOS (Elegancia y Tecnología)
C_BLACK = "#1a1a1a"
C_GOLD = "#D4AC0D" 
C_GRAY = "#F4F6F7"
C_PURPLE = "#5B2C6F" # Toque distintivo

# CSS PARA GENERAR LA INTERFAZ SIN FOTOS
st.markdown(f"""
    <style>
    /* FUENTES Y FONDO */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }}
    
    /* LOGO TIPOGRÁFICO (Reemplaza imagen) */
    .brand-logo {{
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: {C_BLACK};
        text-transform: uppercase;
        border-bottom: 4px solid {C_PURPLE};
        display: inline-block;
        margin-bottom: 20px;
    }}
    
    /* MUESTRAS DE COLOR (SWATCHES) */
    .color-swatch {{
        width: 100%;
        height: 120px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        border: 2px solid #eee;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }}
    .color-swatch:hover {{ transform: scale(1.05); border-color: {C_PURPLE}; }}
    
    /* TARJETAS DE PRECIO */
    .price-card {{
        background: #fafafa;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid {C_PURPLE};
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    
    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 8px;
        padding: 15px;
        font-weight: 600;
        border: none;
        width: 100%;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{ background-color: {C_PURPLE}; }}

    /* ESCONDER ELEMENTOS DE STREAMLIT */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (CLIENTES REALES / JURADO)
# ==============================================================================
# Aquí escondemos los nombres reales para que aparezcan solo al loguearse
DB_CLIENTES = {
    '1001': {'nombre': 'Alejandro Romero', 'tipo': 'Fundador', 'cintura': 82, 'largo': 104, 'fit': 'Slim'},
    '1002': {'nombre': 'Samael Gómez Rúa', 'tipo': 'Cliente VIP', 'cintura': 94, 'largo': 100, 'fit': 'Regular Comfort'}, # Panelista
    '1003': {'nombre': 'Jessica Susana Daza', 'tipo': 'Cliente VIP', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed'}, # Tutora
    '1004': {'nombre': 'Miguel Vidal Sejas', 'tipo': 'Cliente VIP', 'cintura': 88, 'largo': 102, 'fit': 'Tailored Fit'} # Relator
}

# ==============================================================================
# 3. LÓGICA DE PERSONALIZACIÓN
# ==============================================================================

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# --- SIDEBAR (Menú Principal) ---
with st.sidebar:
    st.title("MENÚ PRINCIPAL")
    opcion = st.radio("", ["INICIO", "DIGITAL LOCKER", "CONFIGURADOR", "CARRITO"])
    
    st.markdown("---")
    st.caption("© 2026 PANTALONERÍA INTEGRAL")
    st.caption("La Paz, Bolivia")
    
    # Créditos discretos (Requisito Académico pero sutil)
    with st.expander("Información Corporativa"):
        st.write("Fundador: Alejandro M. Romero")
        st.write("Directorio: Jessica Daza, Samael Gómez, Miguel Vidal.")

# ==============================================================================
# 4. PÁGINAS DEL SITIO
# ==============================================================================

# --- PÁGINA: INICIO ---
if opcion == "INICIO":
    st.markdown('<div class="brand-logo">PANTALONERÍA INTEGRAL</div>', unsafe_allow_html=True)
    st.markdown("### SASTRERÍA DIGITAL & INGENIERÍA TEXTIL")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Precisión de Ajuste", "99.8%", "+ Escaneo 3D")
    col_kpi2.metric("Tiempos de Entrega", "24 Horas", "Express")
    col_kpi3.metric("Materiales", "100% Algodón", "Certificado")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💎 NUESTRA PROMESA")
        st.write("""
        Somos la primera marca en Bolivia especializada **exclusivamente en pantalones**.
        
        Eliminamos los trajes innecesarios y las tallas genéricas (S/M/L) para ofrecerte una prenda construida matemática y anatómicamente para ti.
        """)
        st.info("✅ **GARANTÍA DE CALIDAD:** Todos nuestros pantalones incluyen forrería interna de **Popelina 100% Algodón** para evitar la transpiración y alergias (Estándar de calidad superior).")
    
    with c2:
        st.markdown("#### 🚀 CÓMO FUNCIONA")
        st.success("1. **DIGITAL LOCKER:** Visitamos tu oficina/hogar una sola vez para escanear tus medidas.")
        st.info("2. **CONFIGURADOR:** Eliges tela, color y corte desde esta web.")
        st.warning("3. **ENTREGA:** Recibes tu pantalón perfecto al día siguiente.")

# --- PÁGINA: DIGITAL LOCKER ---
elif opcion == "DIGITAL LOCKER":
    st.markdown("## 🔐 ACCESO BIOMÉTRICO")
    st.write("Sistema de gestión de moldería personalizada.")
    
    col_input, col_display = st.columns([1, 2])
    
    with col_input:
        st.text("Ingrese su ID de Cliente:")
        id_user = st.text_input("ID", placeholder="Ej: 1004", label_visibility="collapsed")
        
        if st.button("AUTENTICAR"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast("Acceso Concedido", icon="🔓")
            else:
                st.error("ID No Reconocido")
                
    with col_display:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="price-card">
                <h1 style="color:#5B2C6F; margin:0;">Hola, {u['nombre']}</h1>
                <p>Nivel: {u['tipo']} | Estado: 🟢 ACTIVO</p>
                <hr>
                <div style="display:flex; justify-content:space-between; text-align:center;">
                    <div><h2>{u['cintura']} cm</h2><small>CINTURA</small></div>
                    <div><h2>{u['largo']} cm</h2><small>LARGO</small></div>
                    <div><h2>{u['fit']}</h2><small>FIT ANATÓMICO</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Sus patrones digitales están cargados y listos para producción.")
        else:
            st.info("🔒 Sistema bloqueado. Ingrese credenciales.")

# --- PÁGINA: CONFIGURADOR (SIN IMÁGENES - PURO CÓDIGO) ---
elif opcion == "CONFIGURADOR":
    st.markdown("## 🛠️ STUDIO DE DISEÑO")
    st.write("Personaliza cada detalle. Sin fotos engañosas, solo materiales reales.")
    
    if st.session_state.usuario:
        st.caption(f"Configurando medidas exactas para: **{st.session_state.usuario['nombre']}**")
    
    # 1. MODELO
    st.subheader("1. SELECCIONA EL CORTE")
    modelo = st.selectbox("Modelo:", ["CHINO (Oficina/Diario)", "5-POCKETS (Casual/Jean)", "SARTORIAL (Vestir/Formal)"])
    
    base_price = 0
    desc = ""
    if "CHINO" in modelo: 
        base_price = 180
        desc = "Bolsillos sesgados. El estándar moderno."
    elif "5-POCKETS" in modelo: 
        base_price = 160
        desc = "Corte de jean, bolsillos parche."
    elif "SARTORIAL" in modelo: 
        base_price = 250
        desc = "Pretina limpia, sin costura visible. Formal."
        
    st.info(f"ℹ️ {desc}")
    
    # 2. TELA
    st.subheader("2. SELECCIONA EL MATERIAL")
    col_telas = st.columns(2)
    with col_telas[0]:
        tela = st.radio("Catálogo de Telas:", 
            ["Gabardina Spandex (97% Algodón)", "Dril Pesado (100% Algodón)", "Lana Fría Super 100's", "Pana (Corduroy)"])
    
    price_add = 0
    if "Lana" in tela: price_add = 200
    if "Pana" in tela: price_add = 50
    if "Dril" in tela: price_add = 20
    
    # 3. COLOR (VISUALIZACIÓN CSS)
    st.subheader("3. SELECCIONA EL COLOR")
    
    # Definimos colores disponibles según tela
    colores_map = {}
    if "Gabardina" in tela or "Dril" in tela:
        colores_map = {"Azul Marino": "#1A237E", "Kaki": "#D7BDE2", "Verde Militar": "#33691E", "Negro": "#000000"}
    elif "Lana" in tela:
        colores_map = {"Gris Oxford": "#546E7A", "Negro Profundo": "#212121", "Azul Noche": "#0D47A1"}
    else:
        colores_map = {"Camel": "#E67E22", "Café": "#5D4037", "Azul": "#1565C0"}
        
    color_elegido = st.radio("Paleta:", list(colores_map.keys()), horizontal=True)
    hex_code = colores_map[color_elegido]
    
    # Renderizar el cuadrado de color (SIN FOTOS)
    st.markdown(f"""
    <div class="color-swatch" style="background-color: {hex_code};">
        {color_elegido}
    </div>
    """, unsafe_allow_html=True)
    
    # RESUMEN Y PRECIO
    precio_final = base_price + price_add
    
    st.markdown("---")
    c_res, c_btn = st.columns([2, 1])
    
    with c_res:
        st.markdown(f"### TOTAL: {precio_final} Bs.")
        st.caption("Incluye impuestos y forrería premium.")
        
    with c_btn:
        if st.button("AÑADIR A ORDEN DE CORTE"):
            st.session_state.carrito.append({
                "Modelo": modelo, "Tela": tela, "Color": color_elegido, "Precio": precio_final
            })
            st.balloons()
            st.success("¡Agregado!")

# --- PÁGINA: CARRITO ---
elif opcion == "CARRITO":
    st.markdown("## 🛒 FINALIZAR PEDIDO")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right'>PAGAR: {total} Bs.</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("WhatsApp")
            st.selectbox("Zona de Entrega", ["Sopocachi", "Zona Sur", "Centro", "El Alto"])
        with c2:
            st.write("Método de Pago:")
            st.selectbox("Seleccione:", ["Transferencia QR", "Efectivo"])
            
            if st.button("CONFIRMAR ORDEN"):
                with st.spinner("Procesando en Digital Locker..."):
                    time.sleep(2)
                st.success("¡PEDIDO ENVIADO!")
                st.info("El taller ha recibido la orden. Gracias por confiar en la Industria Nacional.")
                st.session_state.carrito = []
    else:
        st.warning("Tu carrito está vacío.")
