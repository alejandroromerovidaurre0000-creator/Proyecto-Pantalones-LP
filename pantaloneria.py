import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS VISUALES (MARCA PROPIA) ---
st.markdown("""
    <style>
    /* Fondo limpio */
    .stApp { background-color: #ffffff; }
    
    /* LOGO DIGITAL (Simulado con CSS) */
    .logo-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1a1a1a 0%, #4B0082 100%);
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .brand-name {
        color: white;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        letter-spacing: 2px;
        margin: 0;
    }
    .brand-slogan {
        color: #d1d1d1;
        font-size: 1rem;
        font-style: italic;
    }
    
    /* Tarjetas de Producto */
    .product-box {
        border: 1px solid #eee;
        border-radius: 15px;
        padding: 20px;
        background: white;
        transition: transform 0.2s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .product-box:hover {
        transform: translateY(-5px);
        border-color: #4B0082;
    }
    
    /* Precios */
    .price-tag {
        color: #4B0082;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    /* Botones */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1a1a1a;
        color: white;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #4B0082; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS ROBUSTA ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'fit': 'Slim'},
        '1002': {'nombre': 'Lic. Samael Gómez', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'fit': 'Regular'},
        '1003': {'nombre': 'Lic. Jessica Daza', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed'},
        '1004': {'nombre': 'Lic. Miguel Vidal', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'fit': 'Tailored'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. FUNCIÓN INTELIGENTE DE IMÁGENES (CAMBIO DE COLOR) ---
def obtener_imagen(modelo, color):
    # Base de datos de URLs por color para simular el cambio
    # MODELO 1: CHINO / GABARDINA
    if "Gabardina" in modelo or "Chino" in modelo:
        if "Azul" in color: return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80"
        if "Beige" in color or "Kaki" in color: return "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=600&q=80"
        if "Negro" in color: return "https://images.unsplash.com/photo-1517445312882-1dd682bc8d96?auto=format&fit=crop&w=600&q=80"
        if "Verde" in color: return "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=600&q=80"
        return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80" # Default
    
    # MODELO 2: LANA / SEMI FORMAL
    if "Lana" in modelo or "Sartorial" in modelo:
        if "Gris" in color: return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80" # Gris clásico
        if "Negro" in color: return "https://images.pexels.com/photos/1342609/pexels-photo-1342609.jpeg?auto=compress&cs=tinysrgb&w=600"
        if "Azul" in color: return "https://images.pexels.com/photos/5325886/pexels-photo-5325886.jpeg?auto=compress&cs=tinysrgb&w=600"
        return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80"

    # MODELO 3: CASUAL / 5 POCKETS
    return "https://images.unsplash.com/photo-1604176354204-9268737828c4?auto=format&fit=crop&w=600&q=80"

# --- 5. INTERFAZ PRINCIPAL ---

# Header con Logo Simulado
st.markdown("""
<div class="logo-container">
    <h1 class="brand-name">PANTALONERÍA INTEGRAL</h1>
    <p class="brand-slogan">Sastrería Phygital & Personalización</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### PANEL DE CONTROL")
    menu = st.radio("Ir a:", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "🛠️ PERSONALIZAR", "🛒 CARRITO"])
    
    st.divider()
    st.markdown("**PROYECTO DE GRADO**")
    st.caption("Ingeniería Comercial 2026")
    st.markdown("**Tribunal:**")
    st.caption("• Jessica Daza (Tutora)\n• Samael Gómez (Panelista)\n• Miguel Vidal (Relator)")

# === 1. INICIO ===
if menu == "🏠 INICIO":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Bienvenido a la Nueva Sastrería")
        st.write("Olvídate de tallas genéricas. Olvídate de los trajes incómodos. Nos especializamos 100% en pantalones a medida con tecnología digital.")
        
        st.info("💡 **Diferenciador (Pág 115):** Usamos forrería de Popelina 100% Algodón para evitar sudoración, a diferencia de las marcas comerciales que usan poliéster.")
        
    with col2:
        # Imagen de calidad (Telas/Sastrería)
        st.image("https://images.unsplash.com/photo-1620799140408-ed5341cd2431?q=80&w=800&auto=format&fit=crop", caption="Materiales Premium y Moldería Digital")

