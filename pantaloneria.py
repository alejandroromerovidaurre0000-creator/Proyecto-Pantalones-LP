import streamlit as st
import pandas as pd
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN CORPORATIVA (MODO STARTUP)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL | Official Store",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES "LUJO ACCESIBLE"
C_BLACK = "#101010"
C_VIOLET = "#6C3483" # Identidad de marca
C_WHITE = "#FFFFFF"
C_GRAY = "#F2F4F4"

# ESTILOS CSS (DISEÑO APP NATIVA)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }}
    
    /* LOGO EMPRESARIAL */
    .brand-header {{
        padding: 20px 0;
        border-bottom: 2px solid {C_VIOLET};
        margin-bottom: 30px;
    }}
    .brand-name {{
        font-size: 2.8rem;
        font-weight: 900;
        color: {C_BLACK};
        letter-spacing: -1px;
        text-transform: uppercase;
        margin: 0;
    }}
    .brand-tagline {{
        font-size: 1rem;
        color: #666;
        font-weight: 300;
        letter-spacing: 2px;
    }}
    
    /* TARJETAS DE PRECIO ACTIVAS */
    .price-card {{
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    .price-card:hover {{
        border-color: {C_VIOLET};
        box-shadow: 0 8px 20px rgba(108, 52, 131, 0.15);
        transform: translateY(-2px);
    }}
    
    /* MUESTRAS DE COLOR (SWATCHES) */
    .color-box {{
        height: 80px;
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 2px solid #eee;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
    }}
    
    /* DATOS DEL LOCKER */
    .metric-box {{
        text-align: center;
        background-color: {C_GRAY};
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }}
    .metric-val {{ font-size: 1.5rem; font-weight: bold; color: {C_BLACK}; }}
    .metric-lbl {{ font-size: 0.7rem; text-transform: uppercase; color: #555; }}

    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 4px;
        height: 50px;
        font-weight: bold;
        border: none;
        width: 100%;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{ background-color: {C_VIOLET}; }}
    
    /* OCULTAR ELEMENTOS STREAMLIT */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS DE CLIENTES (MIGUEL, SAMAEL, JESSICA)
# ==============================================================================
# Datos biométricos completos para que el Locker se vea profesional.

DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'nivel': 'Founder',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42,
        'fit': 'Slim Fit'
    },
    '1002': { # Panelista
        'nombre': 'Samael Gómez Rúa', 'nivel': 'Miembro VIP',
        'cintura': 94, 'largo': 100, 'cadera': 105, 'muslo': 62, 'tiro': 28, 'rodilla': 46,
        'fit': 'Regular Comfort'
    },
    '1003': { # Tutora
        'nombre': 'Jessica Susana Daza', 'nivel': 'Miembro VIP',
        'cintura': 70, 'largo': 95, 'cadera': 92, 'muslo': 50, 'tiro': 24, 'rodilla': 38,
        'fit': 'Relaxed Fit'
    },
    '1004': { # Relator
        'nombre': 'Miguel Vidal Sejas', 'nivel': 'Miembro VIP',
        'cintura': 88, 'largo': 102, 'cadera': 100, 'muslo': 58, 'tiro': 27, 'rodilla': 44,
        'fit': 'Tailored Fit'
    }
}

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# ==============================================================================
# 3. BARRA DE NAVEGACIÓN
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/7543/7543152.png", width=50) # Icono sutil
    st.markdown("### PANTALONERÍA INTEGRAL")
    st.caption("La Paz • Bolivia")
    st.markdown("---")
    
    opcion = st.radio("MENÚ", ["INICIO", "DIGITAL LOCKER", "COLECCIÓN & COMPRA", "MI PEDIDO"], label_visibility="collapsed")
    
    st.markdown("---")
    # Créditos como "Directorio" para que parezca empresa real
    with st.expander("Equipo Directivo"):
        st.write("Alejandro Romero (CEO)")
        st.write("Jessica Daza (Directora)")
        st.write("Samael Gómez (Socio)")
        st.write("Miguel Vidal (Socio)")

# ==============================================================================
# 4. PÁGINAS DEL SITIO
# ==============================================================================

# --- PÁGINA: INICIO ---
if opcion == "INICIO":
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-name">PANTALONERÍA INTEGRAL</h1>
        <p class="brand-tagline">INGENIERÍA DE CONFORT | SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Precisión Biométrica", "99.9%", "Escáner 3D")
    c2.metric("Entrega", "24 Horas", "Sopocachi / Sur")
    c3.metric("Satisfacción", "100%", "Garantizada")
    
    st.divider()
    
    col_img, col_txt = st.columns([1, 1.5])
    with col_txt:
        st.markdown("### 💎 LA EVOLUCIÓN DEL PANTALÓN")
        st.write("""
        Olvídate de las tallas S, M o L. Nosotros confeccionamos tu pantalón basándonos en tu **Avatar Digital**.
        
        **Nuestra Promesa:**
        1.  **Ajuste Matemático:** Sin pruebas físicas incómodas.
        2.  **Solo Pantalones:** Especialización absoluta. Sin trajes ni distracciones.
        3.  **Calidad Superior:** Forrería interna de **Popelina 100% Algodón** en todas las prendas (Hipoalergénico y fresco).
        """)
        
        st.success("👉 **ACCESO CLIENTES:** Diríjase a 'DIGITAL LOCKER' para gestionar su perfil.")

# --- PÁGINA: DIGITAL LOCKER (DATOS COMPLETOS) ---
elif opcion == "DIGITAL LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER")
    st.caption("Gestión de Moldería y Datos Biométricos.")
    
    col_login, col_data = st.columns([1, 3])
    
    with col_login:
        st.markdown("#### Identificación")
        id_user = st.text_input("ID de Cliente", placeholder="Ej: 1004", label_visibility="collapsed")
        
        if st.button("ACCEDER"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Bienvenido de nuevo", icon="👋")
            else:
                st.error("ID no registrado en la base de datos.")
    
    with col_data:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Tarjeta de Perfil Profesional
            st.markdown(f"""
            <div class="price-card" style="border-left-color: #101010;">
                <h2 style="margin:0; color:#5B2C6F;">{u['nombre']}</h2>
                <span style="background:#eee; padding:2px 8px; border-radius:4px; font-size:0.8rem;">{u['nivel']}</span>
                <hr>
                <p><b>FIT ASIGNADO:</b> {u['fit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📐 ESPECIFICACIONES TÉCNICAS (CM)")
            
            # Grilla de medidas completa
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cintura']}</div><div class='metric-lbl'>Cintura</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cadera']}</div><div class='metric-lbl'>Cadera</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-box'><div class='metric-val'>{u['largo']}</div><div class='metric-lbl'>Largo</div></div>", unsafe_allow_html=True)
            m4.markdown(f"<div class='metric-box'><div class='metric-val'>{u['tiro']}</div><div class='metric-lbl'>Tiro</div></div>", unsafe_allow_html=True)
            m5.markdown(f"<div class='metric-box'><div class='metric-val'>{u['muslo']}</div><div class='metric-lbl'>Muslo</div></div>", unsafe_allow_html=True)
            m6.markdown(f"<div class='metric-box'><div class='metric-val'>{u['rodilla']}</div><div class='metric-lbl'>Rodilla</div></div>", unsafe_allow_html=True)
            
            st.info("✅ **ESTADO:** Patrones digitales verificados y listos para corte láser.")

        else:
            st.info("🔒 Sistema protegido. Ingrese su ID.")

# --- PÁGINA: COLECCIÓN & COMPRA (PRECIOS REALES) ---
elif opcion == "COLECCIÓN & COMPRA":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.success(f"Configurando medidas para: **{st.session_state.usuario['nombre']}**")
    
    # 1. SELECCIÓN DE LÍNEA
    st.subheader("1. SELECCIONA TU LÍNEA")
    linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
    
    precio = 0
    telas = []
    desc = ""
    
    if "ESTÁNDAR" in linea:
        # Variación de precios dentro de la línea estándar
        telas = ["Gabardina Spandex (220 Bs.)", "Dril Confort (240 Bs.)"]
        desc = "Tejidos resistentes de algodón con elastano para máxima movilidad."
    else:
        # Variación de precios dentro de la línea premium (Hasta 450)
        telas = ["Lana Fría Super 100's (420 Bs.)", "Casimir Importado (450 Bs.)"]
        desc = "Tejidos nobles importados. Termicidad regulada y caída impecable."
        
    st.caption(f"ℹ️ {desc}")
    
    col_conf1, col_conf2 = st.columns(2)
    
    with col_conf1:
        # 2. SELECCIÓN DE TELA
        st.markdown("#### 2. MATERIAL")
        tela_seleccionada = st.radio("Opciones Disponibles:", telas)
        
        # Extraer precio del string (ej: "450 Bs")
        precio = int(''.join(filter(str.isdigit, tela_seleccionada)))
        
    with col_conf2:
        # 3. SELECCIÓN DE COLOR (CSS)
        st.markdown("#### 3. COLOR")
        
        # Mapa de colores
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1B2631", "Kaki": "#D5D8DC", "Verde Olivo": "#1E8449"}
        else:
            colores = {"Gris Oxford": "#566573", "Negro Profundo": "#000000", "Azul Noche": "#154360"}
            
        color_nombre = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        color_hex = colores[color_nombre]
        
        # Muestra visual
        st.markdown(f"<div class='color-box' style='background-color:{color_hex};'></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # RESUMEN
    c_price, c_add = st.columns([1, 1])
    with c_price:
        st.markdown(f"### PRECIO: {precio} Bs.")
        st.caption("Incluye impuestos y personalización.")
    
    with c_add:
        st.write("")
        if st.button("AÑADIR A LA BOLSA"):
            st.session_state.carrito.append({
                "Línea": linea,
                "Tela": tela_seleccionada.split("(")[0], # Limpiar nombre
                "Color": color_nombre,
                "Precio": precio
            })
            st.balloons()
            st.success("¡Agregado correctamente!")

# --- PÁGINA: CHECKOUT (LOGÍSTICA COMPLETA) ---
elif opcion == "MI PEDIDO":
    st.markdown("## 🛒 FINALIZAR COMPRA")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:#5B2C6F;'>TOTAL A PAGAR: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Entrega")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.selectbox("Zona de Cobertura", ["Sopocachi", "Zona Sur (Calacoto/Obrajes)", "Centro", "Miraflores", "El Alto"])
            # CAMPOS SOLICITADOS
            st.text_area("Dirección Exacta:", placeholder="Calle, Número de Edificio, Piso...")
            st.text_input("Referencia Visual:", placeholder="Ej: Portón color café, al lado de la farmacia...")
            
        with c2:
            st.text_input("WhatsApp de Contacto:")
            st.selectbox("Método de Pago", ["Transferencia QR (Simple)", "Tarjeta de Débito/Crédito", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR PEDIDO"):
                with st.spinner("Procesando orden de corte..."):
                    time.sleep(2)
                st.success("¡PEDIDO CONFIRMADO!")
                st.info("Nos pondremos en contacto vía WhatsApp para coordinar la entrega.")
                st.session_state.carrito = [] # Limpiar
                
    else:
        st.warning("Tu bolsa de compras está vacía.")
