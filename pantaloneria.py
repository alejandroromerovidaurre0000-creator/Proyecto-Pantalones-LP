import streamlit as st
import pandas as pd
import time
import random
import plotly.graph_objects as go

# --- 1. CONFIGURACIÓN INICIAL & BRANDING ---
st.set_page_config(
    page_title="Pantalonería Integral | Proyecto de Grado",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de Colores (Basada en identidad visual elegante/tecnológica)
COLOR_PRIMARIO = "#2C3E50" # Azul Oscuro Ejecutivo
COLOR_ACENTO = "#8E44AD"   # Morado (Innovación/Digital)
COLOR_FONDO = "#F4F6F7"

# --- 2. CSS AVANZADO (ESTILO APP NATIVA) ---
st.markdown(f"""
    <style>
    /* Estilos Globales */
    .stApp {{ background-color: {COLOR_FONDO}; }}
    h1, h2, h3 {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    
    /* Header Personalizado */
    .header-container {{
        background: linear-gradient(90deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%);
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* Tarjetas de Producto */
    .product-card {{
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid #e0e0e0;
    }}
    .product-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }}
    
    /* Etiquetas Técnicas */
    .tech-badge {{
        background-color: #E8F8F5;
        color: #117864;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #A2D9CE;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #1B2631;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: #BDC3C7;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS DE USUARIOS (JURADO) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = {
        '1001': {
            'nombre': 'Alejandro Romero', 
            'rol': 'Postulante', 
            'cintura': 82, 'largo': 104, 'tiro': 'Regular', 'fit': 'Slim Fit',
            'historial': 2
        },
        '1002': {
            'nombre': 'Lic. Samael Gómez Rúa', 
            'rol': 'Panelista', 
            'cintura': 94, 'largo': 100, 'tiro': 'Corto', 'fit': 'Regular Comfort',
            'historial': 0
        },
        '1003': {
            'nombre': 'Lic. Jessica Susana Daza', 
            'rol': 'Tutora', 
            'cintura': 70, 'largo': 95, 'tiro': 'Alto', 'fit': 'Relaxed',
            'historial': 5
        },
        '1004': {
            'nombre': 'Lic. Miguel Vidal Sejas', 
            'rol': 'Relator', 
            'cintura': 88, 'largo': 102, 'tiro': 'Regular', 'fit': 'Tailored Fit',
            'historial': 1
        }
    }

if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'usuario' not in st.session_state:
    st.session_state.usuario = None

# --- 4. BARRA LATERAL (CRÉDITOS ACADÉMICOS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9379/9379293.png", width=80) # Icono genérico de pantalón elegante
    st.markdown("## PROYECTO DE GRADO")
    st.caption("Ingeniería Comercial - UCB 2026")
    st.markdown("---")
    
    st.markdown("### 🎓 Tribunal Evaluador")
    st.markdown("**Tutora:** Jessica Susana Daza Morales")
    st.markdown("**Panelista:** Samael Gómez Rúa")
    st.markdown("**Relator:** Miguel Vidal Sejas")
    
    st.markdown("---")
    st.markdown("**Postulante:**")
    st.markdown("Alejandro M. Romero Vidaurre")
    
    st.markdown("---")
    menu = st.radio("NAVEGACIÓN:", ["🏠 INICIO / CONCEPTO", "🔐 DIGITAL LOCKER", "🧵 ATELIER (Catálogo)", "🛒 MI PEDIDO"])

# --- 5. LÓGICA DE PÁGINAS ---

# === PÁGINA 1: INICIO ===
if menu == "🏠 INICIO / CONCEPTO":
    # Header Visual
    st.markdown(f"""
    <div class="header-container">
        <h1>PANTALONERÍA INTEGRAL MASCULINA</h1>
        <p style="font-size: 1.2rem;">La primera experiencia <i>Phygital</i> de sastrería en La Paz.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80", 
                 caption="Taller & Showroom en Sopocachi", use_column_width=True)
    
    with col2:
        st.markdown("### 🚀 El Problema")
        st.markdown("""
        * **Incomodidad:** Las tallas S-M-L no existen en la vida real.
        * **Calidad Oculta:** Pantalones caros con forros de poliéster que hacen transpirar.
        * **Tiempo:** Ir al sastre tradicional toma 3 pruebas y 2 semanas.
        """)
        
        st.markdown("### ✅ Nuestra Solución (Tesis)")
        st.info("**1. Escaneo 3D:** Una sola visita para digitalizar medidas.")
        st.info("**2. Materiales Certificados:** (Ver Pág. 115) Gabardina con Elastano y Forrería 100% Algodón.")
        st.info("**3. Recompra Online:** Pide desde tu celular sin volverte a probar.")

    st.divider()
    st.warning("🔒 **DEMO PARA DEFENSA:** Ingrese al 'Digital Locker' con el ID **1004** (Relator) o **1002** (Panelista).")

# === PÁGINA 2: DIGITAL LOCKER ===
elif menu == "🔐 DIGITAL LOCKER":
    st.title("🔐 Digital Locker | Perfil Biométrico")
    
    col_login, col_dash = st.columns([1, 3])
    
    with col_login:
        st.markdown("### Identificación")
        st.markdown("Ingrese su ID único de cliente:")
        id_input = st.text_input("ID Cliente", placeholder="Ej: 1004")
        
        if st.button("Acceder al Sistema"):
            if id_input in st.session_state.db_clientes:
                st.session_state.usuario = st.session_state.db_clientes[id_input]
                st.toast("Identidad Verificada", icon="✅")
            else:
                st.error("ID no encontrado.")
                
    with col_dash:
        if st.session_state.usuario:
            user = st.session_state.usuario
            
            # Tarjeta de Bienvenida
            st.markdown(f"""
            <div style="background-color:white; padding:20px; border-radius:10px; border-left:5px solid {COLOR_ACENTO}; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="margin:0; color:{COLOR_PRIMARIO};">Bienvenido, {user['nombre']}</h2>
                <p style="color:gray;">Cargo: {user['rol']} | Estado: <b>Medidas Verificadas</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("") # Espacio
            
            # Tabs para información detallada
            tab1, tab2, tab3 = st.tabs(["📐 MIS MEDIDAS", "📊 ANÁLISIS DE FIT", "🛍️ HISTORIAL"])
            
            with tab1:
                c1, c2, c3 = st.columns(3)
                c1.metric("Cintura", f"{user['cintura']} cm", "Exacto")
                c2.metric("Largo Pierna", f"{user['largo']} cm", "Sin basta")
                c3.metric("Tiro", user['tiro'], "Confort")
                
                st.info(f"💡 **Preferencia de Corte:** {user['fit']}. Tus patrones están listos para corte automático.")

            with tab2:
                # Gráfico Radar Simulado con Plotly
                categories = ['Cintura', 'Cadera', 'Muslo', 'Largo', 'Tiro']
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                      r=[4, 3, 5, 4, 3],
                      theta=categories,
                      fill='toself',
                      name='Ajuste Personal'
                ))
                fig.update_layout(
                  polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                  showlegend=False,
                  height=300,
                  margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Gráfico de morfología vs. Patrón Base")

            with tab3:
                if user['historial'] > 0:
                    st.success(f"Tienes {user['historial']} compras anteriores satisfactorias.")
                    st.text("• 15/01/2025 - Gabardina Azul (Entregado)")
                else:
                    st.warning("Aún no tienes pedidos. ¡Estrena tu primer pantalón hoy!")

        else:
            # Estado vacío (Placeholder)
            st.info("👈 Por favor, ingrese un ID para cargar la simulación.")
            st.image("https://cdn.dribbble.com/users/2063388/screenshots/15647700/media/1a90c675371c89073145d475ce9953db.png?compress=1&resize=800x600", width=400)

# === PÁGINA 3: ATELIER (CATÁLOGO TÉCNICO) ===
elif menu == "🧵 ATELIER (Catálogo)":
    st.title("Colección 2026 | Selección de Materiales")
    
    if st.session_state.usuario:
        st.success(f"Confeccionando a medida para: **{st.session_state.usuario['nombre']}**")
    
    st.markdown("""
    > **Nota Técnica (Pág. 115):** Todos nuestros pantalones incluyen forrería de **Popelina 100% Algodón** > para garantizar frescura y evitar las roturas comunes de los forros sintéticos.
    """)
    
    # SEPARACIÓN POR LÍNEAS DE PRODUCTO
    tab_std, tab_prem = st.tabs(["🔹 LÍNEA ESTÁNDAR (Uso Diario)", "🔸 LÍNEA PREMIUM (Ejecutivo)"])
    
    # --- LÍNEA ESTÁNDAR ---
    with tab_std:
        st.markdown("#### Gabardina Spandex (Dril Elastizado)")
        col_a, col_b = st.columns(2)
        
        # PRODUCTO 1: AZUL MARINO
        with col_a:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1473966968600-fa801b869a1a?auto=format&fit=crop&w=600&q=80", caption="El Básico Imprescindible")
            st.markdown("### Gabardina Navy Blue")
            st.markdown("**Composición:** 97% Algodón / 3% Elastano")
            st.markdown("**Uso:** Oficina diaria / Universidad")
            st.markdown("#### 240 Bs.")
            
            with st.expander("Ver Ficha Técnica"):
                st.write("- **Tejido:** Dril de alta densidad.")
                st.write("- **Elastano (3%):** Permite movilidad al sentarse.")
                st.write("- **Color:** Azul reactivo (no despinta).")
            
            if st.button("Añadir al Carrito", key="p1"):
                st.session_state.carrito.append({"Item": "Gabardina Navy", "Precio": 240, "Linea": "Estándar"})
                st.toast("Pantalón agregado!")
            st.markdown('</div>', unsafe_allow_html=True)

        # PRODUCTO 2: KAKI / BEIGE
        with col_b:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image("https://images.unsplash.com/photo-1542272617-0858607c2242?auto=format&fit=crop&w=600&q=80", caption="Casual Friday")
            st.markdown("### Gabardina Kaki Office")
            st.markdown("**Composición:** 97% Algodón / 3% Elastano")
            st.markdown("**Uso:** Viernes casual / Eventos de día")
            st.markdown("#### 240 Bs.")
            
            with st.expander("Ver Ficha Técnica"):
                st.write("- **Versatilidad:** Combina con camisa o polo.")
                st.write("- **Construcción:** Costuras reforzadas en entrepierna.")
                st.write("- **Fit Recomendado:** Slim.")
            
            if st.button("Añadir al Carrito", key="p2"):
                st.session_state.carrito.append({"Item": "Gabardina Kaki", "Precio": 240, "Linea": "Estándar"})
                st.toast("Pantalón agregado!")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- LÍNEA PREMIUM ---
    with tab_prem:
        st.markdown("#### Lana Super 100's (Sastrería Fina)")
        col_c, col_d = st.columns(2)
        
        # PRODUCTO 3: GRIS OXFORD
        with col_c:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            # Imagen específica de pantalón de lana gris
            st.image("https://images.pexels.com/photos/5325886/pexels-photo-5325886.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", caption="Elegancia sin Traje Completo")
            st.markdown("### Lana Fría Gris Oxford")
            st.markdown("**Composición:** 100% Lana (Super 100's)")
            st.markdown("**Uso:** Reuniones Ejecutivas / Formal")
            st.markdown("#### 450 Bs.")
            
            with st.expander("💎 ¿Por qué Super 100's?"):
                st.write("Es una lana más fina y ligera. Ideal para el clima de La Paz porque regula la temperatura (no acalora, pero abriga).")
                st.write("**Forrería:** Popelina 100% Algodón blanca.")
            
            if st.button("Añadir al Carrito", key="p3"):
                st.session_state.carrito.append({"Item": "Lana Super 100 Gris", "Precio": 450, "Linea": "Premium"})
                st.toast("Artículo Premium agregado!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # INFO EXTRA
        with col_d:
            st.info("ℹ️ **Diferenciador de Marca**")
            st.markdown("""
            A diferencia de la competencia que vende trajes completos de poliéster, nosotros nos especializamos 
            únicamente en el pantalón.
            
            Al eliminar el saco, podemos invertir en **mejores telas (Lana)** a un precio accesible.
            """)
            st.image("https://images.pexels.com/photos/3755706/pexels-photo-3755706.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Detalle de confección artesanal")

# === PÁGINA 4: CARRITO ===
elif menu == "🛒 MI PEDIDO":
    st.title("Resumen de Compra")
    
    if len(st.session_state.carrito) > 0:
        # Tabla limpia con Pandas
        df = pd.DataFrame(st.session_state.carrito)
        st.dataframe(df, use_container_width=True)
        
        total = df['Precio'].sum()
        st.markdown(f"<h2 style='text-align: right; color: {COLOR_ACENTO};'>Total: {total} Bs.</h2>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("📍 Datos de Entrega (La Paz)")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona de Cobertura", ["Sopocachi (Gratis)", "Zona Sur (Calacoto/Obrajes)", "Centro", "Miraflores", "El Alto (Ciudad Satélite)"])
            st.text_area("Dirección Exacta", placeholder="Calle, Número, Edificio...")
        
        with c2:
            st.radio("Método de Pago", ["QR Simple", "Transferencia Bancaria", "Efectivo contra-entrega"])
            celular = st.text_input("WhatsApp de Contacto")
            
        if st.button("CONFIRMAR ORDEN DE CORTE"):
            if not celular:
                st.error("Por favor ingrese su número de celular.")
            else:
                with st.spinner("Enviando especificaciones al taller..."):
                    time.sleep(2)
                st.balloons()
                st.success("¡PEDIDO CONFIRMADO!")
                
                cliente = st.session_state.usuario['nombre'] if st.session_state.usuario else "Invitado"
                
                st.markdown(f"""
                <div style="background-color:#D4EFDF; padding:20px; border-radius:10px; color:#145A32;">
                    <h3>✅ Orden Generada Exitosamente</h3>
                    <ul>
                        <li><b>Cliente:</b> {cliente}</li>
                        <li><b>Total:</b> {total} Bs.</li>
                        <li><b>Instrucción Taller:</b> Usar forrería Popelina 100% Algodón.</li>
                    </ul>
                    <p>Gracias por validar el modelo de negocio.</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.carrito = [] # Limpiar
    else:
        st.info("Tu carrito está vacío. Ve al 'Atelier' para seleccionar tus pantalones.")
