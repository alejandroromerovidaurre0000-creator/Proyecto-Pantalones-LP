import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time
import random
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA Y METADATA
# ==============================================================================
st.set_page_config(
    page_title="SISTEMA PHYGITAL | TESIS 2026",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definición de Constantes de Marca
BRAND_NAME = "PANTALONERÍA INTEGRAL"
BRAND_SLOGAN = "Ingeniería de Confort & Sastrería Digital"
COLOR_PRIMARY = "#17202A"    # Negro Mate (Elegancia)
COLOR_SECONDARY = "#5B2C6F"  # Morado (Tecnología/Tesis)
COLOR_ACCENT = "#D4AC0D"     # Dorado (Premium)
COLOR_BG = "#F2F3F4"         # Gris Suave

# ==============================================================================
# 2. ESTILOS CSS AVANZADOS (INTERFAZ PROFESIONAL)
# ==============================================================================
st.markdown(f"""
    <style>
    /* RESET Y FUENTES */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    .stApp {{
        background-color: {COLOR_BG};
        font-family: 'Montserrat', sans-serif;
    }}

    /* -----------------------------------------------------------
       LOGO CSS (NO IMAGEN - CÓDIGO PURO PARA QUE NO FALLE)
    ----------------------------------------------------------- */
    .brand-header {{
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #2C3E50 100%);
        padding: 40px 20px;
        text-align: center;
        border-bottom: 5px solid {COLOR_SECONDARY};
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 30px;
        border-radius: 0 0 20px 20px;
    }}
    
    .brand-logo-text {{
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        text-transform: uppercase;
        letter-spacing: 8px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .brand-subtitle {{
        font-family: 'Roboto Mono', monospace;
        color: #D7BDE2;
        font-size: 1.2rem;
        margin-top: 10px;
        letter-spacing: 2px;
    }}

    /* -----------------------------------------------------------
       TARJETAS Y CONTENEDORES
    ----------------------------------------------------------- */
    .feature-card {{
        background-color: white;
        border-radius: 10px;
        padding: 25px;
        border-left: 5px solid {COLOR_SECONDARY};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        height: 100%;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(91, 44, 111, 0.2);
    }}

    .tech-spec {{
        background-color: #EAEDED;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
        color: #333;
        border: 1px dashed #999;
    }}

    /* -----------------------------------------------------------
       ELEMENTOS DE UI
    ----------------------------------------------------------- */
    h1, h2, h3 {{ color: {COLOR_PRIMARY}; }}
    
    .price-tag {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {COLOR_SECONDARY};
    }}
    
    .status-badge {{
        background-color: #2ECC71;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }}

    /* Botones Personalizados */
    .stButton>button {{
        width: 100%;
        background-color: {COLOR_PRIMARY};
        color: white;
        border: none;
        padding: 15px;
        border-radius: 5px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_SECONDARY};
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }}

    /* Sidebar Branding */
    [data-testid="stSidebar"] {{
        background-color: #FBFCFC;
        border-right: 1px solid #E5E7E9;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. BASE DE DATOS Y LÓGICA DE NEGOCIO
# ==============================================================================

# DATOS DEL TRIBUNAL (Protocolo Académico Estricto)
# Sin "Lic.", solo cargos y nombres completos.
DB_CLIENTES = {
    '1001': {
        'nombre': 'Alejandro Romero',
        'cargo': 'Postulante',
        'medidas': {'Cintura': 82, 'Largo': 104, 'Cadera': 98, 'Muslo': 54, 'Tiro': 28},
        'fit_pref': 'Slim Fit',
        'fidelidad': 'Nivel 1'
    },
    '1002': {
        'nombre': 'Samael Gómez Rúa',
        'cargo': 'Panelista',
        'medidas': {'Cintura': 94, 'Largo': 100, 'Cadera': 105, 'Muslo': 60, 'Tiro': 26},
        'fit_pref': 'Regular Comfort',
        'fidelidad': 'VIP Académico'
    },
    '1003': {
        'nombre': 'Jessica Susana Daza Morales',
        'cargo': 'Tutora',
        'medidas': {'Cintura': 72, 'Largo': 96, 'Cadera': 90, 'Muslo': 50, 'Tiro': 30},
        'fit_pref': 'Relaxed Fit',
        'fidelidad': 'VIP Académico'
    },
    '1004': {
        'nombre': 'Miguel Vidal Sejas',
        'cargo': 'Relator',
        'medidas': {'Cintura': 88, 'Largo': 102, 'Cadera': 100, 'Muslo': 58, 'Tiro': 28},
        'fit_pref': 'Tailored Fit',
        'fidelidad': 'VIP Académico'
    }
}

# CATALOGO DE MATERIALES (TEXTURAS - NO TRAJES)
# Usamos imágenes de TELAS para evitar el error de mostrar trajes.
DB_MATERIALES = {
    "Gabardina Spandex": {
        "desc": "97% Algodón / 3% Elastano",
        "precio_add": 0,
        "img": "https://images.unsplash.com/photo-1596489352928-1b2c57705141?q=80&w=600&auto=format&fit=crop", # Textura Tela Beige/Azul
        "colores": ["Azul Marino", "Kaki Oficina", "Verde Militar", "Negro"]
    },
    "Dril 100% Algodón": {
        "desc": "Tejido plano resistente, sin elasticidad",
        "precio_add": 20,
        "img": "https://images.unsplash.com/photo-1620799140408-ed5341cd2431?q=80&w=600&auto=format&fit=crop", # Textura Algodon
        "colores": ["Arena", "Café Tierra", "Gris Plomo"]
    },
    "Lana Fría Super 100's": {
        "desc": "Lana Importada (Termicidad Regulada)",
        "precio_add": 210, # Premium
        "img": "https://images.unsplash.com/photo-1605518216938-7c31b7b14ad0?q=80&w=600&auto=format&fit=crop", # Textura Gris Sastre
        "colores": ["Gris Oxford", "Negro Profundo", "Azul Noche"]
    },
    "Pana (Corduroy)": {
        "desc": "Tejido acanalado para invierno",
        "precio_add": 50,
        "img": "https://images.unsplash.com/photo-1517257982260-2646270b22a6?q=80&w=600&auto=format&fit=crop", # Textura
        "colores": ["Camel", "Vino", "Azul Marino"]
    }
}

# INICIALIZACIÓN DE ESTADO
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'usuario' not in st.session_state: st.session_state.usuario = None
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

# ==============================================================================
# 4. COMPONENTES DE LA INTERFAZ (FUNCIONES REUTILIZABLES)
# ==============================================================================

def mostrar_header():
    """Muestra el Logo CSS Gigante"""
    st.markdown(f"""
    <div class="brand-header">
        <h1 class="brand-logo-text">{BRAND_NAME}</h1>
        <p class="brand-subtitle">{BRAND_SLOGAN}</p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Barra lateral con protocolo académico"""
    with st.sidebar:
        st.markdown("### 🧭 PANEL DE CONTROL")
        
        opciones = [
            "1. INICIO & CONCEPTO",
            "2. DIGITAL LOCKER (Biometría)",
            "3. ATELIER (Configurador)",
            "4. CHECKOUT",
            "5. ADMIN PANEL (Simulación)"
        ]
        seleccion = st.radio("Navegación:", opciones, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### 🎓 PROYECTO DE GRADO")
        st.caption("Ingeniería Comercial - UCB 2026")
        
        with st.expander("⚖️ TRIBUNAL EVALUADOR", expanded=True):
            st.markdown("**Tutora:**")
            st.write("Jessica Susana Daza Morales")
            st.markdown("**Panelista:**")
            st.write("Samael Gómez Rúa")
            st.markdown("**Relator:**")
            st.write("Miguel Vidal Sejas")
        
        st.markdown("---")
        st.caption(f"Postulante: Alejandro M. Romero V.")
        
        return seleccion

# ==============================================================================
# 5. LÓGICA PRINCIPAL (CONTROL DE FLUJO)
# ==============================================================================

mostrar_header()
menu = mostrar_sidebar()

# ------------------------------------------------------------------------------
# MÓDULO 1: INICIO & CONCEPTO
# ------------------------------------------------------------------------------
if "1. INICIO" in menu:
    st.markdown("## 💡 LA PROPUESTA DE VALOR")
    
    col_intro1, col_intro2 = st.columns([1, 1])
    
    with col_intro1:
        st.markdown("""
        ### El Problema del Mercado
        La industria actual ofrece solo dos opciones extremas:
        1.  **Fast Fashion:** Tallas S/M/L que no ajustan bien y telas sintéticas.
        2.  **Sastrería Tradicional:** Procesos lentos (2-3 semanas), costosos y obligan a comprar el traje completo.
        
        ### Nuestra Solución (Tesis)
        Un modelo **Phygital** (Físico + Digital) especializado exclusivamente en pantalones.
        """)
        
        st.info("📌 **DATO CLAVE (Pág 115):** Todos nuestros productos usan forrería de **Popelina 100% Algodón** para evitar la transpiración y alergias que causa el poliéster.")

    with col_intro2:
        # Gráfico conceptual simple
        st.markdown("#### Matriz de Posicionamiento")
        chart_data = pd.DataFrame({
            'Precio': [80, 200, 450, 1500],
            'Personalización': [10, 30, 90, 100],
            'Tipo': ['Mercado Informal', 'Zara/H&M', 'PANTALONERÍA INTEGRAL', 'Sastre de Lujo']
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data['Precio'],
            y=chart_data['Personalización'],
            text=chart_data['Tipo'],
            mode='markers+text',
            textposition='top center',
            marker=dict(size=[20, 30, 50, 25], color=[1, 2, 3, 4])
        ))
        fig.update_layout(
            title="Calidad vs. Precio",
            xaxis_title="Precio (Bs)",
            yaxis_title="Nivel de Personalización (%)",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.warning("👉 **INSTRUCCIÓN:** Diríjase al módulo 'DIGITAL LOCKER' e ingrese el ID **1004** (Relator) para iniciar la demo.")

# ------------------------------------------------------------------------------
# MÓDULO 2: DIGITAL LOCKER (BIOMETRÍA)
# ------------------------------------------------------------------------------
elif "2. DIGITAL LOCKER" in menu:
    st.markdown("## 🔐 DIGITAL LOCKER | GESTIÓN BIOMÉTRICA")
    st.write("El corazón del sistema: Almacenamiento seguro de moldería digital.")
    
    col_auth, col_profile = st.columns([1, 2])
    
    with col_auth:
        st.markdown("### 🆔 Autenticación")
        id_input = st.text_input("Ingrese ID Cliente:", placeholder="Ej: 1004")
        
        if st.button("🔍 BUSCAR PERFIL"):
            user = DB_CLIENTES.get(id_input)
            if user:
                st.session_state.usuario = user
                st.success("¡Identidad Confirmada!")
                time.sleep(0.5)
            else:
                st.error("ID No Encontrado. Intente con: 1002, 1003 o 1004.")

    with col_profile:
        if st.session_state.usuario:
            u = st.session_state.usuario
            med = u['medidas']
            
            # Encabezado del Perfil
            st.markdown(f"""
            <div class="feature-card" style="border-left-color: {COLOR_ACCENT};">
                <h2 style="margin:0;">{u['nombre']}</h2>
                <p style="color:gray; font-family:'Roboto Mono'">CARGO: {u['cargo'].upper()} | FIDELIDAD: {u['fidelidad']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            # Visualización de Medidas (Radar Chart)
            # Este gráfico es muy "Ingeniero", se ve muy bien en defensa.
            col_graph, col_data = st.columns([1, 1])
            
            with col_graph:
                st.markdown("#### 📐 Morfología Corporal")
                
                categories = list(med.keys())
                values = list(med.values())
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=u['nombre'],
                    line_color=COLOR_SECONDARY
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
                    showlegend=False,
                    height=300,
                    margin=dict(l=30, r=30, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with col_data:
                st.markdown("#### 📋 Ficha Técnica")
                st.markdown(f"""
                <div class="tech-spec">
                    <b>CINTURA:</b> {med['Cintura']} cm<br>
                    <b>LARGO PIERNA:</b> {med['Largo']} cm<br>
                    <b>CADERA:</b> {med['Cadera']} cm<br>
                    <b>TIRO:</b> {med['Tiro']} cm<br>
                    <hr>
                    <b>FIT PREFERIDO:</b> {u['fit_pref']}
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Patrones DXF generados y listos para corte.")
                
        else:
            st.info("👋 Ingrese un ID en el panel izquierdo para cargar los datos del tribunal.")

# ------------------------------------------------------------------------------
# MÓDULO 3: ATELIER (CONFIGURADOR SIN TRAJES)
# ------------------------------------------------------------------------------
elif "3. ATELIER" in menu:
    st.markdown("## 🛠️ ATELIER DE DISEÑO")
    st.write("Configuración de producto basada en materiales. Precio dinámico.")

    if st.session_state.usuario:
        st.success(f"Diseñando para: **{st.session_state.usuario['nombre']}**")
    
    # PASO 1: MODELO
    st.markdown("### 1. SELECCIONA EL CORTE (MODELO)")
    c_mod1, c_mod2, c_mod3 = st.columns(3)
    
    modelo = st.radio("Modelo Base:", 
        ["Chino (Oficina/Diario)", "5-Pockets (Casual)", "Sartorial (Formal)"],
        horizontal=True, label_visibility="collapsed"
    )
    
    # Descripción dinámica del modelo
    desc_modelo = ""
    precio_base = 0
    if "Chino" in modelo:
        desc_modelo = "Bolsillos sesgados, corte limpio. El estándar para la oficina."
        precio_base = 180
    elif "5-Pockets" in modelo:
        desc_modelo = "Corte tipo Jean, bolsillos parche traseros. Informal."
        precio_base = 160
    elif "Sartorial" in modelo:
        desc_modelo = "Pantalón de vestir, pretina con botón oculto. (Solo pantalón, sin saco)."
        precio_base = 220

    st.info(f"ℹ️ **{modelo}:** {desc_modelo}")
    
    st.markdown("---")
    
    # PASO 2: MATERIAL (MOTOR VISUAL DE TELAS)
    st.markdown("### 2. SELECCIONA EL MATERIAL (TELA)")
    
    # Layout de columnas para telas
    cols_telas = st.columns(2)
    
    # Selector de Tela
    nombre_tela = st.selectbox("Catálogo de Telas:", list(DB_MATERIALES.keys()))
    
    # Recuperar datos de la tela seleccionada
    datos_tela = DB_MATERIALES[nombre_tela]
    
    col_vis, col_det = st.columns([1, 1])
    
    with col_vis:
        st.markdown("#### Textura del Material")
        # AQUI MOSTRAMOS SOLO LA TELA (TEXTURA), NO UN TRAJE
        st.image(datos_tela['img'], caption=f"Zoom: {nombre_tela}", use_column_width=True)
        st.caption("*Imagen referencial de la textura del tejido.")
    
    with col_det:
        st.markdown("#### Detalles Técnicos")
        st.markdown(f"**Composición:** {datos_tela['desc']}")
        st.markdown(f"**Costo Adicional:** +{datos_tela['precio_add']} Bs.")
        
        # PASO 3: COLOR
        st.markdown("#### 3. Color")
        color = st.radio("Tonos Disponibles:", datos_tela['colores'], horizontal=True)
        
        # CÁLCULO FINAL
        precio_final = precio_base + datos_tela['precio_add']
        
        st.markdown("---")
        st.markdown(f"### PRECIO FINAL: <span style='color:{COLOR_SECONDARY}'>{precio_final} Bs.</span>", unsafe_allow_html=True)
        
        if st.button("AÑADIR A ORDEN DE CORTE"):
            item = {
                "Modelo": modelo,
                "Tela": nombre_tela,
                "Color": color,
                "Precio": precio_final,
                "ID": random.randint(10000, 99999)
            }
            st.session_state.carrito.append(item)
            st.balloons()
            st.success("¡Item Agregado Correctamente!")

# ------------------------------------------------------------------------------
# MÓDULO 4: CHECKOUT (FACTURACIÓN)
# ------------------------------------------------------------------------------
elif "4. CHECKOUT" in menu:
    st.markdown("## 🛒 RESUMEN DE ORDEN")
    
    if len(st.session_state.carrito) > 0:
        # Convertir carrito a DataFrame para mostrar bonito
        df = pd.DataFrame(st.session_state.carrito)
        
        st.table(df[['Modelo', 'Tela', 'Color', 'Precio']])
        
        total = df['Precio'].sum()
        
        col_total, col_space = st.columns([2, 1])
        with col_total:
             st.markdown(f"<div class='price-tag'>TOTAL A PAGAR: {total} Bs.</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🚚 Datos de Despacho")
        
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Zona de Entrega", ["Sopocachi (Gratis)", "Zona Sur", "Centro", "Miraflores", "El Alto"])
            st.text_input("Dirección Exacta")
            st.text_input("NIT / Factura (Opcional)")
        
        with c2:
            st.text_input("WhatsApp de Contacto")
            st.radio("Método de Pago", ["Transferencia QR", "Efectivo Contra-entrega"])
            
            st.write("")
            if st.button("CONFIRMAR Y PROCESAR"):
                with st.spinner("Conectando con Digital Locker... Verificando Stock..."):
                    time.sleep(2)
                
                st.success("¡PEDIDO CONFIRMADO!")
                
                # Simulación de Recibo
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border: 1px dashed #333; font-family: 'Roboto Mono';">
                    <h3 style="text-align:center;">ORDEN DE CORTE #2026-{random.randint(100,999)}</h3>
                    <p><b>Cliente:</b> {st.session_state.usuario['nombre'] if st.session_state.usuario else 'Invitado'}</p>
                    <p><b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    <hr>
                    <p><b>Total:</b> {total} Bs.</p>
                    <p><b>Nota:</b> Incluye Forrería 100% Algodón.</p>
                    <div style="text-align:center; margin-top:20px;">
                        <span style="font-size:30px;">🏁</span><br>
                        GRACIAS POR SU PREFERENCIA
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.carrito = [] # Limpiar
                
    else:
        st.info("Tu carrito está vacío. Ve al ATELIER para configurar tus pantalones.")
        st.image("https://cdn-icons-png.flaticon.com/512/102/102661.png", width=100, style="opacity:0.5")

# ------------------------------------------------------------------------------
# MÓDULO 5: ADMIN PANEL (EXTRA PARA QUE SE VEA LARGO Y PRO)
# ------------------------------------------------------------------------------
elif "5. ADMIN PANEL" in menu:
    st.markdown("## ⚙️ PANEL DE ADMINISTRACIÓN (BACKEND)")
    st.warning("🔒 Área restringida para uso interno de la tienda.")
    
    password = st.text_input("Contraseña de Admin:", type="password")
    
    if password == "admin123":
        st.success("Acceso Concedido")
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Ventas del Mes", "12,450 Bs", "+15%")
        kpi2.metric("Pedidos Activos", "8", "-2")
        kpi3.metric("Tela en Stock", "450 Mts", "OK")
        
        st.subheader("Órdenes Recientes")
        datos_dummy = pd.DataFrame({
            'ID Orden': ['#2021', '#2022', '#2023'],
            'Cliente': ['Juan Pérez', 'Carlos Mamani', 'Ana López'],
            'Estado': ['En Corte', 'En Costura', 'Entregado'],
            'Monto': [240, 450, 200]
        })
        st.dataframe(datos_dummy, use_container_width=True)
        
        st.subheader("Inventario de Telas")
        chart_stock = pd.DataFrame({
            'Tela': ['Gabardina', 'Lana 100s', 'Dril', 'Popelina'],
            'Metros': [120, 40, 85, 200]
        })
        st.bar_chart(chart_stock.set_index('Tela'))
        
    elif password != "":
        st.error("Contraseña incorrecta.")

# ==============================================================================
# FOOTER (PIE DE PÁGINA)
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    &copy; 2026 PANTALONERÍA INTEGRAL. Todos los derechos reservados.<br>
    Proyecto de Grado | Universidad Católica Boliviana "San Pablo"
</div>
""", unsafe_allow_html=True)
