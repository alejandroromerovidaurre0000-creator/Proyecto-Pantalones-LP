import streamlit as st
import pandas as pd
import time
import random

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS (Diseño Tecnológico y Limpio) ---
st.markdown("""
    <style>
    /* General */
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; color: #1a1a1a; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #ddd !important;
    }
    
    /* Digital Locker Card */
    .locker-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4B0082;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    /* Precios */
    .big-price {
        font-size: 24px;
        font-weight: bold;
        color: #4B0082;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2e0052;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS MEJORADA ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'tiro': 'Regular', 'fit': 'Slim', 'fidelidad': 'Gold'},
        '1002': {'nombre': 'Samael Gómez Rúa', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'tiro': 'Corto', 'fit': 'Regular', 'fidelidad': 'VIP'},
        '1004': {'nombre': 'Miguel Vidal', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'tiro': 'Regular', 'fit': 'Tailored', 'fidelidad': 'Platinum'},
        '1003': {'nombre': 'Jessica Daza Morales', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'tiro': 'Alto', 'fit': 'Relaxed', 'fidelidad': 'VIP'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. SIDEBAR (CRÉDITOS REALES) ---
with st.sidebar:
    st.title("PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    st.markdown("---")
    st.markdown("**Postulante:** Alejandro M. Romero")
    st.markdown("---")
    st.markdown("### Tribunal Evaluador")
    st.info("Tutora: **Jessica Susana Daza Morales**")
    st.info("Panelista: **Samael Gómez Rúa**")
    st.info("Relator: **Miguel Vidal**")
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "🛠️ PERSONALIZAR PANTALÓN", "🛒 CARRITO"])

# --- 5. LÓGICA DEL SISTEMA ---

# === INICIO ===
if menu == "🏠 INICIO":
    st.title("Pantalonería Integral Masculina")
    st.subheader("La revolución Phygital: Sastrería + Datos.")
    
    # Imagen de portada confiable
    st.image("https://images.pexels.com/photos/1342609/pexels-photo-1342609.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", use_column_width=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1. Escaneo")
        st.write("Visita nuestra tienda en Sopocachi. Te medimos una sola vez.")
    with c2:
        st.markdown("### 2. Digitalización")
        st.write("Tus medidas se guardan en tu perfil único (Digital Locker).")
    with c3:
        st.markdown("### 3. Personalización")
        st.write("Elige tela y modelo desde tu celular. Ajuste perfecto garantizado.")

    st.warning("⚠️ **INSTRUCCIÓN PARA JURADO:** Vaya a 'Digital Locker' e ingrese su ID (Relator: 1004, Panelista: 1002) para ver la simulación completa.")

# === DIGITAL LOCKER (AHORA MÁS COMPLETO) ===
elif menu == "🔐 DIGITAL LOCKER":
    st.title("🔐 Digital Locker | Perfil Biométrico")
    
    col_login, col_data = st.columns([1, 3])
    
    with col_login:
        st.markdown("### Acceso")
        id_input = st.text_input("ID Cliente:", placeholder="Ej: 1004")
        if st.button("Buscar ID"):
            if id_input in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[id_input]
                st.success("Acceso Concedido")
            else:
                st.error("ID No encontrado")
    
    with col_data:
        if st.session_state.usuario:
            u = st.session_state.usuario
            
            # Encabezado del perfil
            st.markdown(f"""
            <div style="background-color:#111; color:white; padding:15px; border-radius:10px;">
                <h2 style="margin:0; color:white;">{u['nombre']}</h2>
                <p style="margin:0; color:#aaa;">Rol: {u['rol']} | Nivel: {u['fidelidad']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # PESTAÑAS PARA QUE NO SE VEA VACÍO
            tab1, tab2, tab3 = st.tabs(["📐 MEDIDAS & MOLDERÍA", "👤 ESCANEO 3D", "📜 HISTORIAL"])
            
            with tab1:
                st.markdown("#### Ficha Técnica de Sastrería")
                c_med1, c_med2, c_med3 = st.columns(3)
                with c_med1:
                    st.metric("Cintura", f"{u['cintura']} cm", "+0.5mm ajuste")
                with c_med2:
                    st.metric("Largo Pierna", f"{u['largo']} cm", "Standard")
                with c_med3:
                    st.metric("Tiro", u['tiro'], "Confort")
                
                st.markdown("---")
                st.markdown(f"**Fit Preferido:** {u['fit']}")
                st.progress(100, text="Patrones digitales listos para corte")

            with tab2:
                col_scan_img, col_scan_txt = st.columns([1, 2])
                with col_scan_img:
                    # Imagen de wireframe (cuerpo 3D)
                    st.image("https://t3.ftcdn.net/jpg/02/03/92/64/360_F_203926476_2cM9cZ4o2r9b9c9c9c9c9c9c9c9c9c9c.jpg", caption="Avatar Digital Generado") # Link genérico de wireframe
                with col_scan_txt:
                    st.info("Último escaneo: 11/02/2026 (Sopocachi)")
                    st.write("Morfología detectada: Ectomorfo")
                    st.write("Hombros: Balanceados")
                    st.write("Postura: Neutral")

            with tab3:
                st.write("No hay pedidos recientes. ¡Personaliza tu primer pantalón!")
                
        else:
            st.info("👈 Ingrese un ID a la izquierda para cargar los datos del cliente.")
            st.image("https://cdn.dribbble.com/users/1256059/screenshots/15454664/media/5e173e6b7c0b0b4b2b4b2b4b2b4b2b4b.png?compress=1&resize=800x600", width=400, caption="Sistema esperando credenciales...")

# === PERSONALIZADOR (SÓLO PANTALONES) ===
elif menu == "🛠️ PERSONALIZAR PANTALÓN":
    st.title("Diseña tu Pantalón")
    
    if st.session_state.usuario:
        st.success(f"Confeccionando para: **{st.session_state.usuario['nombre']}** (Medidas cargadas)")
    
    # Selector de Modelo Principal
    st.subheader("1. Elige el Modelo Base")
    modelo = st.selectbox("Selecciona el corte:", 
                          ["THE CHINO (Oficina/Casual)", 
                           "GURKHA SARTORIAL (Pretina Alta)", 
                           "5-POCKETS (Estilo Jean)", 
                           "CARGO CITY (Urbano)"])
    
    # Columnas para mostrar foto y opciones
    col_img, col_opt = st.columns([1, 1])
    
    # Precios base y lógica de imagen
    precio_base = 0
    img_url = ""
    
    if modelo == "THE CHINO (Oficina/Casual)":
        precio_base = 220
        img_url = "https://images.pexels.com/photos/52518/jeans-pants-blue-shop-52518.jpeg?auto=compress&cs=tinysrgb&w=600" # Chino style
        desc = "Bolsillos sesgados, corte limpio. El estándar para la oficina moderna."
    elif modelo == "GURKHA SARTORIAL (Pretina Alta)":
        precio_base = 350
        img_url = "https://i.pinimg.com/736x/8f/3e/2e/8f3e2e0e0e0e0e0e0e0e0e0e0e0e0e0e.jpg" # Fallback to generic if needed, using a clear pants image
        # Usando link seguro de Unsplash para Gurkha/Sartorial vibe
        img_url = "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80"
        desc = "Cierre cruzado en cintura, doble pinza. Elegancia clásica sin usar traje."
    elif modelo == "5-POCKETS (Estilo Jean)":
        precio_base = 200
        img_url = "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=600&q=80"
        desc = "La construcción robusta de un jean, pero en la tela que tú elijas."
    elif modelo == "CARGO CITY (Urbano)":
        precio_base = 240
        img_url = "https://images.unsplash.com/photo-1517445312882-1dd682bc8d96?auto=format&fit=crop&w=600&q=80"
        desc = "Bolsillos laterales funcionales. Silueta ajustada (no holgada)."

    with col_img:
        st.image(img_url, caption=modelo, use_column_width=True)
        st.info(desc)

    with col_opt:
        st.subheader("2. Elige la Tela")
        tela = st.radio("Material disponible:", 
                        ["Gabardina Spandex (97% Algodón)", 
                         "Dril Pesado (100% Algodón)", 
                         "Lana Fría Super 100's (Premium)", 
                         "Pana / Corduroy (Invierno)"])
        
        # Lógica de precios dinámica
        precio_final = precio_base
        if "Lana" in tela:
            precio_final += 200 # La lana es cara
            st.caption("✨ La Lana Fría añade +200 Bs por ser importada.")
        elif "Pana" in tela:
            precio_final += 40
        
        st.subheader("3. Color")
        color = st.selectbox("Tono:", ["Azul Navy", "Negro Profundo", "Kaki / Arena", "Gris Oxford", "Verde Olivo"])
        
        st.divider()
        st.markdown(f"### Precio Final: <span class='big-price'>{precio_final} Bs.</span>", unsafe_allow_html=True)
        
        if st.button("AÑADIR AL PEDIDO", type="primary"):
            item = {
                "Modelo": modelo,
                "Tela": tela,
                "Color": color,
                "Precio": precio_final
            }
            st.session_state.carrito.append(item)
            st.balloons()
            st.success("¡Pantalón configurado y añadido!")

# === CARRITO ===
elif menu == "🛒 CARRITO":
    st.title("Finalizar Compra")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True)
        
        total = df['Precio'].sum()
        st.markdown(f"<div style='text-align:right; font-size:30px;'>Total: <b>{total} Bs.</b></div>", unsafe_allow_html=True)
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("WhatsApp de Contacto")
            st.selectbox("Zona de Entrega", ["Sopocachi", "Sur", "Centro", "El Alto"])
        with c2:
            if st.button("CONFIRMAR ORDEN DE CORTE"):
                with st.spinner("Enviando especificaciones al taller..."):
                    time.sleep(2)
                st.success("PEDIDO ENVIADO. Nos contactaremos para el pago QR.")
                st.session_state.carrito = []
    else:
        st.info("Tu carrito está vacío.")

