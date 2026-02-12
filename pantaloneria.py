import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN VISUAL Y ESTILO (BRANDING)
# ==============================================================================
st.set_page_config(
    page_title="Pantalonería Integral | Tesis 2026",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de Colores (Seria y Tecnológica)
COLOR_MAIN = "#1C2833"  # Negro/Azul Oscuro
COLOR_ACCENT = "#5B2C6F" # Morado (Innovación)
COLOR_BG = "#FDFEFE"    # Blanco Hueso

st.markdown(f"""
    <style>
    /* Estilos Generales */
    .stApp {{ background-color: {COLOR_BG}; }}
    h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {COLOR_MAIN}; }}
    
    /* Header Principal */
    .hero-header {{
        background: linear-gradient(90deg, {COLOR_MAIN} 0%, {COLOR_ACCENT} 100%);
        padding: 40px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    .hero-title {{ font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin: 0; }}
    .hero-subtitle {{ font-size: 1.2rem; font-weight: 300; opacity: 0.9; margin-top: 10px; }}

    /* Tarjetas de Producto */
    .product-card {{
        background: white;
        border: 1px solid #E5E7E9;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }}
    .product-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(91, 44, 111, 0.15);
        border-color: {COLOR_ACCENT};
    }}

    /* Etiquetas */
    .role-badge {{
        background-color: #E8F8F5;
        color: #117864;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        border: 1px solid #A3E4D7;
    }}

    /* Botones */
    .stButton>button {{
        width: 100%;
        background-color: {COLOR_MAIN};
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: 600;
        border: none;
    }}
    .stButton>button:hover {{ background-color: {COLOR_ACCENT}; color: white; }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{ background-color: #F2F3F4; }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MOTOR DE IMÁGENES (SOLO PANTALONES - SIN TRAJES)
# ==============================================================================
# He verificado estos links para que sean solo texturas, piernas o pantalones doblados.

def obtener_foto(modelo, color):
    # --- MODELO CHINO (Gabardina) ---
    if "Chino" in modelo:
        if "Azul" in color: return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80" # Piernas pantalón azul
        if "Beige" in color: return "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80" # Pantalón beige colgado
        if "Verde" in color: return "https://images.unsplash.com/photo-1517445312882-1dd682bc8d96?auto=format&fit=crop&w=800&q=80" # Pantalón oscuro/verde
        return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80"
    
    # --- MODELO 5-POCKETS (Casual) ---
    elif "5-Pockets" in modelo:
        if "Azul" in color: return "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=800&q=80" # Jean texture
        if "Negro" in color: return "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=800" # Jean negro
        if "Gris" in color: return "https://images.pexels.com/photos/2343661/pexels-photo-2343661.jpeg?auto=compress&cs=tinysrgb&w=800"
        return "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=800&q=80"
    
    # --- MODELO SARTORIAL (Lana - Pantalón de Vestir) ---
    elif "Sartorial" in modelo:
        # Usamos fotos de TEXTURAS o piernas solas, NUNCA trajes completos
        if "Gris" in color: return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80" # Tela Gris Sastre
        if "Negro" in color: return "https://images.pexels.com/photos/1342609/pexels-photo-1342609.jpeg?auto=compress&cs=tinysrgb&w=800" # Pantalón negro detalle
        if "Azul" in color: return "https://images.pexels.com/photos/3755706/pexels-photo-3755706.jpeg?auto=compress&cs=tinysrgb&w=800" # Tela Azul Sastre
        return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80"

    return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80"

# ==============================================================================
# 3. BASE DE DATOS (CORREGIDA SIN "LIC.")
# ==============================================================================
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'fit': 'Slim', 'data': [4,3,4,4,5]},
        # JURADO - SIN "LIC"
        '1002': {'nombre': 'Samael Gómez Rúa', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'fit': 'Regular Comfort', 'data': [5,4,3,3,4]},
        '1003': {'nombre': 'Jessica Susana Daza', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed', 'data': [3,5,2,4,3]},
        '1004': {'nombre': 'Miguel Vidal Sejas', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'fit': 'Tailored', 'data': [4,4,4,4,4]}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# ==============================================================================
# 4. BARRA LATERAL (DATOS ACADÉMICOS)
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800201.png", width=60)
    st.markdown("### PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    
    st.markdown("---")
    st.markdown("**Postulante:**\nAlejandro M. Romero V.")
    st.markdown("---")
    
    # SECCIÓN TRIBUNAL (CORREGIDA)
    with st.expander("⚖️ TRIBUNAL EVALUADOR", expanded=True):
        st.markdown("**Tutora:**")
        st.caption("Jessica Susana Daza Morales")
        st.markdown("**Panelista:**")
        st.caption("Samael Gómez Rúa")
        st.markdown("**Relator:**")
        st.caption("Miguel Vidal Sejas")
    
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "🛠️ PERSONALIZADOR", "🛒 CARRITO"])

# ==============================================================================
# 5. LÓGICA DE PÁGINAS
# ==============================================================================

# --- INICIO ---
if menu == "🏠 INICIO":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">PANTALONERÍA INTEGRAL</h1>
        <p class="hero-subtitle">SASTRERÍA DIGITAL • CERO TRAJES • SOLO PANTALONES</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 1])
    
    with col_img:
        # Foto de Inicio: Un sastre midiendo o telas (NO UN TRAJE)
        st.image("https://images.unsplash.com/photo-1620799140408-ed5341cd2431?q=80&w=1000&auto=format&fit=crop", 
                 caption="Taller Phygital en Sopocachi", use_column_width=True)
    
    with col_txt:
        st.markdown("### 💡 La Propuesta (Tesis)")
        st.markdown("""
        El mercado actual te obliga a comprar **trajes completos** de mala calidad o pantalones de tallas genéricas.
        
        **Nuestra solución:**
        1.  **Especialización:** Solo pantalones. Nada más.
        2.  **Tecnología:** Escaneo de medidas (Digital Locker).
        3.  **Calidad (Pág. 115):** Usamos **Popelina 100% Algodón** en la forrería, no poliéster barato.
        """)
        
        st.info("ℹ️ **Instrucción:** Para demostrar el sistema al tribunal, vaya a 'Digital Locker' e ingrese el ID **1004** (Relator).")

# --- DIGITAL LOCKER ---
elif menu == "🔐 DIGITAL LOCKER":
    st.markdown("## 🔐 Perfil Biométrico del Cliente")
    st.write("Base de datos de moldería digital. Ingrese el ID para recuperar las medidas.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        id_input = st.text_input("Ingrese ID (Ej: 1004):")
        if st.button("BUSCAR EXPEDIENTE"):
            user = st.session_state.db_clientes.get(id_input)
            if user:
                st.session_state.usuario = user
                st.success("¡Perfil Cargado!")
                time.sleep(0.5)
            else:
                st.error("ID no encontrado. Pruebe 1002, 1003 o 1004.")
    
    with c2:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Tarjeta de Datos
            st.markdown(f"""
            <div class="product-card">
                <h2 style="color:{COLOR_ACCENT}; margin:0;">{u['nombre']}</h2>
                <span class="role-badge">{u['rol']}</span>
                <hr>
                <div style="display:flex; justify-content:space-between; text-align:center;">
                    <div><h1>{u['cintura']}</h1><small>CM CINTURA</small></div>
                    <div><h1>{u['largo']}</h1><small>CM LARGO</small></div>
                    <div><h1>{u['fit']}</h1><small>TIPO DE FIT</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico Radar (Plotly)
            st.markdown("### 📊 Análisis de Morfología")
            categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=u['data'], theta=categories, fill='toself', name=u['nombre'], line_color=COLOR_ACCENT
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("👈 Ingrese un ID para ver la simulación.")

# --- PERSONALIZADOR (SIN TRAJES) ---
elif menu == "🛠️ PERSONALIZADOR":
    st.markdown("## 🛠️ Atelier de Diseño")
    st.write("Configura tu pantalón ideal. El precio se ajusta según la tela seleccionada.")

    if st.session_state.usuario:
        st.success(f"Diseñando para: **{st.session_state.usuario['nombre']}** (Medidas cargadas)")

    # 1. SELECCIÓN DE MODELO
    col_mod1, col_mod2 = st.columns([1, 1])
    
    with col_mod1:
        st.markdown("### 1. Elige Modelo y Tela")
        modelo = st.selectbox("Modelo Base:", 
                             ["Chino Gabardina (Uso Diario)", 
                              "5-Pockets (Casual Tipo Jean)", 
                              "Sartorial (Pantalón de Vestir - Lana)"])
        
        # Opciones de Tela según Modelo
        tela = "Estándar"
        precio_base = 0
        
        if "Chino" in modelo:
            tela = st.selectbox("Tela:", ["Gabardina Spandex (97% Algodón)", "Dril Pesado"])
            precio_base = 240
        elif "5-Pockets" in modelo:
            tela = st.selectbox("Tela:", ["Dril Confort", "Pana / Corduroy"])
            precio_base = 200
        elif "Sartorial" in modelo:
            tela = st.selectbox("Tela:", ["Lana Fría Super 100's (Importada)", "Casimir Nacional"])
            precio_base = 450 # Más caro
            
        st.markdown("### 2. Elige Color")
        # Colores dinámicos
        colores = []
        if "Chino" in modelo: colores = ["Azul Marino", "Kaki / Beige", "Verde Oliva"]
        elif "5-Pockets" in modelo: colores = ["Azul Denim", "Negro", "Gris"]
        elif "Sartorial" in modelo: colores = ["Gris Oxford", "Negro", "Azul Noche"]
        
        color = st.radio("Tonos:", colores, horizontal=True)

    with col_mod2:
        st.markdown("### Vista Previa")
        
        # OBTENER FOTO DINÁMICA
        foto_url = obtener_foto(modelo, color)
        
        st.image(foto_url, caption=f"Visualización: {color}", use_column_width=True)
        
        # Tarjeta de Precio
        st.markdown(f"""
        <div class="product-card" style="text-align:center;">
            <h3 style="margin:0;">{modelo}</h3>
            <p style="color:gray;">{tela} | {color}</p>
            <h1 style="color:{COLOR_ACCENT}; font-size: 3rem;">{precio_base} Bs.</h1>
            <small>Incluye Forrería Popelina 100% (Tesis Pág. 115)</small>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("AÑADIR AL PEDIDO"):
            st.session_state.carrito.append({"Modelo": modelo, "Tela": tela, "Color": color, "Precio": precio_base})
            st.balloons()
            st.success("¡Agregado al carrito!")

# --- CARRITO ---
elif menu == "🛒 CARRITO":
    st.markdown("## 🛒 Confirmación de Orden")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align:right'>Total: {total} Bs.</h2>", unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.text_input("WhatsApp")
            st.selectbox("Zona", ["Sopocachi", "Sur", "Centro", "El Alto"])
        with col_f2:
            if st.button("CONFIRMAR Y ENVIAR A TALLER"):
                with st.spinner("Procesando..."):
                    time.sleep(2)
                st.success("¡Orden Enviada!")
                st.info("El taller ha recibido tus medidas digitales y la selección de tela.")
                st.session_state.carrito = []
    else:
        st.info("Carrito vacío.")
