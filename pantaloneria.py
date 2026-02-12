import streamlit as st
import pandas as pd
import time
import random

# ==============================================================================
# 1. CONFIGURACIÓN E IDENTIDAD DE MARCA (MODO EMPRESA REAL)
# ==============================================================================
st.set_page_config(
    page_title="PANTALONERÍA INTEGRAL",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COLORES CORPORATIVOS
C_BLACK = "#0a0a0a"   # Negro Profundo
C_PURPLE = "#5B2C6F"  # Morado Identidad
C_GOLD = "#B7950B"    # Dorado Premium
C_GRAY = "#F8F9F9"    # Fondo Limpio

# CSS PARA GENERAR LA INTERFAZ SIN FOTOS (ESTILO TESLA/APPLE)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
    
    .stApp {{
        background-color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* LOGO TIPOGRÁFICO */
    .brand-logo {{
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: {C_BLACK};
        text-transform: uppercase;
        border-bottom: 5px solid {C_PURPLE};
        display: inline-block;
        margin-bottom: 10px;
    }}
    
    /* MUESTRAS DE COLOR (SWATCHES) */
    .color-swatch {{
        width: 100%;
        height: 100px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        border: 2px solid #eee;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
        cursor: pointer;
    }}
    .color-swatch:hover {{ transform: scale(1.03); border-color: {C_PURPLE}; }}
    
    /* TARJETAS DE PRECIO */
    .price-card {{
        background: {C_GRAY};
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid {C_PURPLE};
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    
    /* BOTONES */
    .stButton>button {{
        background-color: {C_BLACK};
        color: white;
        border-radius: 6px;
        padding: 15px;
        font-weight: 700;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{ background-color: {C_PURPLE}; }}

    /* OCULTAR MARCAS DE AGUA */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS (TRIBUNAL OCULTO)
# ==============================================================================
DB_CLIENTES = {
    '1001': {'nombre': 'Alejandro Romero', 'tipo': 'Fundador', 'cintura': 82, 'largo': 104, 'fit': 'Slim'},
    '1002': {'nombre': 'Samael Gómez Rúa', 'tipo': 'Cliente VIP', 'cintura': 94, 'largo': 100, 'fit': 'Regular Comfort'}, # Panelista
    '1003': {'nombre': 'Jessica Susana Daza', 'tipo': 'Cliente VIP', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed'}, # Tutora
    '1004': {'nombre': 'Miguel Vidal Sejas', 'tipo': 'Cliente VIP', 'cintura': 88, 'largo': 102, 'fit': 'Tailored Fit'} # Relator
}

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None

# ==============================================================================
# 3. BARRA LATERAL (DATOS ACADÉMICOS)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🧭 MENÚ PRINCIPAL")
    opcion = st.radio("", ["INICIO", "DIGITAL LOCKER", "CATÁLOGO & DISEÑO", "CARRITO DE COMPRAS"], label_visibility="collapsed")
    
    st.markdown("---")
    st.caption("© 2026 PANTALONERÍA INTEGRAL")
    st.caption("La Paz, Bolivia")
    
    with st.expander("Información Corporativa", expanded=True):
        st.markdown("**Fundador:** Alejandro Romero V.")
        st.markdown("**Directorio:**")
        st.caption("• Jessica Susana Daza Morales")
        st.caption("• Samael Gómez Rúa")
        st.caption("• Miguel Vidal Sejas")

# ==============================================================================
# 4. PÁGINAS DEL SISTEMA
# ==============================================================================

# --- PÁGINA: INICIO ---
if opcion == "INICIO":
    st.markdown('<div class="brand-logo">PANTALONERÍA INTEGRAL</div>', unsafe_allow_html=True)
    st.markdown("### INGENIERÍA DE CONFORT & SASTRERÍA DIGITAL")
    
    # KPIs (Corregido: Materiales Certificados en lugar de 100% Algodón)
    col1, col2, col3 = st.columns(3)
    col1.metric("Precisión de Ajuste", "99.8%", "Escaneo 3D")
    col2.metric("Entrega", "24 - 48 Hrs", "Producción Local")
    col3.metric("Materiales", "Certificados", "Nacionales e Importados")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💎 PROPUESTA DE VALOR")
        st.write("""
        Transformamos la experiencia de compra masculina. 
        
        **No vendemos trajes.** No vendemos tallas genéricas. 
        Vendemos el pantalón perfecto, configurado digitalmente y confeccionado a medida.
        """)
        # Nota Técnica Pág 115
        st.info("✅ **CALIDAD TÉCNICA (Tesis Pág. 115):** Independiente de la tela exterior, todos nuestros pantalones llevan forrería interna de **Popelina 100% Algodón** para garantizar frescura y durabilidad.")
    
    with c2:
        st.markdown("#### 🚀 PROCESO PHYGITAL")
        st.success("1. **DIGITAL LOCKER:** Digitalizamos tus medidas en nuestra tienda en Sopocachi.")
        st.info("2. **CATÁLOGO:** Eliges entre Línea Estándar o Premium desde tu celular.")
        st.warning("3. **ENTREGA:** Recibes el producto sin necesidad de pruebas físicas.")

# --- PÁGINA: DIGITAL LOCKER ---
elif opcion == "DIGITAL LOCKER":
    st.markdown("## 🔐 ACCESO BIOMÉTRICO")
    st.write("Ingrese ID de Cliente para cargar moldería digital.")
    
    col_input, col_display = st.columns([1, 2])
    
    with col_input:
        st.text("ID Cliente:")
        id_user = st.text_input("ID", placeholder="Ej: 1004", label_visibility="collapsed")
        
        if st.button("AUTENTICAR PERFIL"):
            if id_user in DB_CLIENTES:
                st.session_state.usuario = DB_CLIENTES[id_user]
                st.toast(f"Bienvenido {st.session_state.usuario['nombre']}", icon="🔓")
            else:
                st.error("ID No Registrado")
                
    with col_display:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            st.markdown(f"""
            <div class="price-card">
                <h2 style="color:#5B2C6F; margin:0;">{u['nombre']}</h2>
                <p><b>Estado:</b> {u['tipo']} | <b>Medidas:</b> Verificadas</p>
                <hr>
                <div style="display:flex; justify-content:space-between; text-align:center;">
                    <div><h1>{u['cintura']}</h1><small>CM CINTURA</small></div>
                    <div><h1>{u['largo']}</h1><small>CM LARGO</small></div>
                    <div><h1>{u['fit']}</h1><small>FIT PREFERIDO</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Patrones DXF listos para corte automático.")
        else:
            st.info("🔒 Ingrese credenciales para visualizar datos.")

# --- PÁGINA: CATÁLOGO & DISEÑO (CORREGIDO: PRECIOS Y LÍNEAS) ---
elif opcion == "CATÁLOGO & DISEÑO":
    st.markdown("## 🛠️ STUDIO DE DISEÑO")
    st.write("Configuración de producto por Líneas.")
    
    if st.session_state.usuario:
        st.caption(f"Configurando para: **{st.session_state.usuario['nombre']}**")
    
    # 1. SELECCIÓN DE LÍNEA (CORREGIDO: SOLO ESTÁNDAR Y PREMIUM)
    st.subheader("1. SELECCIONA LA LÍNEA")
    
    linea = st.selectbox("Categoría:", 
                         ["LÍNEA ESTÁNDAR (Uso Diario / Oficina)", 
                          "LÍNEA PREMIUM (Ejecutivo / Sartorial)"])
    
    # Lógica de Precios y Modelos
    precio_base = 0
    telas_disponibles = []
    
    if "ESTÁNDAR" in linea:
        precio_base = 200 # CORREGIDO: Empieza en 200
        desc_linea = "Resistencia y confort para el día a día."
        telas_disponibles = ["Gabardina Spandex (97% Alg / 3% Elast)", "Dril Confort (Casual)"]
    else:
        precio_base = 450 # CORREGIDO: Premium
        desc_linea = "Elegancia superior con telas importadas y acabados a mano."
        telas_disponibles = ["Lana Fría Super 100's", "Casimir Importado"]
        
    st.info(f"ℹ️ **{linea}:** {desc_linea}")
    
    col_config = st.columns(2)
    
    # 2. SELECCIÓN DE TELA
    with col_config[0]:
        st.subheader("2. MATERIAL (TELA)")
        tela_elegida = st.radio("Opciones Disponibles:", telas_disponibles)
        
        # Ajuste de precio por tela específica (opcional)
        precio_final = precio_base
        if "Casimir" in tela_elegida: precio_final += 30 # Casimir un poco más caro que Lana base
        
    # 3. SELECCIÓN DE COLOR (SWATCHES CSS)
    with col_config[1]:
        st.subheader("3. COLOR")
        
        # Mapa de colores según la línea
        colores_map = {}
        if "ESTÁNDAR" in linea:
            colores_map = {
                "Azul Marino": "#154360", 
                "Kaki Oficina": "#D6DBDF", 
                "Verde Oliva": "#1E8449", 
                "Negro": "#17202A"
            }
        else: # PREMIUM
            colores_map = {
                "Gris Oxford": "#566573", 
                "Negro Profundo": "#000000", 
                "Azul Noche": "#1B2631", 
                "Arena": "#F5CBA7"
            }
            
        color_nombre = st.radio("Paleta:", list(colores_map.keys()), horizontal=True)
        color_hex = colores_map[color_nombre]
        
        # Renderizar Cuadro de Color
        st.markdown(f"""
        <div class="color-swatch" style="background-color: {color_hex};">
            {color_nombre}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # RESUMEN Y BOTÓN
    c_res, c_btn = st.columns([1, 1])
    
    with c_res:
        st.markdown(f"### PRECIO FINAL: {precio_final} Bs.")
        st.caption("Incluye impuestos de ley.")
        
    with c_btn:
        st.write("")
        if st.button("AÑADIR A ORDEN DE CORTE"):
            item = {
                "Línea": linea,
                "Tela": tela_elegida,
                "Color": color_nombre,
                "Precio": precio_final
            }
            st.session_state.carrito.append(item)
            st.balloons()
            st.success("¡Producto Agregado!")

# --- PÁGINA: CARRITO ---
elif opcion == "CARRITO DE COMPRAS":
    st.markdown("## 🛒 FINALIZAR PEDIDO")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        
        # Mostrar tabla limpia
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h1 style='text-align:right; color:#5B2C6F'>TOTAL: {total} Bs.</h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("WhatsApp de Contacto")
            st.selectbox("Zona de Entrega", ["Sopocachi (Gratis)", "Zona Sur", "Centro", "El Alto"])
        with c2:
            st.selectbox("Método de Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            st.write("")
            if st.button("CONFIRMAR ORDEN"):
                with st.spinner("Conectando con Digital Locker..."):
                    time.sleep(1.5)
                st.success("¡PEDIDO ENVIADO AL TALLER!")
                st.info("Gracias por confiar en Pantalonería Integral.")
                st.session_state.carrito = []
    else:
        st.warning("Tu carrito está vacío. Ve al Catálogo para configurar tu pantalón.")
   
