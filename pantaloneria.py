import streamlit as st
import pandas as pd
import time
import random

# --- 1. CONFIGURACIÓN PREMIUM DE LA PÁGINA ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS "ULTRA PRO" (Diseño Limpio y Académico) ---
st.markdown("""
    <style>
    /* Tipografía y Fondos */
    .stApp { background-color: #Fdfdfd; }
    
    /* Encabezados */
    h1, h2, h3 { color: #1B2631; font-family: 'Helvetica Neue', sans-serif; }
    .highlight { color: #4B0082; font-weight: bold; }
    
    /* Tarjetas de Métricas (Digital Locker) */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 6px solid #4B0082; /* Morado Institucional */
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: scale(1.02); }
    
    /* Botones Personalizados */
    .stButton>button {
        background-color: #1B2631; /* Negro/Azul Oscuro */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: 500;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #4B0082; /* Cambio a Morado al pasar el mouse */
        box-shadow: 0 4px 12px rgba(75, 0, 130, 0.3);
    }
    
    /* Ficha Técnica */
    .tech-spec {
        font-size: 0.85rem;
        color: #555;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DIGITAL LOCKER (Base de Datos Realista) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'cintura': 82, 'largo': 104, 'tiro': 'Regular', 'fit': 'Slim Fit'},
        # JURADO 1
        '1002': {'nombre': 'Lic. Samael Gómez (Panelista)', 'cintura': 94, 'largo': 100, 'tiro': 'Corto', 'fit': 'Regular Comfort'},
        # JURADO 2 (NUEVO)
        '1004': {'nombre': 'Lic. Miguel Vidal (Relator)', 'cintura': 88, 'largo': 102, 'tiro': 'Regular', 'fit': 'Tailored Fit'},
        # TUTORA
        '1003': {'nombre': 'Lic. Jessica Daza (Tutora)', 'cintura': 70, 'largo': 95, 'tiro': 'Alto', 'fit': 'Relaxed'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. SIDEBAR ACADÉMICO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800201.png", width=70)
    st.markdown("### Proyecto de Grado")
    st.caption("Ingeniería Comercial - UCB 2026")
    st.markdown("---")
    st.markdown("**Postulante:**\nAlejandro M. Romero Vidaurre")
    st.markdown("**Tribunal:**")
    st.text("• Lic. Jessica Daza (Tutora)")
    st.text("• Lic. Samael Gómez (Panelista)")
    st.text("• Lic. Miguel Vidal (Relator)")
    st.markdown("---")
    menu = st.radio("Navegación del Sistema:", ["Inicio & Phygital", "🔐 Digital Locker", "👖 Catálogo Técnico", "🛒 Checkout"])

# --- 5. LÓGICA DEL SISTEMA ---

# --- HOME ---
if menu == "Inicio & Phygital":
    st.title("PANTALONERÍA INTEGRAL MASCULINA")
    st.markdown("#### *La fusión entre Sastrería Tradicional y Personalización Digital*")
    
    # Hero Section con imagen de calidad
    st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=1200&q=80", caption="Taller de Confección en Sopocachi", use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎯 **1. Captura de Datos**\n\nEl cliente visita la tienda en Sopocachi una sola vez. Se escanean sus medidas y preferencias de Fit.")
    with col2:
        st.warning("💾 **2. Digital Locker**\n\nCreamos un avatar matemático del cliente. Sus medidas quedan guardadas en la nube para siempre.")
    with col3:
        st.success("📦 **3. Recompra Inteligente**\n\nEl cliente pide nuevos pantalones desde su celular. El sistema ya sabe su talla exacta.")

    st.markdown("---")
    st.error("💡 **DEMO PARA JURADO:** Diríjase a 'Digital Locker' e ingrese el ID **1004** (Lic. Vidal) o **1002** (Lic. Gómez).")

# --- DIGITAL LOCKER ---
elif menu == "🔐 Digital Locker":
    st.title("🔐 Acceso Biométrico")
    st.markdown("El corazón del negocio: Base de datos de moldería personalizada.")
    
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.markdown("#### Identificación")
        id_input = st.text_input("Ingrese ID de Cliente:", placeholder="Ej: 1004")
        if st.button("Buscar Expediente"):
            if id_input in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[id_input]
                st.toast(f"Perfil cargado: {st.session_state.usuario['nombre']}", icon="✅")
            else:
                st.error("ID no encontrado. Pruebe con 1004 o 1002.")
    
    with col_der:
        if st.session_state.usuario:
            user = st.session_state.usuario
            st.markdown(f"### 👤 {user['nombre']}")
            st.markdown(f"**Estado:** Cliente Verificado | **Última visita:** Sopocachi")
            
            # Tarjeta de Datos
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: grid; grid-template-columns: 1fr 1fr;">
                    <div>
                        <p style="color:#888; margin:0;">Cintura Anatómica</p>
                        <h2 style="margin:0;">{user['cintura']} cm</h2>
                    </div>
                    <div>
                        <p style="color:#888; margin:0;">Largo de Pierna</p>
                        <h2 style="margin:0;">{user['largo']} cm</h2>
                    </div>
                </div>
                <hr style="border-top: 1px solid #eee;">
                <div style="display: grid; grid-template-columns: 1fr 1fr;">
                    <div>
                        <p><strong>Tiro:</strong> {user['tiro']}</p>
                    </div>
                    <div>
                        <p><strong>Preferencia Fit:</strong> {user['fit']}</p>
                    </div>
                </div>
                <p style="margin-top:10px; font-size: 0.9em; color: green;">✅ Patrones listos para corte automático.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("waiting for input... (Ingrese un ID a la izquierda)")

# --- CATÁLOGO ---
elif menu == "👖 Catálogo Técnico":
    st.title("Colección & Fichas Técnicas")
    
    if st.session_state.usuario:
        st.success(f"Confeccionando a medida exacta para: **{st.session_state.usuario['nombre']}**")
    else:
        st.warning("⚠️ Visualizando tallas estándar (Inicie sesión en Locker para activar personalización).")

    tab_std, tab_prem = st.tabs(["LÍNEA ESTÁNDAR (Casual)", "LÍNEA PREMIUM (Sartorial)"])
    
    # --- LÍNEA ESTÁNDAR ---
    with tab_std:
        st.caption("Referencia Tesis: Pág. 115 - Ficha Técnica Gabardina")
        c1, c2 = st.columns(2)
        
        # PRODUCTO 1: AZUL MARINO
        with c1:
            st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80", height=300)
            st.markdown("### Gabardina Spandex - Azul Marino")
            st.markdown("**Precio: 240 Bs.**")
            
            with st.expander("📄 Ver Ficha Técnica (Tesis Pág. 115)"):
                st.markdown("""
                - **Composición:** 97% Algodón / 3% Elastano.
                - **Tejido:** Dril elastizado de alta densidad.
                - **Forrería:** Popelina 100% Algodón (Anti-transpirante).
                - **Uso:** Diario / Oficina Casual.
                """)
            
            if st.button("Añadir al Pedido", key="p1"):
                st.session_state.carrito.append({"Item": "Gabardina Azul Marino", "Linea": "Estándar", "Precio": 240})
                st.toast("Agregado!")

        # PRODUCTO 2: KAKI
        with c2:
            st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=600&q=80", height=300)
            st.markdown("### Gabardina Spandex - Kaki / Beige")
            st.markdown("**Precio: 240 Bs.**")
            
            with st.expander("📄 Ver Ficha Técnica (Tesis Pág. 115)"):
                st.markdown("""
                - **Composición:** 97% Algodón / 3% Elastano.
                - **Beneficio:** Confort dinámico (estira al sentarse).
                - **Forrería:** Popelina 100% Algodón (Evita roturas de bolsillo).
                - **Uso:** Viernes casual / Universidad.
                """)
            
            if st.button("Añadir al Pedido", key="p2"):
                st.session_state.carrito.append({"Item": "Gabardina Kaki", "Linea": "Estándar", "Precio": 240})
                st.toast("Agregado!")

    # --- LÍNEA PREMIUM ---
    with tab_prem:
        st.caption("Referencia Tesis: Pág. 115 - Ficha Técnica Lana Fría")
        c3, c4 = st.columns(2)
        
        # PRODUCTO 3: GRIS OXFORD
        with c3:
            st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=600&q=80", height=300)
            st.markdown("### Lana Super 100's - Gris Oxford")
            st.markdown("**Precio: 450 Bs.**")
            
            with st.expander("📄 Ver Ficha Técnica (Tesis Pág. 115)"):
                st.markdown("""
                - **Composición:** 100% Lana Fría (Super 100's).
                - **Origen:** Importado (Casimir de alto micronaje).
                - **Termicidad:** Regulada (Ideal clima de La Paz).
                - **Forrería:** Popelina 100% Algodón mercerizado.
                """)
            
            if st.button("Añadir al Pedido", key="p3"):
                st.session_state.carrito.append({"Item": "Lana Super 100's Gris", "Linea": "Premium", "Precio": 450})
                st.toast("Agregado!")
        
        # PRODUCTO 4: TEXTO EXPLICATIVO
        with c4:
            st.info("🌟 **Diferenciador de Calidad**")
            st.markdown("""
            A diferencia de la competencia que usa forros sintéticos (poliéster) que generan calor y mal olor, 
            nuestra tesis propone **Forrería de Popelina 100% Algodón** en todas las gamas.
            
            Esto garantiza:
            1. Frescura.
            2. Durabilidad de los bolsillos.
            3. Hipoalergénico.
            """)

# --- CHECKOUT ---
elif menu == "🛒 Checkout":
    st.title("Finalizar Compra")
    
    if len(st.session_state.carrito) > 0:
        # Tabla resumen
        df_cart = pd.DataFrame(st.session_state.carrito)
        st.table(df_cart)
        
        total = df_cart['Precio'].sum()
        st.markdown(f"<h2 style='text-align: right;'>Total: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Logística de Entrega (La Paz)")
        
        c_form1, c_form2 = st.columns(2)
        with c_form1:
            zona = st.selectbox("Zona de Cobertura:", ["Sopocachi (Gratis)", "Centro", "Miraflores", "Obrajes", "Calacoto", "El Alto"])
            direccion = st.text_area("Dirección / Referencia:", placeholder="Ej: Edificio Alborada, Piso 3...")
        with c_form2:
            pago = st.radio("Método de Pago:", ["QR Simple", "Transferencia", "Efectivo contra-entrega"])
            celular = st.text_input("WhatsApp de Contacto:", placeholder="70000000")

        if st.button("CONFIRMAR PEDIDO (Simulación)"):
            if not celular:
                st.error("Por favor ingrese un número de contacto.")
            else:
                # Simulación de proceso
                with st.spinner('⏳ Verificando stock de tela...'):
                    time.sleep(1)
                with st.spinner('📐 Cruzando datos con tu Digital Locker...'):
                    time.sleep(1)
                
                # Éxito
                order_id = random.randint(1000, 9999)
                st.balloons()
                st.success(f"¡Pedido #{order_id} Confirmado!")
                
                cliente_nombre = st.session_state.usuario['nombre'] if st.session_state.usuario else "Invitado"
                
                st.markdown(f"""
                <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; border: 1px solid #c3e6cb;">
                    <h4 style="color: #155724;">Resumen Enviado a Fábrica:</h4>
                    <ul>
                        <li><strong>Cliente:</strong> {cliente_nombre}</li>
                        <li><strong>Items:</strong> {len(st.session_state.carrito)} prendas</li>
                        <li><strong>Forrería Específica:</strong> Popelina 100% Algodón (Según Ficha Pág. 115)</li>
                        <li><strong>Entrega:</strong> {zona}</li>
                    </ul>
                    <p><em>Gracias por validar el modelo de negocio.</em></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.carrito = [] # Limpiar
    else:
        st.info("🛒 Tu carrito está vacío. Ve al Catálogo para seleccionar tus prendas.")
