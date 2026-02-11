import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Pantalonería Integral - Proyecto de Grado",
    page_icon="👖",
    layout="wide"
)

# --- 2. ESTILOS VISUALES (Identidad Corporativa) ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B0082; /* Morado Institucional */
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #4B0082;
    }
    .stButton>button {
        width: 100%;
        background-color: #1a1a1a;
        color: white;
    }
    .stButton>button:hover {
        background-color: #4B0082;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS SIMULADA (Digital Locker) ---
# Aquí están los datos precargados para la demostración
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'cintura': 82, 'largo': 104, 'tiro': 'Regular', 'fit': 'Slim Fit'},
        '1002': {'nombre': 'Samael Gómez (Jurado)', 'cintura': 90, 'largo': 100, 'tiro': 'Corto', 'fit': 'Regular'},
        '1003': {'nombre': 'Jessica Daza (Tutora)', 'cintura': 78, 'largo': 98, 'tiro': 'Alto', 'fit': 'Relaxed'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. BARRA LATERAL (Créditos Académicos) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800201.png", width=80)
    st.title("Proyecto de Grado")
    st.caption("Ingeniería Comercial - UCB 2026")
    st.markdown("---")
    st.info("**Postulante:** Alejandro Manuel Romero Vidaurre")
    st.text(f"Tutora: Jessica Susana Daza Morales")
    st.text(f"Panelista: Samael Gómez Rúa")
    st.markdown("---")
    menu = st.radio("Navegación:", ["🏠 Inicio", "🔐 Digital Locker", "👖 Catálogo", "🛒 Carrito"])

# --- 5. LÓGICA DE NAVEGACIÓN ---

if menu == "🏠 Inicio":
    st.markdown("<div class='main-header'>PANTALONERÍA INTEGRAL MASCULINA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Modelo Phygital: Sastrería + Tecnología en La Paz</div>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1593030761757-71bd90dbe3e4?q=80&w=1000&auto=format&fit=crop", use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📍 Fase 1: Tienda Física")
        st.write("Ubicada en **Sopocachi**. El cliente viene, toca las telas y realizamos el **Escaneo Digital** de medidas.")
    with col2:
        st.markdown("### ☁️ Fase 2: Digital Locker")
        st.write("Las medidas se guardan en la nube. El cliente ya no necesita volver a probarse nunca más.")
    with col3:
        st.markdown("### 🚀 Fase 3: E-Commerce")
        st.write("Pedidos online con ajuste garantizado. Entrega en 24 horas en La Paz.")

    st.success("💡 **Para la demo:** Ve a 'Digital Locker' e ingresa el código **1002**.")

elif menu == "🔐 Digital Locker":
    st.header("🔐 Acceso a Perfil Biométrico")
    st.markdown("Simulación: El cliente ingresa su ID único para recuperar sus medidas exactas.")
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        id_input = st.text_input("Ingresa tu ID de Cliente:", placeholder="Ej: 1001, 1002...")
    with col_btn:
        st.write("")
        st.write("")
        btn_login = st.button("🔍 Buscar Medidas")

    if btn_login:
        if id_input in st.session_state.db_clientes:
            user = st.session_state.db_clientes[id_input]
            st.session_state.usuario = user
            
            st.success(f"¡Bienvenido de nuevo, {user['nombre']}!")
            st.markdown(f"""
            <div class='metric-card'>
                <h3>📋 Ficha Técnica Digital</h3>
                <p>El sistema ha cargado tus patrones de corte:</p>
                <ul>
                    <li><strong>Cintura:</strong> {user['cintura']} cm</li>
                    <li><strong>Largo de Pierna:</strong> {user['largo']} cm</li>
                    <li><strong>Tiro:</strong> {user['tiro']}</li>
                    <li><strong>Preferencia de Fit:</strong> {user['fit']}</li>
                </ul>
                <p><em>Estado: Listo para producción.</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("ID no encontrado en la base de datos.")

elif menu == "👖 Catálogo":
    st.header("Colección 2026")
    
    if st.session_state.usuario:
        st.info(f"✅ Precios y tallas ajustados para: **{st.session_state.usuario['nombre']}**")
    else:
        st.warning("⚠️ Modo Invitado: Se usarán tallas estándar.")

    tab1, tab2 = st.tabs(["Línea Estándar (Diario)", "Línea Premium (Ejecutivo)"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=400&q=80")
            st.subheader("Gabardina Office")
            st.write("Ideal para trabajo diario. Resistente y fresco.")
            st.markdown("**Precio: 240 Bs.**")
            if st.button("Añadir Gabardina"):
                st.session_state.carrito.append({"Item": "Gabardina Office", "Precio": 240})
                st.toast("Producto añadido")
        with c2:
            st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=400&q=80")
            st.subheader("Jeans Dril Confort")
            st.write("Con elastano para máxima movilidad.")
            st.markdown("**Precio: 200 Bs.**")
            if st.button("Añadir Dril"):
                st.session_state.carrito.append({"Item": "Jeans Dril", "Precio": 200})
                st.toast("Producto añadido")

    with tab2:
        c3, c4 = st.columns(2)
        with c3:
            st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=400&q=80")
            st.subheader("Lana Fría Sastre")
            st.write("Termicidad regulada para el clima de La Paz.")
            st.markdown("**Precio: 450 Bs.**")
            if st.button("Añadir Lana Fría"):
                st.session_state.carrito.append({"Item": "Lana Fría", "Precio": 450})
                st.toast("Producto añadido")
        with c4:
            st.image("https://images.unsplash.com/photo-1507680434567-5739c8fbe69d?auto=format&fit=crop&w=400&q=80")
            st.subheader("Casimir Importado")
            st.write("Acabados de lujo y forrería reforzada.")
            st.markdown("**Precio: 480 Bs.**")
            if st.button("Añadir Casimir"):
                st.session_state.carrito.append({"Item": "Casimir", "Precio": 480})
                st.toast("Producto añadido")

elif menu == "🛒 Carrito":
    st.header("Resumen de Pedido")
    
    if len(st.session_state.carrito) > 0:
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        total = df["Precio"].sum()
        
        st.markdown(f"### Total a Pagar: {total} Bs.")
        
        st.markdown("---")
        st.subheader("Detalles de Entrega")
        
        # Formulario de checkout
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            nombre = st.text_input("Nombre Completo:", value=st.session_state.usuario['nombre'] if st.session_state.usuario else "")
            celular = st.text_input("WhatsApp de contacto:")
        with col_form2:
            zona = st.selectbox("Zona de Entrega:", ["Sopocachi (Gratis)", "Centro", "Miraflores", "Zona Sur (Calacoto/Obrajes)", "El Alto"])
            pago = st.radio("Método de Pago:", ["QR Simple", "Transferencia", "Efectivo contra-entrega"])

        if st.button("✅ FINALIZAR COMPRA"):
            if not celular:
                st.error("Por favor ingresa un número de contacto.")
            else:
                with st.spinner("Procesando medidas y generando orden..."):
                    time.sleep(2)
                st.balloons()
                st.success("¡Pedido Confirmado!")
                st.info(f"""
                Se ha generado la orden #2026-001.
                - **Cliente:** {nombre}
                - **Zona:** {zona}
                - **Total:** {total} Bs.
                
                Gracias por apoyar la industria nacional.
                """)
                st.session_state.carrito = [] # Limpiar carrito
    else:
        st.info("Tu carrito está vacío. Ve al catálogo para seleccionar tus productos.")