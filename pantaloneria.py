import streamlit as st
import pandas as pd
import time
import random

# --- 1. CONFIGURACIÓN VISUAL (MODO DISEÑO) ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS AVANZADO (DISEÑO LIMPIO Y MINIMALISTA) ---
st.markdown("""
    <style>
    /* Tipografía y Fondo */
    .stApp { background-color: #FAFAFA; color: #333; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 300; }
    
    /* Header Personalizado */
    .brand-header {
        text-align: center;
        padding: 40px;
        background-color: #111;
        color: white;
        margin-bottom: 20px;
        border-radius: 0 0 15px 15px;
    }
    
    /* Tarjetas del Configurador */
    .config-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    
    /* Precios */
    .price-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4B0082;
        text-align: right;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1a1a1a; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #ccc; }
    
    /* Botones */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        font-weight: 600;
        background-color: #4B0082;
        border: none;
        padding: 12px;
    }
    .stButton>button:hover { background-color: #30005a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS (JURADO) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {'nombre': 'Alejandro Romero', 'rol': 'Postulante', 'cintura': 82, 'largo': 104, 'fit': 'Slim', 'historial': 2},
        '1002': {'nombre': 'Samael Gómez Rúa', 'rol': 'Panelista', 'cintura': 94, 'largo': 100, 'fit': 'Regular', 'historial': 0},
        '1003': {'nombre': 'Jessica Susana Daza', 'rol': 'Tutora', 'cintura': 70, 'largo': 95, 'fit': 'Relaxed', 'historial': 5},
        '1004': {'nombre': 'Miguel Vidal Sejas', 'rol': 'Relator', 'cintura': 88, 'largo': 102, 'fit': 'Tailored', 'historial': 1}
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. BARRA LATERAL (CRÉDITOS) ---
with st.sidebar:
    # Logo conceptual (Icono)
    st.markdown("<h1 style='text-align: center;'>🧵</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>PANTALONERÍA<br>INTEGRAL</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    
    st.info("**Postulante:** Alejandro Romero Vidaurre")
    
    with st.expander("🎓 TRIBUNAL EVALUADOR", expanded=True):
        st.write("**Tutora:** Jessica Susana Daza Morales")
        st.write("**Panelista:** Samael Gómez Rúa")
        st.write("**Relator:** Miguel Vidal Sejas")
    
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN", ["🏠 INICIO", "🔐 DIGITAL LOCKER", "🛠️ PERSONALIZADOR", "🛒 CARRITO"])

# --- 5. LÓGICA DEL SISTEMA ---

# === INICIO ===
if menu == "🏠 INICIO":
    # Header Branding
    st.markdown("""
    <div class="brand-header">
        <h1>Sastrería Phygital</h1>
        <p>Precisión Digital. Confección Artesanal. Solo Pantalones.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Image (Sastrería/Telas, NO trajes)
    st.image("https://images.unsplash.com/photo-1605518216938-7c31b7b14ad0?q=80&w=1200&auto=format&fit=crop", 
             caption="Taller en Sopocachi | Materiales Premium", use_column_width=True)
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1. Escaneo Único")
        st.caption("Visítanos una sola vez para digitalizar tus medidas.")
    with c2:
        st.markdown("### 2. Configura tu Estilo")
        st.caption("Elige tela, color y fit desde tu celular.")
    with c3:
        st.markdown("### 3. Ajuste Garantizado")
        st.caption("Sin pruebas intermedias. Te queda o te queda.")
        
    st.info("ℹ️ **Para la Defensa:** Ingrese al 'Digital Locker' con el ID **1004** o **1002**.")

# === DIGITAL LOCKER ===
elif menu == "🔐 DIGITAL LOCKER":
    st.title("🔐 Acceso Biométrico")
    
    c_login, c_info = st.columns([1, 2])
    
    with c_login:
        st.markdown("### Identificación")
        id_user = st.text_input("Ingrese ID Cliente:", placeholder="Ej: 1004")
        if st.button("Buscar Expediente"):
            if id_user in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[id_user]
                st.toast("Usuario Identificado", icon="✅")
            else:
                st.error("ID no encontrado.")
    
    with c_info:
        if st.session_state.usuario:
            u = st.session_state.usuario
            st.markdown(f"""
            <div class="config-card">
                <h2 style="color:#4B0082; margin:0;">{u['nombre']}</h2>
                <p style="color:gray;">{u['rol']} | Perfil Verificado</p>
                <hr>
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><h1>{u['cintura']}</h1><small>CM CINTURA</small></div>
                    <div><h1>{u['largo']}</h1><small>CM LARGO</small></div>
                    <div><h1>{u['fit']}</h1><small>FIT ANATÓMICO</small></div>
                </div>
                <br>
                <div style="background-color:#e8f5e9; padding:10px; border-radius:5px; color:#2e7d32; font-size:0.8rem;">
                    ✅ <b>Patrón Digital Generado:</b> Listo para corte automático.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico simple de medidas
            st.markdown("### 📊 Análisis Morfológico")
            st.progress(u['cintura'], text="Proporción Cintura")
            st.progress(u['largo'], text="Proporción Altura")
        else:
            st.info("Esperando credenciales...")
            # Imagen de 'Escáner' o 'Huella'
            st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80", caption="Sistema de Seguridad de Datos")

# === PERSONALIZADOR (EL CORE DEL NEGOCIO) ===
elif menu == "🛠️ PERSONALIZADOR":
    st.title("Estudio de Diseño")
    st.markdown("Diseña tu pantalón único. El precio se ajusta según la calidad de la tela.")
    
    if st.session_state.usuario:
        st.success(f"Confeccionando a medida para: **{st.session_state.usuario['nombre']}**")
    
    # 1. ELIGIR MODELO BASE
    st.subheader("1. Selecciona el Modelo Base")
    
    # Usamos columnas para mostrar opciones visuales
    col_model1, col_model2, col_model3 = st.columns(3)
    
    modelo_seleccionado = st.radio("Modelo:", 
        ["Chino Clásico (Oficina)", "5-Pockets (Casual/Jean)", "Sartorial (Vestir/Lana)"], 
        horizontal=True, label_visibility="collapsed")

    # Mostrar imagen según selección
    img_url = ""
    desc_modelo = ""
    
    if "Chino" in modelo_seleccionado:
        # Foto de pantalones doblados o chinos, no traje
        img_url = "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=800&q=80"
        desc_modelo = "Bolsillos diagonales. El equilibrio perfecto entre formal y casual."
        base_price = 180
    elif "5-Pockets" in modelo_seleccionado:
        # Foto de texturas de jeans/pantalon
        img_url = "https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=800&q=80"
        desc_modelo = "Corte de jean, remaches reforzados. Para el fin de semana."
        base_price = 160
    else: # Sartorial
        # Foto de tela de vestir gris
        img_url = "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80"
        desc_modelo = "Corte limpio, sin costuras visibles. Elegancia pura."
        base_price = 250

    c_img, c_config = st.columns([1, 1])
    
    with c_img:
        st.image(img_url, use_column_width=True)
        st.caption(desc_modelo)
        st.info("💡 Todos nuestros pantalones incluyen **Forrería de Popelina 100% Algodón** (Tesis Pág. 115).")

    with c_config:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        
        # 2. SELECCIÓN DE TELA
        st.subheader("2. Personaliza la Tela")
        tela = st.selectbox("Material:", [
            "Gabardina Spandex (97% Alg / 3% Elast)", 
            "Dril Pesado (100% Algodón)", 
            "Lana Fría Super 100's (Premium)", 
            "Pana / Corduroy (Invierno)"
        ])
        
        # Lógica de Precios (Tesis)
        precio_tela = 0
        mensaje_tela = ""
        
        if "Gabardina" in tela:
            precio_tela = 60 # Costo añadido al base
            mensaje_tela = "Estándar: Ideal uso diario."
        elif "Lana" in tela:
            precio_tela = 200 # Premium
            mensaje_tela = "Premium: Termicidad regulada y caída perfecta."
        elif "Pana" in tela:
            precio_tela = 80
            mensaje_tela = "Textura clásica para invierno."
        else:
            precio_tela = 40
            mensaje_tela = "Resistente y fresco."

        st.caption(f"ℹ️ {mensaje_tela}")
        
        # 3. SELECCIÓN DE COLOR
        st.subheader("3. Elige el Color")
        color_opciones = []
        if "Lana" in tela:
            color_opciones = ["Gris Oxford", "Negro", "Azul Noche", "Carbón"]
        elif "Gabardina" in tela:
            color_opciones = ["Azul Marino", "Kaki / Beige", "Verde Oliva", "Negro"]
        else:
            color_opciones = ["Café", "Vino", "Azul", "Gris"]
            
        color = st.selectbox("Tono disponible:", color_opciones)
        
        # CÁLCULO FINAL
        precio_final = base_price + precio_tela
        
        st.divider()
        st.markdown(f"Total: <span class='price-display'>{precio_final} Bs.</span>", unsafe_allow_html=True)
        
        if st.button("AGREGAR AL PEDIDO"):
            item = {
                "Modelo": modelo_seleccionado,
                "Tela": tela,
                "Color": color,
                "Precio": precio_final
            }
            st.session_state.carrito.append(item)
            st.balloons()
            st.success("¡Pantalón Configurado con Éxito!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# === CARRITO ===
elif menu == "🛒 CARRITO":
    st.title("Finalizar Compra")
    
    if len(st.session_state.carrito) > 0:
        st.write("Resumen de tu colección personalizada:")
        
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True)
        
        total = df['Precio'].sum()
        st.markdown(f"<h1 style='text-align:right;'>Total: {total} Bs.</h1>", unsafe_allow_html=True)
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Entrega")
            st.selectbox("Zona La Paz", ["Sopocachi", "Zona Sur", "Centro", "Miraflores", "El Alto"])
            st.text_input("Dirección Exacta")
        with c2:
            st.subheader("Contacto")
            st.text_input("WhatsApp")
            st.radio("Pago", ["QR", "Efectivo"])
            
        if st.button("ENVIAR ORDEN A TALLER"):
            with st.spinner("Procesando medidas del Digital Locker..."):
                time.sleep(2)
            st.success("¡PEDIDO CONFIRMADO!")
            st.info("Tu orden de corte ha sido generada con tus medidas exactas.")
            st.session_state.carrito = []
    else:
        st.info("Tu carrito está vacío. Ve al 'Personalizador' para crear tu pantalón.")
