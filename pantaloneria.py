import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURACIÓN VISUAL (MODO PRESENTACIÓN) ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PERSONALIZADO (ESTILO DE TESIS) ---
st.markdown("""
    <style>
    /* Fondo y fuentes */
    .stApp { background-color: #fcfcfc; }
    h1, h2, h3 { color: #1a1a1a; font-family: 'Arial', sans-serif; font-weight: 700; }
    
    /* Estilo de los Créditos en Sidebar */
    .credit-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        font-size: 0.9rem;
        border-left: 3px solid #4B0082;
    }
    
    /* Tarjetas de Producto en Catálogo */
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .price-tag {
        font-size: 1.5rem;
        color: #4B0082;
        font-weight: bold;
        margin: 10px 0;
    }
    
    /* Botones */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS (DIGITAL LOCKER) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'fit': 'Slim Fit'},
        # CORRECCIÓN DE NOMBRES Y CARGOS
        '1002': {'nombre': 'Samael Gómez Rúa', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'fit': 'Regular Comfort'},
        '1004': {'nombre': 'Miguel Vidal', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'fit': 'Tailored Fit'},
        '1003': {'nombre': 'Jessica Susana Daza Morales', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. BARRA LATERAL (DATOS ACADÉMICOS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800201.png", width=60)
    st.markdown("### PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    
    st.markdown("---")
    st.markdown("**Postulante:** Alejandro M. Romero Vidaurre")
    st.markdown("---")
    
    # Créditos Formateados
    st.markdown("**Tribunal Evaluador:**")
    st.markdown("<div class='credit-box'>Tutora<br><b>Jessica Susana Daza Morales</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='credit-box'>Panelista<br><b>Samael Gómez Rúa</b></div>", unsafe_allow_html=True)
    st.markdown("<div class='credit-box'>Relator<br><b>Miguel Vidal</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("MENÚ DEL SISTEMA", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "👖 CATÁLOGO", "🛒 MI PEDIDO"])

# --- 5. LÓGICA DEL SISTEMA ---

# === INICIO ===
if menu == "🏠 INICIO":
    # Hero Section
    st.markdown("# PANTALONERÍA INTEGRAL MASCULINA")
    st.markdown("### *Modelo Phygital: Donde la sastrería encuentra la tecnología.*")
    
    st.image("https://images.unsplash.com/photo-1593030761757-71bd90dbe3e4?q=80&w=1200&auto=format&fit=crop", use_column_width=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📍 1. Tienda (Sopocachi)")
        st.write("Visita única. Escaneo de medidas y selección de telas. Ubicación estratégica entre el Centro y la Sur.")
    with col2:
        st.markdown("#### ☁️ 2. Digital Locker")
        st.write("Tus medidas se guardan en la nube. Creamos tu 'Avatar' matemático para futuras compras.")
    with col3:
        st.markdown("#### 📦 3. E-Commerce")
        st.write("Pide desde casa sin miedo a fallar la talla. Entrega en 24 horas en toda La Paz.")

    st.info("ℹ️ **Nota para el Tribunal:** Para probar el sistema, diríjase a 'Digital Locker' e ingrese el ID **1004** (Relator) o **1002** (Panelista).")

# === DIGITAL LOCKER ===
elif menu == "🔐 DIGITAL LOCKER":
    st.title("🔐 Acceso a Perfil Biométrico")
    st.markdown("Simulación de base de datos de clientes con moldería digital.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### Identificación")
        input_id = st.text_input("Ingrese ID de Cliente:", placeholder="Ej: 1004")
        if st.button("🔍 CONSULTAR BASE DE DATOS"):
            if input_id in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[input_id]
                st.toast("Identidad Verificada Correctamente", icon="✅")
            else:
                st.error("ID no encontrado. Intente con 1002 o 1004.")
    
    with c2:
        if st.session_state.usuario:
            u = st.session_state.usuario
            st.success(f"BIENVENIDO: {u['nombre']}")
            
            # Tarjeta de Datos Técnicos
            st.markdown(f"""
            <div style="background-color:white; padding:20px; border-radius:10px; border:1px solid #ddd; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color:#4B0082; margin-top:0;">📋 Ficha Técnica Personal</h3>
                <p><strong>Cargo:</strong> {u['rol']}</p>
                <hr>
                <div style="display:grid; grid-template-columns: 1fr 1fr;">
                    <div><span style="font-size:2rem;">📏 {u['cintura']}</span><br><small>CM CINTURA</small></div>
                    <div><span style="font-size:2rem;">👖 {u['largo']}</span><br><small>CM LARGO</small></div>
                </div>
                <br>
                <p><strong>✂️ Fit Preferido:</strong> {u['fit']}</p>
                <p style="color:green; font-weight:bold;">✅ Patrones listos para corte automático.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Esperando ingreso de credenciales...")

# === CATÁLOGO (EL REGLADO) ===
elif menu == "👖 CATÁLOGO":
    st.title("Colección 2026")
    
    if st.session_state.usuario:
        st.info(f"✅ Precios y Tallas ajustados para: **{st.session_state.usuario['nombre']}**")
    else:
        st.warning("⚠️ MODO INVITADO: Se mostrarán precios estándar.")

    tab_std, tab_prem = st.tabs(["🔹 LÍNEA ESTÁNDAR (Diario)", "🔸 LÍNEA PREMIUM (Ejecutivo)"])
    
    # --- LÍNEA ESTÁNDAR ---
    with tab_std:
        col_a, col_b = st.columns(2)
        
        # Producto 1
        with col_a:
            st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=500&q=80", use_column_width=True)
            st.markdown("### Gabardina Spandex (Azul)")
            st.caption("97% Algodón / 3% Elastano | Forro Popelina 100%")
            st.markdown("<div class='price-tag'>240 Bs.</div>", unsafe_allow_html=True)
            if st.button("AGREGAR AL CARRITO", key="btn_std1"):
                st.session_state.carrito.append({"Item": "Gabardina Azul", "Precio": 240, "Linea": "Estándar"})
                st.toast("✅ Gabardina agregada")
        
        # Producto 2
        with col_b:
            st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=500&q=80", use_column_width=True)
            st.markdown("### Gabardina Spandex (Kaki)")
            st.caption("Dril Elastizado | Ideal oficina casual")
            st.markdown("<div class='price-tag'>240 Bs.</div>", unsafe_allow_html=True)
            if st.button("AGREGAR AL CARRITO", key="btn_std2"):
                st.session_state.carrito.append({"Item": "Gabardina Kaki", "Precio": 240, "Linea": "Estándar"})
                st.toast("✅ Gabardina agregada")

    # --- LÍNEA PREMIUM ---
    with tab_prem:
        col_c, col_d = st.columns(2)
        
        # Producto 3
        with col_c:
            st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=500&q=80", use_column_width=True)
            st.markdown("### Lana Fría (Super 100's)")
            st.caption("100% Lana Importada | Termicidad Regulada")
            st.markdown("<div class='price-tag'>450 Bs.</div>", unsafe_allow_html=True)
            if st.button("AGREGAR AL CARRITO", key="btn_prm1"):
                st.session_state.carrito.append({"Item": "Lana Fría Gris", "Precio": 450, "Linea": "Premium"})
                st.toast("✅ Lana Fría agregada")
        
        # Producto 4
        with col_d:
            st.image("https://images.unsplash.com/photo-1507680434567-5739c8fbe69d?auto=format&fit=crop&w=500&q=80", use_column_width=True)
            st.markdown("### Casimir Importado")
            st.caption("Acabado de lujo | Forrería reforzada")
            st.markdown("<div class='price-tag'>480 Bs.</div>", unsafe_allow_html=True)
            if st.button("AGREGAR AL CARRITO", key="btn_prm2"):
                st.session_state.carrito.append({"Item": "Casimir Importado", "Precio": 480, "Linea": "Premium"})
                st.toast("✅ Casimir agregado")

# === CHECKOUT ===
elif menu == "🛒 MI PEDIDO":
    st.title("Finalizar Compra")
    
    if len(st.session_state.carrito) > 0:
        # Tabla resumen
        df = pd.DataFrame(st.session_state.carrito)
        st.table(df)
        
        total = df['Precio'].sum()
        st.markdown(f"## TOTAL A PAGAR: **{total} Bs.**")
        
        st.divider()
        st.subheader("Datos de Entrega")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona de Envío", ["Sopocachi (Tienda)", "Zona Sur", "Centro", "Miraflores", "El Alto"])
            st.text_input("Dirección Exacta")
        with c2:
            st.radio("Método de Pago", ["QR Simple", "Transferencia", "Efectivo"])
            st.text_input("WhatsApp de Contacto")
            
        if st.button("CONFIRMAR PEDIDO"):
            with st.spinner("Conectando con Digital Locker..."):
                time.sleep(1.5)
            st.balloons()
            st.success("¡PEDIDO CONFIRMADO!")
            st.markdown("""
            > **El sistema ha generado la orden de corte.**
            > Gracias por confiar en la industria nacional.
            """)
            st.session_state.carrito = []
    else:
        st.info("Tu carrito está vacío. Ve al catálogo para añadir productos.")
