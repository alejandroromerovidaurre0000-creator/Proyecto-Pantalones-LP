import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA Y BRANDING
# ==============================================================================

st.set_page_config(
    page_title="Pantalonería Integral | Sistema Phygital",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores de la Marca (Negro, Blanco, Morado Tecnológico)
COLOR_BRAND_PRIMARY = "#111111"
COLOR_BRAND_ACCENT = "#5B2C6F" # Morado Oscuro
COLOR_BRAND_LIGHT = "#F4F6F7"
COLOR_TEXT_MAIN = "#212F3C"

# CSS AVANZADO (ESTILO APP NATIVA)
st.markdown(f"""
    <style>
    /* Importar fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
        background-color: {COLOR_BRAND_LIGHT};
    }}
    
    /* HEADER PERSONALIZADO */
    .main-header {{
        background: linear-gradient(135deg, {COLOR_BRAND_PRIMARY} 0%, {COLOR_BRAND_ACCENT} 100%);
        padding: 30px;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}
    .main-header h1 {{ font-weight: 700; letter-spacing: 2px; text-transform: uppercase; font-size: 2.5rem; color: white; margin: 0; }}
    .main-header p {{ font-weight: 300; font-size: 1.1rem; opacity: 0.9; margin-top: 10px; }}

    /* TARJETAS DE PRODUCTO (CONFIGURADOR) */
    .product-card {{
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #EAECEE;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .product-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(91, 44, 111, 0.15);
        border-color: {COLOR_BRAND_ACCENT};
    }}

    /* DIGITAL LOCKER CARDS */
    .locker-metric {{
        background-color: white;
        border-left: 4px solid {COLOR_BRAND_ACCENT};
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }}
    .locker-metric h2 {{ color: {COLOR_BRAND_ACCENT}; margin: 0; font-size: 2rem; }}
    .locker-metric span {{ color: #7F8C8D; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }}

    /* BOTONES */
    .stButton > button {{
        width: 100%;
        background-color: {COLOR_BRAND_PRIMARY};
        color: white;
        border-radius: 50px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
        transition: all 0.3s;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_BRAND_ACCENT};
        box-shadow: 0 5px 15px rgba(91, 44, 111, 0.4);
        color: white;
    }}

    /* ALERTA DE TESIS */
    .thesis-alert {{
        background-color: #E8F6F3;
        color: #145A32;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #A9DFBF;
        font-size: 0.9rem;
        margin-top: 10px;
    }}
    
    /* Ocultar elementos nativos de Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. BASE DE DATOS DE IMÁGENES (MOTOR DE CAMBIO DE COLOR)
# ==============================================================================
# Diccionario que mapea MODELO + COLOR a una URL específica de PANTALONES (Sin trajes)

DB_IMAGENES = {
    "Chino": {
        "Azul Marino": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80",
        "Kaki / Beige": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80", # Beige Pants
        "Negro": "https://images.unsplash.com/photo-1517445312882-1dd682bc8d96?auto=format&fit=crop&w=800&q=80",
        "Verde Oliva": "https://images.pexels.com/photos/934069/pexels-photo-934069.jpeg?auto=compress&cs=tinysrgb&w=800",
        "Gris": "https://images.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "5-Pockets": {
        "Azul Denim": "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=800&q=80",
        "Negro": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=800",
        "Café / Tierra": "https://images.pexels.com/photos/4210866/pexels-photo-4210866.jpeg?auto=compress&cs=tinysrgb&w=800",
        "Gris": "https://images.pexels.com/photos/2343661/pexels-photo-2343661.jpeg?auto=compress&cs=tinysrgb&w=800"
    },
    "Sartorial": {
        "Gris Oxford": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80", # Tela de vestir
        "Negro Profundo": "https://images.pexels.com/photos/1342609/pexels-photo-1342609.jpeg?auto=compress&cs=tinysrgb&w=800",
        "Azul Noche": "https://images.pexels.com/photos/3755706/pexels-photo-3755706.jpeg?auto=compress&cs=tinysrgb&w=800",
        "Arena": "https://images.pexels.com/photos/5325886/pexels-photo-5325886.jpeg?auto=compress&cs=tinysrgb&w=800"
    }
}

def obtener_imagen(modelo_key, color_key):
    """Función segura para obtener imagen sin romper el código"""
    try:
        return DB_IMAGENES[modelo_key][color_key]
    except:
        # Imagen por defecto si falla algo
        return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80"

# ==============================================================================
# 3. GESTIÓN DE ESTADO (SESSION STATE)
# ==============================================================================

if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {
            'nombre': 'Alejandro Romero', 'rol': 'Postulante', 
            'cintura': 82, 'largo': 104, 'tiro': 'Regular', 'fit': 'Slim',
            'morfologia': [4, 3, 4, 5, 4] # Datos para gráfico radar
        },
        '1002': {
            'nombre': 'Lic. Samael Gómez Rúa', 'rol': 'Panelista', 
            'cintura': 94, 'largo': 100, 'tiro': 'Corto', 'fit': 'Regular Comfort',
            'morfologia': [5, 4, 3, 3, 5]
        },
        '1003': {
            'nombre': 'Lic. Jessica Daza Morales', 'rol': 'Tutora', 
            'cintura': 70, 'largo': 95, 'tiro': 'Alto', 'fit': 'Relaxed',
            'morfologia': [3, 5, 2, 4, 3]
        },
        '1004': {
            'nombre': 'Lic. Miguel Vidal Sejas', 'rol': 'Relator', 
            'cintura': 88, 'largo': 102, 'tiro': 'Regular', 'fit': 'Tailored',
            'morfologia': [4, 4, 4, 4, 4]
        }
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# ==============================================================================
# 4. BARRA LATERAL DE NAVEGACIÓN
# ==============================================================================

with st.sidebar:
    # Logo simulado
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div style='background-color: white; width: 60px; height: 60px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 30px;'>🧵</div>
            <h3 style='color: white; margin-top: 10px;'>PANTALONERÍA<br>INTEGRAL</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🧭 NAVEGACIÓN")
    menu = st.radio("", 
        ["1. CONCEPT & PHYGITAL", "2. DIGITAL LOCKER", "3. PERSONALIZADOR", "4. INGENIERÍA (TESIS)", "5. CHECKOUT"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎓 DATOS ACADÉMICOS")
    with st.expander("Ver Tribunal Evaluador", expanded=True):
        st.caption("PROYECTO DE GRADO 2026")
        st.markdown("**Tutora:**\nJessica Susana Daza Morales")
        st.markdown("**Panelista:**\nSamael Gómez Rúa")
        st.markdown("**Relator:**\nMiguel Vidal Sejas")
        st.markdown("---")
        st.caption("Postulante:\n**Alejandro M. Romero V.**")

# ==============================================================================
# 5. MÓDULOS DEL SISTEMA
# ==============================================================================

# --- MÓDULO 1: HOME ---
if "1. CONCEPT" in menu:
    st.markdown(f"""
    <div class="main-header">
        <h1>PANTALONERÍA INTEGRAL MASCULINA</h1>
        <p>REDEFINIENDO LA SASTRERÍA CON TECNOLOGÍA BIOMÉTRICA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    col_hero1, col_hero2 = st.columns([1.5, 1])
    
    with col_hero1:
        st.image("https://images.unsplash.com/photo-1620799140408-ed5341cd2431?q=80&w=1200&auto=format&fit=crop", 
                 caption="Taller Phygital: Donde la tela encuentra al dato.", use_column_width=True)
    
    with col_hero2:
        st.markdown("### 🛑 EL PROBLEMA ACTUAL")
        st.markdown("""
        1.  **Tallas Irreales:** "Soy 32 en una marca y 34 en otra".
        2.  **Materiales Pobres:** El mercado abusa del poliéster que genera calor y mal olor.
        3.  **El Traje Innecesario:** El hombre moderno busca **pantalones**, no trajes completos.
        """)
        
        st.markdown("### ✅ NUESTRA SOLUCIÓN")
        st.info("**A. ESCANEO ÚNICO:** Visitas la tienda una vez. Te digitalizamos.")
        st.info("**B. DIGITAL LOCKER:** Tus medidas se guardan en la nube.")
        st.info("**C. CONFECCIÓN A DEMANDA:** Eliges tela y diseño. Nosotros cortamos con tus medidas.")

# --- MÓDULO 2: DIGITAL LOCKER (AVANZADO) ---
elif "2. DIGITAL LOCKER" in menu:
    st.markdown("""
    <div class="main-header">
        <h1>🔐 DIGITAL LOCKER</h1>
        <p>PERFIL BIOMÉTRICO Y GESTIÓN DE DATOS DEL CLIENTE</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 3])
    
    with c1:
        st.markdown("### 👤 IDENTIFICACIÓN")
        id_input = st.text_input("ID Cliente:", placeholder="Ej: 1004")
        
        if st.button("🔍 CONSULTAR ID"):
            user_data = st.session_state.db_clientes.get(id_input)
            if user_data:
                st.session_state.usuario = user_data
                st.success("¡Identidad Verificada!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("ID No encontrado. Pruebe 1002, 1003 o 1004.")
                
    with c2:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Encabezado del perfil
            st.markdown(f"## Expediente: {u['nombre']}")
            st.caption(f"Rol: {u['rol']} | Estado: ACTIVO | Última Actualización: {datetime.now().strftime('%d/%m/%Y')}")
            
            # Métricas Clave
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"<div class='locker-metric'><h2>{u['cintura']}</h2><span>CINTURA (CM)</span></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div class='locker-metric'><h2>{u['largo']}</h2><span>LARGO (CM)</span></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='locker-metric'><h2>{u['tiro']}</h2><span>TIPO TIRO</span></div>", unsafe_allow_html=True)
            with m4:
                st.markdown(f"<div class='locker-metric'><h2>{u['fit']}</h2><span>FIT PREFERIDO</span></div>", unsafe_allow_html=True)
            
            st.write("")
            
            # VISUALIZACIÓN DE DATOS (GRÁFICO RADAR)
            col_graph, col_detail = st.columns([1, 1])
            
            with col_graph:
                st.markdown("### 📊 Morfología vs. Patrón Base")
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                      r=u['morfologia'],
                      theta=categories,
                      fill='toself',
                      name='Cliente',
                      line_color='#5B2C6F'
                ))
                fig.add_trace(go.Scatterpolar(
                      r=[3, 3, 3, 3, 3],
                      theta=categories,
                      name='Talla M (Ref)',
                      line_color='#BDC3C7',
                      line_dash='dot'
                ))
                fig.update_layout(
                  polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                  showlegend=True,
                  height=300,
                  margin=dict(l=40, r=40, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with col_detail:
                st.markdown("### 📋 Análisis Técnico")
                st.markdown("""
                - **Discrepancia detectada:** La relación Cintura/Cadera requiere ajuste de pinzas traseras.
                - **Sugerencia de Sastre:** Recomendamos tiro medio para mayor comodidad al sentarse.
                - **Digitalización:** Patrones DXF generados y listos para máquina de corte.
                """)
                st.success("✅ ESTE PERFIL ESTÁ LISTO PARA COMPRAR.")

        else:
            st.info("👋 Esperando autenticación. Por favor ingrese un ID en el panel izquierdo.")
            st.image("https://cdn.dribbble.com/users/2063388/screenshots/15647700/media/1a90c675371c89073145d475ce9953db.png?compress=1&resize=800x400", caption="Sistema Biométrico Seguro")

# --- MÓDULO 3: PERSONALIZADOR (CONFIGURADOR DE PRODUCTO) ---
elif "3. PERSONALIZADOR" in menu:
    st.markdown("""
    <div class="main-header">
        <h1>🛠️ ATELIER DE DISEÑO</h1>
        <p>CONFIGURA TU PANTALÓN ÚNICO. PRECIO DINÁMICO.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.usuario:
        st.success(f"🪡 Diseñando con medidas de: **{st.session_state.usuario['nombre']}**")
    else:
        st.warning("⚠️ Modo Invitado (Medidas Estándar). Se recomienda iniciar sesión en Digital Locker.")

    # --- PASO 1: MODELO ---
    st.subheader("1. SELECCIONA EL MODELO BASE")
    
    col_models = st.columns(3)
    modelo_elegido = None
    key_modelo = ""
    base_price = 0
    
    with col_models[0]:
        st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80", caption="CHINO CLASSIC")
        if st.checkbox("Seleccionar CHINO", key="chk_chino"):
            modelo_elegido = "Chino Gabardina"
            key_modelo = "Chino"
            base_price = 180

    with col_models[1]:
        st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=600&q=80", caption="5-POCKETS (Casual)")
        if st.checkbox("Seleccionar 5-POCKETS", key="chk_5p"):
            modelo_elegido = "5-Pockets Casual"
            key_modelo = "5-Pockets"
            base_price = 160
            
    with col_models[2]:
        st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80", caption="SARTORIAL (Vestir)")
        if st.checkbox("Seleccionar SARTORIAL", key="chk_sart"):
            modelo_elegido = "Sartorial Dress"
            key_modelo = "Sartorial"
            base_price = 250

    st.markdown("---")

    if modelo_elegido:
        # --- PASO 2 Y 3: TELA Y COLOR ---
        col_config_izq, col_config_der = st.columns([1, 1])
        
        with col_config_izq:
            st.markdown(f"### Configurando: {modelo_elegido}")
            
            # Selector de Tela
            st.markdown("#### 2. La Tela (Material)")
            tela_opciones = ["Gabardina Spandex (Estándar)", "Dril 100% Algodón", "Lana Fría Super 100's (Premium)", "Pana / Corduroy"]
            tela = st.selectbox("Seleccione Material:", tela_opciones)
            
            # Lógica de precios
            extra_price = 0
            if "Lana" in tela: extra_price = 200
            elif "Pana" in tela: extra_price = 60
            elif "Dril" in tela: extra_price = 40
            elif "Gabardina" in tela: extra_price = 20
            
            # Selector de Color (Dinámico)
            st.markdown("#### 3. El Color")
            colores_disponibles = []
            if key_modelo == "Chino": colores_disponibles = ["Azul Marino", "Kaki / Beige", "Negro", "Verde Oliva"]
            elif key_modelo == "5-Pockets": colores_disponibles = ["Azul Denim", "Negro", "Gris", "Café / Tierra"]
            elif key_modelo == "Sartorial": colores_disponibles = ["Gris Oxford", "Negro Profundo", "Azul Noche", "Arena"]
            
            color = st.radio("Tonos:", colores_disponibles, horizontal=True)
            
            # Detalles Finales
            precio_final = base_price + extra_price
            
            st.markdown(f"""
            <div class="thesis-alert">
                <b>Nota Tesis (Pág 115):</b> Independiente de la tela elegida, este pantalón incluirá 
                forrería interna de <b>Popelina 100% Algodón</b> para máxima frescura.
            </div>
            """, unsafe_allow_html=True)

        with col_config_der:
            st.markdown("#### Vista Previa")
            
            # OBTENER IMAGEN DINÁMICA
            img_url = obtener_imagen(key_modelo, color)
            
            st.markdown(f"""
            <div class="product-card">
                <img src="{img_url}" style="width:100%; border-radius:10px; height: 300px; object-fit: cover;">
                <h2 style="text-align:right; color:{COLOR_BRAND_ACCENT}; margin-top:10px;">{precio_final} Bs.</h2>
                <hr>
                <p><b>Modelo:</b> {modelo_elegido}</p>
                <p><b>Tela:</b> {tela}</p>
                <p><b>Color:</b> {color}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("AÑADIR AL CARRITO 🛒"):
                item = {
                    "Modelo": modelo_elegido,
                    "Tela": tela,
                    "Color": color,
                    "Precio": precio_final,
                    "ID": random.randint(1000,9999)
                }
                st.session_state.carrito.append(item)
                st.balloons()
                st.success("¡Producto añadido exitosamente!")

    else:
        st.info("👆 Selecciona un modelo arriba para comenzar a configurar.")

# --- MÓDULO 4: INGENIERÍA DEL PRODUCTO (TESIS) ---
elif "4. INGENIERÍA" in menu:
    st.markdown("""
    <div class="main-header">
        <h1>📘 INGENIERÍA DEL PRODUCTO</h1>
        <p>FUNDAMENTOS TÉCNICOS (REF. TESIS PÁG. 115)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ¿Por qué nuestros pantalones son diferentes?")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.image("https://images.unsplash.com/photo-1613915617430-8ab0fd7c6baf?q=80&w=800&auto=format&fit=crop", caption="Detalle de Tejido Natural")
    
    with col_t2:
        st.markdown("""
        #### 1. LA TELA PRINCIPAL (Shell)
        * **Gabardina Spandex:** Utilizamos una composición **97% Algodón / 3% Elastano**.
        * **Beneficio:** El algodón permite que la piel respire, mientras el 3% de elastano otorga la flexibilidad necesaria para sentarse en la oficina sin que el pantalón 'ahorque'.
        
        #### 2. LA FORRERÍA (Lining) - EL SECRETO
        * **Problema del Mercado:** La mayoría usa *Poliéster* en los bolsillos. El poliéster es plástico, genera calor y se rompe con las llaves.
        * **Nuestra Solución:** Usamos **Popelina 100% Algodón**.
        * **Resultado:** Bolsillos frescos, hipoalergénicos y ultra resistentes.
        """)
        
        st.info("💡 **Dato:** Esta especificación técnica reduce la tasa de devolución por incomodidad en un 40%.")

# --- MÓDULO 5: CHECKOUT ---
elif "5. CHECKOUT" in menu:
    st.markdown("""
    <div class="main-header">
        <h1>🛒 CHECKOUT</h1>
        <p>CONFIRMACIÓN DE ORDEN DE CORTE</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.carrito) > 0:
        # Mostrar tabla
        df = pd.DataFrame(st.session_state.carrito)
        
        # Estilizar tabla
        st.dataframe(
            df[["Modelo", "Tela", "Color", "Precio"]], 
            use_container_width=True,
            hide_index=True
        )
        
        total = df["Precio"].sum()
        
        c_tot, c_vacio = st.columns([2, 1])
        with c_tot:
             st.markdown(f"<h1 style='color:{COLOR_BRAND_ACCENT}'>TOTAL: {total} Bs.</h1>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Envío")
        
        c_form1, c_form2 = st.columns(2)
        with c_form1:
            st.selectbox("Ciudad / Zona", ["La Paz - Sopocachi", "La Paz - Sur", "La Paz - Centro", "El Alto"])
            st.text_input("Dirección Exacta")
            st.text_input("Referencia")
        
        with c_form2:
            st.text_input("WhatsApp de Contacto")
            st.radio("Método de Pago", ["Transferencia QR (Simple)", "Efectivo contra-entrega"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("CONFIRMAR PEDIDO Y GENERAR ORDEN"):
                with st.spinner("Conectando con Digital Locker... Validando Medidas..."):
                    time.sleep(2)
                
                st.success("¡PEDIDO CONFIRMADO!")
                st.markdown("""
                <div style="background-color:#D5F5E3; padding:20px; border-radius:10px; color:#186A3B;">
                    <h3>✅ Orden de Corte #2026-001 Generada</h3>
                    <p>Las especificaciones han sido enviadas al taller. Se utilizarán los moldes digitales
                    asociados a su ID de cliente.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                st.session_state.carrito = [] # Limpiar
                
    else:
        st.markdown("<div style='text-align:center; padding:50px;'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2038/2038854.png", width=100)
        st.subheader("Tu carrito está vacío")
        st.info("Ve al 'Personalizador' para diseñar tu primer pantalón a medida.")
        st.markdown("</div>", unsafe_allow_html=True)