# === 2. DIGITAL LOCKER (CORREGIDO) ===
elif menu == "🔐 DIGITAL LOCKER":
    st.subheader("Acceso a Perfil Biométrico")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        id_user = st.text_input("Ingrese ID (Ej: 1004):")
        if st.button("BUSCAR PERFIL"):
            # Lógica corregida con .get() para evitar errores
            usuario = st.session_state.db_clientes.get(id_user)
            if usuario:
                st.session_state.usuario = usuario
                st.success("¡Perfil Encontrado!")
            else:
                st.error("ID no existe. Intente con 1002 o 1004.")

    with c2:
        if st.session_state.usuario:
            u = st.session_state.usuario
            st.markdown(f"""
            <div class="product-box">
                <h3 style="color:#4B0082">{u['nombre']}</h3>
                <p><b>Rol:</b> {u['rol']}</p>
                <hr>
                <div style="display:flex; justify-content:space-between;">
                    <div><h2>{u['cintura']} cm</h2><small>Cintura</small></div>
                    <div><h2>{u['largo']} cm</h2><small>Largo</small></div>
                    <div><h2>{u['fit']}</h2><small>Fit</small></div>
                </div>
                <br>
                <p style="color:green">✅ Medidas digitales verificadas.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Esperando identificación...")

# === 3. PERSONALIZADOR (EL PLATO FUERTE) ===
elif menu == "🛠️ PERSONALIZAR":
    st.subheader("Diseña tu Pantalón Único")
    
    if st.session_state.usuario:
        st.success(f"Configurando medidas para: **{st.session_state.usuario['nombre']}**")
    
    # PASO 1: MODELO
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.markdown("##### 1. Elige el Modelo")
        modelo = st.selectbox("Tipo de Pantalón:", 
            ["Chino Gabardina (Uso Diario)", "Sartorial Lana (Semi-Formal)", "5-Pockets (Casual/Fin de semana)"])
        
        st.markdown("##### 2. Elige el Color")
        # Opciones de color dinámicas según modelo
        opciones_color = []
        if "Gabardina" in modelo:
            opciones_color = ["Azul Marino", "Kaki Beige", "Verde Oliva", "Negro"]
        elif "Lana" in modelo:
            opciones_color = ["Gris Oxford", "Azul Noche", "Negro Profundo"]
        else:
            opciones_color = ["Azul Denim", "Café Tierra", "Gris Humo"]
            
        color = st.radio("Tonos Disponibles:", opciones_color, horizontal=True)
        
        st.markdown("##### 3. Elige la Tela")
        tela = st.selectbox("Material:", ["Estándar", "Premium (Importada)"])

    # LÓGICA DE ACTUALIZACIÓN DE IMAGEN Y PRECIO
    with col_der:
        # Obtener URL dinámica
        img_actual = obtener_imagen(modelo, color)
        
        # Calcular Precio
        precio = 200
        if "Gabardina" in modelo: precio = 240
        if "Lana" in modelo: precio = 450
        if tela == "Premium (Importada)" and "Lana" not in modelo: precio += 50
        
        # Mostrar Tarjeta
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        st.image(img_actual, caption=f"Vista Previa: {color}", use_column_width=True)
        
        st.markdown(f"""
        <div style="text-align:center;">
            <h3>{modelo}</h3>
            <p>{color} | Tela {tela}</p>
            <div class="price-tag">{precio} Bs.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("AÑADIR AL PEDIDO"):
            st.session_state.carrito.append({
                "Modelo": modelo, "Color": color, "Tela": tela, "Precio": precio
            })
            st.balloons()
            st.toast("¡Producto Agregado!")
        st.markdown('</div>', unsafe_allow_html=True)

# === 4. CARRITO ===
elif menu == "🛒 CARRITO":
    st.subheader("Finalizar Pedido")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True)
        
        total = df['Precio'].sum()
        st.markdown(f"### Total a Pagar: **{total} Bs.**")
        
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("WhatsApp")
            st.selectbox("Zona Entrega", ["Sopocachi", "Sur", "Centro", "El Alto"])
        with c2:
            st.info("Al confirmar, se generará la orden de corte con tus medidas del Digital Locker.")
            if st.button("CONFIRMAR COMPRA"):
                with st.spinner("Procesando..."):
                    time.sleep(2)
                st.success("¡Pedido Enviado!")
                st.session_state.carrito = []
    else:
        st.warning("Tu carrito está vacío.")
