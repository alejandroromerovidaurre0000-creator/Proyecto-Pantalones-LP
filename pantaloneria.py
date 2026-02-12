import streamlit as st
import pandas as pd
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL | Tesis 2026",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PALETA DE COLORES (Sobria y Tecnológica)
C_BLACK = "#101010"
C_VIOLET = "#6C3483" # Color de acento (Innovación)
C_GRAY_BG = "#F8F9F9"

# ESTILOS CSS (DISEÑO LIMPIO)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }}
    
    /* HEADER TIPO MARCA (Logo CSS Seguro) */
    .brand-header {{
        padding: 30px 0;
        text-align: center;
        background: linear-gradient(to right, {C_BLACK}, #2c3e50);
        color: white;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .brand-name {{
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
    }}
    .brand-tagline {{
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 1px;
        opacity: 0.9;
    }}
    
    /* TARJETAS DE PRECIO/PERFIL */
    .info-card {{
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 25px;
        border-left: 5px solid {C_VIOLET};
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    .info-card:hover {{
        box-shadow: 0 8px 20px rgba(108, 52, 131, 0.15);
        transform: translateY(-3px);
    }}
    
    /* MUESTRAS DE COLOR (SWATCHES CSS) */
    .color-box {{
        height: 80px;
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 3px solid #eee;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.1);
        cursor: pointer;
    }}
    
    /* CAJAS DE MÉTRICAS (LOCKER) */
    .metric-box {{
        text-align: center;
        background-color: {C_GRAY_BG};
        padding: 15px 5px;
        border-radius: 8px;
        border: 1px solid #eee;
    }}
    .metric-val {{ font-size: 1.6rem; font-weight: 700; color: {C_BLACK}; }}
    .metric-lbl {{ font-size: 0.7rem; text-transform: uppercase; color: #666; margin-top: 5px; }}

    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 6px;
        height: 55px;
        font-weight: 700;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1rem;
    }}
    .stButton>button:hover {{ background-color: {C_VIOLET}; }}
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {{ background-color: {C_GRAY_BG}; }}

    /* OCULTAR ELEMENTOS STREAMLIT */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (TRIBUNAL ACADÉMICO)
# ==============================================================================
# Datos completos para el Digital Locker.

DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero', 'cargo': 'Postulante',
        'cintura': 82, 'largo': 104, 'cadera': 96, 'muslo': 54, 'tiro': 26, 'rodilla': 42,
        'fit': 'Slim Fit'
    },
    '1002': { # Panelista
        'nombre': 'Samael Gómez Rúa', 'cargo': 'Panelista',
        'cintura': 94, 'largo': 100, 'cadera': 105, 'muslo': 62, 'tiro': 28, 'rodilla': 46,
        'fit': 'Regular Comfort'
    },
    '1003': { # Tutora
        'nombre': 'Jessica Susana Daza', 'cargo': 'Tutora',
        'cintura': 70, 'largo': 95, 'cadera': 92, 'muslo': 50, 'tiro': 24, 'rodilla': 38,
        'fit': 'Relaxed Fit'
    },
    '1004': { # Relator
        'nombre': 'Miguel Vidal Sejas', 'cargo': 'Relator',
        'cintura': 88, 'largo': 102, 'cadera': 100, 'muslo': 58, 'tiro': 27, 'rodilla': 44,
        'fit': 'Tailored Fit'
    }
}

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# ==============================================================================
# 3. BARRA DE NAVEGACIÓN & CRÉDITOS
# ==============================================================================
with st.sidebar:
    # Icono de marca
    st.markdown("<div style='text-align:center; font-size: 40px;'>🧵</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcion = st.radio("MENÚ PRINCIPAL", ["INICIO", "DIGITAL LOCKER", "COLECCIÓN & COMPRA", "MI PEDIDO"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # CRÉDITOS ACADÉMICOS (CORREGIDOS)
    st.markdown("### CRÉDITOS ACADÉMICOS")
    st.caption("Proyecto de Grado UCB 2026")
    
    with st.expander("Ver Tribunal Evaluador", expanded=True):
        st.markdown("**Tutora:**\nJessica Susana Daza Morales")
        st.markdown("**Panelista:**\nSamael Gómez Rúa")
        st.markdown("**Relator:**\nMiguel Vidal Sejas")
        
    st.markdown("---")
    st.caption("**Postulante:**\nAlejandro M. Romero V.")

# ==============================================================================
# 4. PÁGINAS DEL SITIO
# ==============================================================================

# --- PÁGINA: INICIO ---
if opcion == "INICIO":
    # Header de Marca (Logo CSS)
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-name">PANTALONERÍA INTEGRAL</h1>
        <p class="brand-tagline">INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs (CORREGIDO: 24-48 Hrs)
    c1, c2, c3 = st.columns(3)
    c1.metric("Precisión Biométrica", "99.9%", "Escáner 3D")
    c2.metric("Tiempo de Entrega", "24 - 48 Hrs", "Producción Local")
    c3.metric("Materiales", "Certificados", "Alta Calidad")
    
    st.divider()
    
    col_txt, col_cta = st.columns([2, 1])
    with col_txt:
        st.markdown("### 💎 LA PROPUESTA DE VALOR")
        st.write("""
        Transformamos la experiencia de compra masculina mediante un modelo **Phygital** (Físico + Digital).
        
        **No vendemos trajes.** Nos especializamos 100% en el pantalón a medida, eliminando las tallas genéricas y los materiales de baja calidad.
        """)
        
        # Nota Técnica Pág 115 (Importante para defensa)
        st.info("✅ **GARANTÍA TÉCNICA (Tesis Pág. 115):** Todos nuestros pantalones, sin excepción, incluyen forrería interna de **Popelina 100% Algodón** para garantizar frescura, hipoalergencia y durabilidad.")
    
    with col_cta:
        st.markdown("#### 🚀 TRES PASOS")
        st.success("1. **DIGITAL LOCKER:** Digitalizamos tus medidas en una sola visita.")
        st.info("2. **CONFIGURADOR:** Eliges tela y color desde esta plataforma.")
        st.warning("3. **ENTREGA:** Recibes tu prenda perfecta en 24-48 horas.")

# --- PÁGINA: DIGITAL LOCKER (DATOS COMPLETOS) ---
elif opcion == "DIGITAL LOCKER":
    st.markdown("## 🔐 DIGITAL LOCKER | PERFIL BIOMÉTRICO")
    st.write("Gestión segura de moldería digital.")
    
    col_login, col_data = st.columns([1, 3])
    
    with col_login:
        st.markdown("#### Acceso Seguro")
        id_user = st.text_input("ID de Cliente", placeholder="Ej: 1004", label_visibility="collapsed")
        
        if st.button("AUTENTICAR"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Identidad Verificada", icon="🔓")
            else:
                st.error("ID No Reconocido en Base de Datos.")
    
    with col_data:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Tarjeta de Perfil
            st.markdown(f"""
            <div class="info-card">
                <h2 style="margin:0; color:{C_VIOLET};">{u['nombre']}</h2>
                <p style="color:#666; text-transform:uppercase; letter-spacing:1px;">{u['cargo']} | Perfil Verificado</p>
                <hr>
                <p><b>FIT ASIGNADO:</b> {u['fit']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📐 ESPECIFICACIONES DE MOLDERÍA (CM)")
            
            # Grilla de 6 medidas
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cintura']}</div><div class='metric-lbl'>Cintura</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='metric-box'><div class='metric-val'>{u['cadera']}</div><div class='metric-lbl'>Cadera</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='metric-box'><div class='metric-val'>{u['largo']}</div><div class='metric-lbl'>Largo</div></div>", unsafe_allow_html=True)
            m4.markdown(f"<div class='metric-box'><div class='metric-val'>{u['tiro']}</div><div class='metric-lbl'>Tiro</div></div>", unsafe_allow_html=True)
            m5.markdown(f"<div class='metric-box'><div class='metric-val'>{u['muslo']}</div><div class='metric-lbl'>Muslo</div></div>", unsafe_allow_html=True)
            m6.markdown(f"<div class='metric-box'><div class='metric-val'>{u['rodilla']}</div><div class='metric-lbl'>Rodilla</div></div>", unsafe_allow_html=True)
            
            st.success("✅ **ESTADO:** Patrones digitales generados. Listo para producción.")

        else:
            st.info("🔒 Ingrese un ID válido (Ej: 1004) para visualizar los datos.")

# --- PÁGINA: COLECCIÓN & COMPRA (PRECIOS REALES) ---
elif opcion == "COLECCIÓN & COMPRA":
    st.markdown("## 🛠️ CONFIGURADOR DE PRODUCTO")
    
    if st.session_state.usuario:
        st.success(f"Diseñando con medidas de: **{st.session_state.usuario['nombre']}**")
    else:
        st.warning("⚠️ Modo Invitado. Se usarán tallas estándar.")
    
    # 1. SELECCIÓN DE LÍNEA
    st.subheader("1. SELECCIONA TU LÍNEA")
    linea = st.selectbox("Categoría:", ["LÍNEA ESTÁNDAR (Uso Diario)", "LÍNEA PREMIUM (Ejecutivo)"])
    
    precio = 0
    telas = []
    desc = ""
    
    if "ESTÁNDAR" in linea:
        # Variación de precios Estándar
        telas = ["Gabardina Spandex (220 Bs.)", "Dril Confort (240 Bs.)"]
        desc = "Tejidos de algodón con elastano para resistencia y movilidad diaria."
    else:
        # Variación de precios Premium (Tope 450)
        telas = ["Lana Fría Super 100's (420 Bs.)", "Casimir Importado (450 Bs.)"]
        desc = "Tejidos nobles importados. Termicidad regulada y caída sastre impecable."
        
    st.caption(f"ℹ️ {desc}")
    
    col_conf1, col_conf2 = st.columns(2)
    
    with col_conf1:
        # 2. SELECCIÓN DE TELA
        st.markdown("#### 2. MATERIAL")
        tela_seleccionada = st.radio("Opciones Disponibles:", telas)
        
        # Extraer precio del string
        precio = int(''.join(filter(str.isdigit, tela_seleccionada)))
        
    with col_conf2:
        # 3. SELECCIÓN DE COLOR (CSS PURO - SIN FOTOS)
        st.markdown("#### 3. COLOR")
        
        # Mapa de colores según línea
        colores = {}
        if "ESTÁNDAR" in linea:
            colores = {"Azul Navy": "#1B2631", "Kaki / Beige": "#D5D8DC", "Verde Olivo": "#4D5645"}
        else:
            colores = {"Gris Oxford": "#424949", "Negro Profundo": "#000000", "Azul Noche": "#154360"}
            
        color_nombre = st.radio("Paleta:", list(colores.keys()), horizontal=True)
        color_hex = colores[color_nombre]
        
        # Muestra visual de color (No falla)
        st.markdown(f"<div class='color-box' style='background-color:{color_hex};'></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # RESUMEN
    c_price, c_add = st.columns([1, 1])
    with c_price:
        st.markdown(f"### PRECIO FINAL: {precio} Bs.")
        st.caption("Incluye impuestos de ley y confección a medida.")
    
    with c_add:
        st.write("")
        if st.button("AÑADIR A LA BOLSA DE COMPRAS"):
            st.session_state.carrito.append({
                "Línea": linea,
                "Tela": tela_seleccionada.split("(")[0], # Limpiar nombre
                "Color": color_nombre,
                "Precio": precio
            })
            st.balloons()
            st.toast("¡Producto Agregado!", icon="🛍️")

# --- PÁGINA: CHECKOUT (LOGÍSTICA COMPLETA) ---
elif opcion == "MI PEDIDO":
    st.markdown("## 🛒 FINALIZAR COMPRA")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right; color:{C_VIOLET};'>TOTAL A PAGAR: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Entrega & Pago")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.selectbox("Zona de Cobertura", ["Sopocachi", "Zona Sur (Calacoto/Obrajes)", "Centro", "Miraflores", "El Alto"])
            # CAMPOS SOLICITADOS
            st.text_area("Dirección Exacta:", placeholder="Calle, Número de Edificio, Piso...")
            st.text_input("Referencia Visual:", placeholder="Ej: Portón color café, frente a la plaza...")
            
        with c2:
            st.text_input("WhatsApp de Contacto:", placeholder="70000000")
            st.selectbox("Método de Pago", ["Transferencia QR (Simple)", "Tarjeta de Débito/Crédito", "Efectivo Contra-entrega"])
            
            st.write("")
            st.info("Al confirmar, se generará la orden de corte con las medidas de su Digital Locker.")
            if st.button("CONFIRMAR PEDIDO"):
                if st.session_state.usuario:
                    with st.spinner("Procesando orden de corte..."):
                        time.sleep(2)
                    st.success("¡PEDIDO CONFIRMADO!")
                    st.markdown(f"""
                    > **Orden Generada para: {st.session_state.usuario['nombre']}**
                    > Nos contactaremos vía WhatsApp para coordinar la entrega en 24-48 horas.
                    """)
                    st.session_state.carrito = [] # Limpiar
                else:
                    st.error("⚠️ Por favor, inicie sesión en el 'Digital Locker' antes de confirmar el pedido para asegurar las medidas.")
                
    else:
        st.warning("Tu bolsa de compras está vacía.")
        st.caption("Ve a 'Colección & Compra' para configurar tu primer pantalón.")
