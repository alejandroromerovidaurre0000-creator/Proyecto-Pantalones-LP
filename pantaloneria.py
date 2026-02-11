import streamlit as st
import pandas as pd
import time
import random

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(
    page_title="Pantalonería Integral | Configura tu Estilo",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS "APPLE STYLE" (Minimalista y Moderno) ---
st.markdown("""
    <style>
    /* Global */
    .stApp { background-color: #ffffff; color: #1d1d1f; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 600; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #fbfbfd; border-right: 1px solid #d2d2d7; }
    
    /* Tarjetas de Producto */
    .product-container {
        border: 1px solid #e5e5e5;
        border-radius: 18px;
        padding: 25px;
        transition: all 0.3s ease;
        background: white;
    }
    .product-container:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transform: translateY(-5px);
    }
    
    /* Precios y Botones */
    .price-display {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0071e3; /* Azul Apple */
    }
    .stButton>button {
        background-color: #1d1d1f;
        color: white;
        border-radius: 980px; /* Redondo completo */
        padding: 10px 20px;
        font-weight: 500;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0071e3;
        transform: scale(1.02);
    }
    
    /* Etiquetas */
    .badge {
        background-color: #f5f5f7;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #86868b;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS (DIGITAL LOCKER) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'fit': 'Slim'},
        '1002': {'nombre': 'Samael Gómez Rúa', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'fit': 'Regular'},
        '1004': {'nombre': 'Miguel Vidal', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'fit': 'Tailored'},
        '1003': {'nombre': 'Jessica Daza Morales', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed'}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. BARRA LATERAL (CRÉDITOS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800201.png", width=50)
    st.markdown("### PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    st.divider()
    
    st.markdown("**Equipo Académico:**")
    st.markdown("🎓 **Tutora:** Jessica Susana Daza Morales")
    st.markdown("⚖️ **Panelista:** Samael Gómez Rúa")
    st.markdown("📝 **Relator:** Miguel Vidal")
    
    st.divider()
    menu = st.radio("MENÚ", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "🛠️ PERSONALIZADOR", "🛒 MI PEDIDO"])

# --- 5. LÓGICA PRINCIPAL ---

# === INICIO ===
if menu == "🏠 INICIO":
    st.title("PANTALONERÍA INTEGRAL")
    st.markdown("#### *La evolución del pantalón masculino: Phygital & Custom Made.*")
    
    st.image("https://images.unsplash.com/photo-1593030761757-71bd90dbe3e4?q=80&w=1200&auto=format&fit=crop", use_column_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ❌ El Problema
        * "No encuentro mi talla exacta."
        * "La tela pica o es poliéster barato."
        * "Tengo que ir al sastre y esperar semanas."
        """)
    with col2:
        st.markdown("""
        ### ✅ Nuestra Solución
        * **Moldería Digital:** Tu talla única guardada en la nube.
        * **Personalización:** Tú eliges la tela (Gabardina, Lana, Lino).
        * **Semi-Formal & Casual:** Ropa real para el día a día.
        """)

# === DIGITAL LOCKER ===
elif menu == "🔐 DIGITAL LOCKER":
    st.title("🔐 Digital Locker")
    st.write("Identificación biométrica para carga de medidas.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        id_user = st.text_input("ID Cliente:", placeholder="Ej: 1004 (Relator)")
        if st.button("Acceder"):
            if id_user in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[id_user]
                st.toast("Usuario Identificado")
            else:
                st.error("Usuario no encontrado.")

    with c2:
        if st.session_state.usuario:
            u = st.session_state.usuario
            st.markdown(f"""
            <div class="product-container">
                <h3 style="color:#0071e3">{u['nombre']}</h3>
                <p style="color:#86868b">{u['rol']}</p>
                <hr>
                <div style="display:flex; justify-content:space-between; text-align:center;">
                    <div><h1>{u['cintura']}</h1><small>CINTURA</small></div>
                    <div><h1>{u['largo']}</h1><small>LARGO</small></div>
                    <div><h1>{u['fit']}</h1><small>FIT PREFERIDO</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# === PERSONALIZADOR (NUEVO) ===
elif menu == "🛠️ PERSONALIZADOR":
    st.title("Estudio de Diseño")
    st.markdown("Elige el modelo base y personaliza la tela y el color.")
    
    if st.session_state.usuario:
        st.info(f"✅ Ajustando patrones para: **{st.session_state.usuario['nombre']}**")

    tabs = st.tabs(["SEMI-FORMAL (Oficina)", "CASUAL (Fin de Semana)"])

    # --- TAB 1: SEMI FORMAL ---
    with tabs[0]:
        c1, c2 = st.columns(2)
        
        # MODELO: EL CHINO CLÁSICO
        with c1:
            st.markdown('<div class="product-container">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=500&q=80")
            st.subheader("Modelo: THE CHINO")
            st.caption("Corte recto, bolsillos sesgados. El rey de la oficina moderna.")
            
            # SELECTOR DE TELA
            tela_chino = st.selectbox("Selecciona tu Tela:", 
                ["Gabardina Spandex (Estándar)", "Dril Pesado (Invierno)", "Lana Fría (Premium)"], key="s1")
            
            # Lógica de Precios
            precio_chino = 240
            if "Lana" in tela_chino: precio_chino = 450
            elif "Dril" in tela_chino: precio_chino = 260
            
            st.markdown(f"<div class='price-display'>{precio_chino} Bs.</div>", unsafe_allow_html=True)
            
            color_chino = st.radio("Color:", ["Azul Navy", "Kaki", "Verde Oliva"], horizontal=True, key="c1")
            
            if st.button("Añadir a Pedido", key="b1"):
                st.session_state.carrito.append({"Modelo": "Chino", "Tela": tela_chino, "Color": color_chino, "Precio": precio_chino})
                st.toast("Agregado!")
            st.markdown('</div>', unsafe_allow_html=True)

        # MODELO: EL GURKHA (Pretina Alta)
        with c2:
            st.markdown('<div class="product-container">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=500&q=80")
            st.subheader("Modelo: GURKHA SARTORIAL")
            st.caption("Pretina alta, ajustadores laterales, doble pinza. Elegancia pura.")
            
            tela_gurkha = st.selectbox("Selecciona tu Tela:", 
                ["Lana Super 100's", "Lino Italiano (Verano)", "Gabardina Premium"], key="s2")
            
            precio_gurkha = 480
            if "Gabardina" in tela_gurkha: precio_gurkha = 350
            
            st.markdown(f"<div class='price-display'>{precio_gurkha} Bs.</div>", unsafe_allow_html=True)
            
            color_gurkha = st.radio("Color:", ["Gris Oxford", "Arena", "Negro"], horizontal=True, key="c2")
            
            if st.button("Añadir a Pedido", key="b2"):
                st.session_state.carrito.append({"Modelo": "Gurkha", "Tela": tela_gurkha, "Color": color_gurkha, "Precio": precio_gurkha})
                st.toast("Agregado!")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: CASUAL ---
    with tabs[1]:
        c3, c4 = st.columns(2)
        
        # MODELO: 5-POCKETS (Tipo Jean)
        with c3:
            st.markdown('<div class="product-container">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=500&q=80")
            st.subheader("Modelo: 5-POCKETS")
            st.caption("Corte de Jean pero en telas más cómodas.")
            
            tela_5p = st.selectbox("Selecciona tu Tela:", 
                ["Dril Confort (con Elastano)", "Pana (Corduroy)", "Denim Selvedge"], key="s3")
            
            precio_5p = 200
            if "Pana" in tela_5p: precio_5p = 240
            if "Denim" in tela_5p: precio_5p = 280
            
            st.markdown(f"<div class='price-display'>{precio_5p} Bs.</div>", unsafe_allow_html=True)
            
            color_5p = st.radio("Color:", ["Camel", "Vino", "Azul Acero"], horizontal=True, key="c3")
            
            if st.button("Añadir a Pedido", key="b3"):
                st.session_state.carrito.append({"Modelo": "5-Pockets", "Tela": tela_5p, "Color": color_5p, "Precio": precio_5p})
                st.toast("Agregado!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # MODELO: CARGO CITY
        with c4:
            st.markdown('<div class="product-container">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1517445312882-1dd682bc8d96?q=80&w=500&auto=format&fit=crop") # Imagen genérica de pantalón
            st.subheader("Modelo: CARGO CITY")
            st.caption("Bolsillos laterales funcionales pero con silueta slim.")
            
            tela_cargo = st.selectbox("Selecciona tu Tela:", 
                ["Ripstop (Antidesgarro)", "Gabardina Lavada"], key="s4")
            
            precio_cargo = 220
            
            st.markdown(f"<div class='price-display'>{precio_cargo} Bs.</div>", unsafe_allow_html=True)
            
            color_cargo = st.radio("Color:", ["Verde Militar", "Negro", "Gris Humo"], horizontal=True, key="c4")
            
            if st.button("Añadir a Pedido", key="b4"):
                st.session_state.carrito.append({"Modelo": "Cargo", "Tela": tela_cargo, "Color": color_cargo, "Precio": precio_cargo})
                st.toast("Agregado!")
            st.markdown('</div>', unsafe_allow_html=True)

# === CHECKOUT ===
elif menu == "🛒 MI PEDIDO":
    st.title("Finalizar Compra")
    
    if len(st.session_state.carrito) > 0:
        st.write("Resumen de tus pantalones personalizados:")
        
        # Mostrar carrito como tabla limpia
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True)
        
        total = df['Precio'].sum()
        st.markdown(f"<div style='text-align:right; font-size:2rem; font-weight:bold;'>TOTAL: {total} Bs.</div>", unsafe_allow_html=True)
        
        st.divider()
        col_pay, col_info = st.columns(2)
        
        with col_pay:
            st.subheader("Pago y Entrega")
            zona = st.selectbox("Zona de Entrega", ["Sopocachi", "Sur", "Centro", "El Alto"])
            metodo = st.radio("Método de Pago", ["QR", "Transferencia", "Contra-entrega"])
            
        with col_info:
            if st.button("CONFIRMAR ORDEN DE CORTE"):
                with st.spinner("Enviando especificaciones a taller..."):
                    time.sleep(2)
                st.balloons()
                st.success("¡ORDEN ENVIADA!")
                st.markdown(f"""
                **Detalle para Taller:**
                * Cliente: {st.session_state.usuario['nombre'] if st.session_state.usuario else 'Invitado'}
                * Cantidad: {len(st.session_state.carrito)} unidades
                * Prioridad: Alta
                """)
                st.session_state.carrito = []
    else:
        st.info("Tu carrito está vacío. Ve al 'Personalizador' para diseñar tu pantalón.")
