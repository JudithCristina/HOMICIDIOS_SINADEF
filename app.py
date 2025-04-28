import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import locale
import time

# Configurar idioma español para fechas
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')

st.set_page_config(page_title="Dashboard de Muertes Violentas", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# =====================
# ESTILO DIVULGA AZUL (SIDEBAR) + ACADÉMICO (MAIN)
# =====================
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #F0F2F5 !important;
        color: #003366 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .block-container {
        padding: 2rem 3rem 3rem;
    }
    h1, h2, h3, h4, h5 {
        font-weight: 700;
        margin-bottom: 10px;
        color: #003366 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .st-emotion-cache-ovf5rk{
        color: #003366 !important;
    }
    .st-eb{
        background-color:#003366!important
    }
    h1 { font-size: 30px !important; }
    h2 { font-size: 30px !important; }
    h3 { font-size: 20px !important; }
    h4, label { font-size: 18px !important; }
    p{
        font-size: 16px!important
        color: white !important
    }
    
    section[data-testid="stSidebar"] {
        background-color: #005EB8 !important;
        border-right: 2px solid #00AEEF;
        padding: 25px 20px 15px 20px;
        color: white !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: bold;
        font-size: 17px !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stSelectbox div, .stMultiSelect div, .stTextInput input {
        color: white !important;
        font-weight: 700 !important;
        font-size: 14px!important;
        font-family: 'Inter', sans-serif !important;
    }
    .stMultiSelect div[data-baseweb="tag"],
    span[data-baseweb="tag"],
    .st-bn {
        background-color: #F39200 !important;
        color: #003366 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        font-size: 15px !important;
        padding: 6px 14px !important;
        border: none !important;
    }
    .stMultiSelect [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #004B99 !important;
        border-color: #00AEEF !important;
    }
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {
        color: white !important;
        font-weight: bold;
        font-size: 15px !important;
    }
    .stRadio [role="radiogroup"] > div {
        background-color: #004B99 !important;
        border: 1px solid #00AEEF !important;
        border-radius: 6px;
        padding: 5px;
        margin-bottom: 8px;
    }
    .stRadio [role="radiogroup"] > div:hover {
        background-color: #0075c9 !important;
    }
    .stRadio [role="radiogroup"] > div[aria-checked="true"] {
        background-color: #00AEEF !important;
    }
    .stRadio [role="radiogroup"] > div[aria-checked="true"] p {
        color: white !important;
    }
    .stButton>button {
        color: white !important;
        background-color: #0079C1 !important;
        font-weight: bold;
        border-radius: 6px;
    }
    .stAppHeader {
        background: transparent;
    }
    .stDataFrame {
        background-color: #f5f5f5 !important;
        color: #003366 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .main-svg {
        background-color: transparent!important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
    .legend{
        background-color: transparent!important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
    .fecha-rango{
        font-size: 25px !important;
    }
    .total-muertes{
        font-size: 40px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# CARGA BASE
# =====================
mes_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
df_base = pd.read_csv("https://raw.githubusercontent.com/JudithCristina/sinadef-automatizado/main/data/processed/BASE_FINAL_GENERAL.csv")
df = pd.DataFrame()
df["sexo"] = df_base["SEXO"]
df["edad"] = df_base["EDADES"]
df["causa_muerte"] = df_base["Grupo_Causa"]
df["mes"] = df_base["MES"].map(mes_dict)
df["año"] = df_base["ANIO"]
df["fecha"] = df_base["FECHA"]
df["cantidad"] = 1
if "FECHA_DESCARGA" in df_base and "HORA_DESCARGA" in df_base:
    fecha_dt = pd.to_datetime(df_base["FECHA_DESCARGA"].iloc[0] + " " + df_base["HORA_DESCARGA"].iloc[0])
    fecha_actualizacion = fecha_dt.strftime("%d de %B de %Y a las %H:%M").capitalize()
else:
    fecha_actualizacion = ""
# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("## 🔎 Filtros del Dashboard")

    # 🎯 Filtros demográficos
    with st.expander("🎯 Filtros demográficos", expanded=True):
        sexo_sel = st.multiselect("Sexo:", df["sexo"].unique(), default=df["sexo"].unique())
        causa_sel = st.multiselect("Causa de muerte:", df["causa_muerte"].unique(), default=df["causa_muerte"].unique())
        edad_sel = st.multiselect("Etapas de vida:", df["edad"].unique(), default=df["edad"].unique())

    # 📆 Filtros temporales
    # 📆 Filtros temporales
    with st.expander("📆 Filtro temporal", expanded=True):
        tipo_filtro_tiempo = st.radio(
            "¿Cómo deseas filtrar el tiempo?",
            ["Por años", "Por rango reciente", "Por calendario"]
        )

        if tipo_filtro_tiempo == "Por años":
            año_inicio, año_fin = st.slider(
                "Año",
                min_value=int(df["año"].min()),
                max_value=int(df["año"].max()),
                value=(int(df["año"].min()), int(df["año"].max())),
                step=1
            )
            rango_reciente = None
            fecha_inicio = fecha_fin = None

        elif tipo_filtro_tiempo == "Por rango reciente":
            rango_reciente = st.selectbox(
                "Selecciona un rango reciente:",
                ["Última semana", "Último mes", "Últimos 3 meses", "Últimos 6 meses"]
            )
            año_inicio = año_fin = fecha_inicio = fecha_fin = None

        else:  # Por calendario
            col1, col2 = st.columns(2)
            hoy = pd.Timestamp.today().date()

            # Calcular lunes y domingo de la semana anterior
            lunes_actual = hoy - pd.Timedelta(days=hoy.weekday())  # lunes de esta semana
            fecha_inicio_default = lunes_actual - pd.Timedelta(days=7)  # lunes anterior
            fecha_fin_default = fecha_inicio_default + pd.Timedelta(days=6)  # domingo anterior
            with col1:
                fecha_inicio = st.date_input("Fecha de inicio", value=fecha_inicio_default, max_value=hoy)
            with col2:
                fecha_fin = st.date_input("Fecha de fin", value=fecha_fin_default,  max_value=hoy)

            año_inicio = año_fin = rango_reciente = None

# =====================
# APLICAR FILTRO TEMPORAL INTELIGENTE
# =====================
df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')
hoy = pd.Timestamp.today()
inicio, fin = None, None

# Guardar una copia del DataFrame original antes de aplicar filtros
df_original = df.copy()

if tipo_filtro_tiempo == "Por calendario":
    # Caso para filtro por calendario
    inicio = pd.to_datetime(fecha_inicio)
    fin = pd.to_datetime(fecha_fin)
    # Incluir todo el día final
    fin = fin + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    
    # Verificar si hay datos en el rango
    registros_rango = df[(df["fecha"] >= inicio) & (df["fecha"] <= fin)].shape[0]
    
    if registros_rango > 0:
        df = df[(df["fecha"] >= inicio) & (df["fecha"] <= fin)]
    else:
        # Mantener el DataFrame original para que los otros filtros puedan aplicarse
        df = df_original

elif rango_reciente:
    primer_dia_mes_actual = hoy.replace(day=1)

    if rango_reciente == "Última semana":
        # Semana epidemiológica pasada: lunes a domingo anterior
        lunes_actual = hoy - timedelta(days=hoy.weekday())
        inicio = lunes_actual - timedelta(days=7)
        fin = lunes_actual - timedelta(days=1)

    elif rango_reciente == "Último mes":
        fin = primer_dia_mes_actual - timedelta(days=1)
        inicio = fin.replace(day=1)

    elif rango_reciente == "Últimos 3 meses":
        fin = primer_dia_mes_actual - timedelta(days=1)
        inicio = (primer_dia_mes_actual - pd.DateOffset(months=3)).replace(day=1)

    elif rango_reciente == "Últimos 6 meses":
        fin = primer_dia_mes_actual - timedelta(days=1)
        inicio = (primer_dia_mes_actual - pd.DateOffset(months=6)).replace(day=1)

    df = df[(df["fecha"] >= inicio) & (df["fecha"] <= fin)]

else:  # Por años
    if año_inicio is not None and año_fin is not None:
        df = df[df["año"].between(año_inicio, año_fin)]
        inicio = df["fecha"].min()
        fin = df["fecha"].max()
    else:
        # Si año_inicio o año_fin son None, mantener todos los datos
        st.warning("⚠️ Por favor selecciona un rango de años válido.")
        df = df_original
# =====================
# FILTRADO
# =====================
if tipo_filtro_tiempo == "Por calendario":
    fecha_inicio_dt = pd.to_datetime(fecha_inicio)
    fecha_fin_dt = pd.to_datetime(fecha_fin)
    
    df_filtrado = df[
        (df["sexo"].isin(sexo_sel)) &
        (df["causa_muerte"].isin(causa_sel)) &
        (df["edad"].isin(edad_sel)) &
        (df["fecha"] >= fecha_inicio_dt) &
        (df["fecha"] <= fecha_fin_dt) 
    ]
else:
    df_filtrado = df[
        (df["sexo"].isin(sexo_sel)) &
        (df["causa_muerte"].isin(causa_sel)) &
        (df["edad"].isin(edad_sel))
    ]
total_muertes = df_filtrado["cantidad"].sum()

# Mostrar título adaptado según el tipo de filtro temporal
if tipo_filtro_tiempo == "Por calendario":
    if fecha_inicio == fecha_fin:
        titulo_rango = f"{fecha_inicio.strftime('%d/%m/%Y')}"
    elif fecha_inicio.year == fecha_fin.year:
        if fecha_inicio.month == fecha_fin.month:
            titulo_rango = f"{fecha_inicio.strftime('%d')} al {fecha_fin.strftime('%d de %B de %Y')}"
        else:
            titulo_rango = f"{fecha_inicio.strftime('%d de %B')} al {fecha_fin.strftime('%d de %B de %Y')}"
    else:
        titulo_rango = f"{fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}"
        
elif rango_reciente:
    if rango_reciente == "Última semana":
        titulo_rango = f"{inicio.strftime('%A %d de %B de %Y')} al {fin.strftime('%A %d de %B de %Y')}"
    elif inicio.year == fin.year:
        if inicio.month == fin.month:
            titulo_rango = f"{inicio.strftime('%B de %Y')}"
        else:
            titulo_rango = f"{inicio.strftime('%-d de %B')} al {fin.strftime('%-d de %B de %Y')}"
    else:
        titulo_rango = f"{inicio.strftime('%-d de %B de %Y')} al {fin.strftime('%-d de %B de %Y')}"
else:
    titulo_rango = f"{año_inicio} - {año_fin}"
    
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;
                background-color: #F39200; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <div>
            <h1  style=" margin: 0px; color: #003366; padding: 0px">Homicidios con necropsia registrados en SINADEF</h1>
            <p class="fecha-rango" style=" font-style: italic; margin: 0; color: #003366;">
                ({titulo_rango})
            </p>
        </div>
        <div style="text-align: right;">
            <p class="fecha-rango" style="color: white;  margin: 0;">Número de homicidios:</p>
            <p class="total-muertes" style="color: white; font-size: 40px; font-weight: bold; margin: 0;">{total_muertes:,}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================
# GRAFICOS
# =====================
col_causa, col_edad = st.columns(2)

with col_causa:
    if tipo_filtro_tiempo == "Por calendario":
        st.markdown("### Causas de muerte según periodo seleccionado")

        fecha_inicio_dt = pd.to_datetime(fecha_inicio)
        fecha_fin_dt = pd.to_datetime(fecha_fin)

        df_filtrado_calendario = df[
            (df["fecha"] >= fecha_inicio_dt) &
            (df["fecha"] <= fecha_fin_dt) &
            (df["sexo"].isin(sexo_sel)) &
            (df["causa_muerte"].isin(causa_sel)) &
            (df["edad"].isin(edad_sel))
        ].copy()

        if df_filtrado_calendario.empty:
            st.markdown("""
            <div style="background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)
        else:
            if fecha_inicio_dt.year != fecha_fin_dt.year:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.year.astype(str)
                orden_x = sorted(df_filtrado_calendario["tiempo"].unique())

            elif fecha_inicio_dt.month != fecha_fin_dt.month:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.strftime('%B %Y')
                orden_x = sorted(
                    df_filtrado_calendario["fecha"].dt.to_period("M").drop_duplicates().sort_values()
                    .dt.to_timestamp().dt.strftime('%B %Y').tolist(),
                    key=lambda x: datetime.strptime(x, '%B %Y')
                )

            else:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.strftime('%d/%m/%Y')
                orden_x = sorted(df_filtrado_calendario["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m/%Y'))

            causa_tiempo = df_filtrado_calendario.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

    elif rango_reciente == "Última semana":
        st.markdown("### Causas de muerte según día de ocurrencia")
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%A')
        orden_x = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        causa_tiempo = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

        causas_completas = causa_tiempo["causa_muerte"].unique()
        index_completo = pd.MultiIndex.from_product(
            [orden_x, causas_completas],
            names=["tiempo", "causa_muerte"]
        )
        causa_tiempo = (
            causa_tiempo
            .set_index(["tiempo", "causa_muerte"])
            .reindex(index_completo, fill_value=0)
            .reset_index()
        )

    elif rango_reciente == "Último mes":
        st.markdown("### Causas de muerte según día de ocurrencia")
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%d/%m')
        orden_x = sorted(df_filtrado["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m'))
        causa_tiempo = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

    elif rango_reciente in ["Últimos 3 meses", "Últimos 6 meses"]:
        st.markdown("### Causas de muerte según mes de ocurrencia")
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%B %Y')
        meses_orden = df_filtrado["fecha"].dt.to_period("M").sort_values().unique()
        orden_x = [d.strftime('%B %Y') for d in meses_orden.to_timestamp()]
        causa_tiempo = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

    else:
        st.markdown("### Causas de muerte según año de ocurrencia")
        df_filtrado["tiempo"] = df_filtrado["año"].astype(str)
        orden_x = sorted(df_filtrado["tiempo"].unique())
        causa_tiempo = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

    # Solo si hay datos
    if 'causa_tiempo' in locals() and not causa_tiempo.empty:
        # 👉 Ordenar causas y poner "arma de fuego" primero
        orden_causas = (
            causa_tiempo.groupby('causa_muerte')['cantidad']
            .sum()
            .sort_values()
            .index
            .tolist()
        )
        if "Arma de fuego" in orden_causas:
            orden_causas.remove("Arma de fuego")
        orden_causas = ["Arma de fuego"] + orden_causas

        # 👉 Aplicar orden categórico para apilar correctamente
        causa_tiempo["causa_muerte"] = pd.Categorical(
            causa_tiempo["causa_muerte"],
            categories=orden_causas,
            ordered=True
        )

        # 🎨 Paleta personalizada (respetando los colores del gráfico original)
        color_map = {
            "Arma blanca": "#90A4AE",
            "Arma de fuego": "#00AEEF", 
            "Asfixia": "#005EB8",
            "Otra causa": "#F39200"             
        }
        # 📊 Gráfico
        fig_causa = px.bar(
            causa_tiempo,
            x='tiempo',
            y='cantidad',
            color='causa_muerte',
            labels={
                'tiempo': 'Periodo',
                'cantidad': 'Número de Homicidios',
                'causa_muerte': 'Causa de muerte'
            },
            category_orders={
                'tiempo': orden_x,
                'causa_muerte': orden_causas
            },
            color_discrete_map=color_map,
            height=350
        )

        fig_causa.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(family='Inter, sans-serif', color='#003366'),
            margin=dict(t=30, r=10, b=50, l=50),
            xaxis=dict(
                title_font=dict(size=16, color='#003366'),
                tickfont=dict(size=12, color='#003366'),
                gridcolor='rgba(145, 191, 219, 0.3)',
                gridwidth=1,
                tickangle=-45,
                tickmode='linear'
            ),
            yaxis=dict(
                title_font=dict(size=16, color='#003366'),
                tickfont=dict(size=12, color='#003366'),
                gridcolor='rgba(145, 191, 219, 0.3)',
                gridwidth=1,
            ),
            legend=dict(
                title_font=dict(size=16, color='#003366'),
                font=dict(size=14, color='#003366'),
                bgcolor='#F0F2F5',
            )
        )

        st.plotly_chart(fig_causa, use_container_width=True)

    elif tipo_filtro_tiempo != "Por calendario":
        st.markdown("""
            <div style="background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)

# Agrupar y luego mapear los nombres amigables
edad_año = df_filtrado.groupby(['año', 'edad'])['cantidad'].sum().reset_index()

# Orden personalizado basado en los valores reales de EDADES
orden_personalizado = ['Niño', 'Adolescente', 'Joven', 'Adulto', 'Adulto mayor']

with col_edad:
    if tipo_filtro_tiempo == "Por calendario":
        st.markdown("### Homicidios por etapas de vida según periodo seleccionado")        

        fecha_inicio_dt = pd.to_datetime(fecha_inicio)
        fecha_fin_dt = pd.to_datetime(fecha_fin)

        df_filtrado_calendario = df[
            (df["fecha"] >= fecha_inicio_dt) &
            (df["fecha"] <= fecha_fin_dt) &
            (df["sexo"].isin(sexo_sel)) &
            (df["causa_muerte"].isin(causa_sel)) &
            (df["edad"].isin(edad_sel))
        ].copy()

        if df_filtrado_calendario.empty:
            st.markdown("""
            <div style="background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)
        else:
            if fecha_inicio_dt.year != fecha_fin_dt.year:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.year.astype(str)
                orden_x = sorted(df_filtrado_calendario["tiempo"].unique())
            elif fecha_inicio_dt.month != fecha_fin_dt.month:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.strftime('%B %Y')
                orden_x = sorted(
                    df_filtrado_calendario["fecha"].dt.to_period("M").drop_duplicates().sort_values()
                    .dt.to_timestamp().dt.strftime('%B %Y').tolist(),
                    key=lambda x: datetime.strptime(x, '%B %Y')
                )
            else:
                df_filtrado_calendario["tiempo"] = df_filtrado_calendario["fecha"].dt.strftime('%d/%m/%Y')
                orden_x = sorted(df_filtrado_calendario["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m/%Y'))

            edad_tiempo = df_filtrado_calendario.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()

            edades_presentes = df_filtrado_calendario["edad"].unique()
            index_completo = pd.MultiIndex.from_product(
                [orden_x, edades_presentes],
                names=["tiempo", "edad"]
            )

            edad_tiempo = (
                edad_tiempo
                .set_index(["tiempo", "edad"])
                .reindex(index_completo, fill_value=0)
                .reset_index()
            )
    elif rango_reciente == "Última semana":
        st.markdown("### Homicidios por etapas de vida según día")
        
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%A')
        orden_x = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        
        # 🔹 NUEVO: asegurar que todos los días y edades estén representados
        edad_tiempo = df_filtrado.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()
        
        edades_presentes = edad_tiempo["edad"].unique()
        index_completo = pd.MultiIndex.from_product(
            [orden_x, edades_presentes],
            names=["tiempo", "edad"]
        )
        
        edad_tiempo = (
            edad_tiempo
            .set_index(["tiempo", "edad"])
            .reindex(index_completo, fill_value=0)
            .reset_index()
        )
    
    elif rango_reciente == "Último mes":
        st.markdown("### Homicidios por etapas de vida según día")
        
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%d/%m')
        orden_x = sorted(df_filtrado["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m'))
        edad_tiempo = df_filtrado.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()
    
    elif rango_reciente in ["Últimos 3 meses", "Últimos 6 meses"]:
        st.markdown("### Homicidios por etapas de vida según mes")
        
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%B %Y')
        meses_orden = df_filtrado["fecha"].dt.to_period("M").sort_values().unique()
        orden_x = [d.strftime('%B %Y') for d in meses_orden.to_timestamp()]
        edad_tiempo = df_filtrado.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()
    
    else:
        st.markdown("### Homicidios por etapas de vida según año")
        
        df_filtrado["tiempo"] = df_filtrado["año"].astype(str)
        orden_x = sorted(df_filtrado["tiempo"].unique())
        edad_tiempo = df_filtrado.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()
    # Continúa con el código para crear y mostrar el gráfico, solo si edad_tiempo existe y tiene datos
    if 'edad_tiempo' in locals() and not edad_tiempo.empty:
        orden_edad = ['Niño', 'Adolescente', 'Joven', 'Adulto', 'Adulto mayor']

        fig_edad = px.bar(
            edad_tiempo,
            x='tiempo',
            y='cantidad',
            color='edad',
            labels={
                'tiempo': 'Periodo',
                'cantidad': 'Número de Homicidios',
                'edad': 'Etapas de vida'
            },
            category_orders={'tiempo': orden_x},
            color_discrete_map={
                'Niño': '#005EB8',
                'Adolescente': '#F39200',
                'Joven': '#90A4AE',
                'Adulto': '#00AEEF',
                'Adulto mayor': '#B2EBF2'
            },
            height=350
        )

        fig_edad.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(family='Inter, sans-serif', color='#003366'),
            margin=dict(t=30, r=10, b=50, l=50),
            xaxis=dict(
                title_font=dict(size=16, color='#003366'),
                tickfont=dict(size=12, color='#003366'),
                gridcolor='rgba(145, 191, 219, 0.3)',
                gridwidth=1,
                tickangle=-45,
                tickmode='linear'
            ),
            yaxis=dict(
                title_font=dict(size=16, color='#003366'),
                tickfont=dict(size=12, color='#003366'),
                gridcolor='rgba(145, 191, 219, 0.3)',
                gridwidth=1,
            ),
            legend=dict(
                title_font=dict(size=16, color='#003366'),
                font=dict(size=14, color='#003366'),
                bgcolor='#F0F2F5',
            )
        )
        st.plotly_chart(fig_edad, use_container_width=True)
    elif tipo_filtro_tiempo != "Por calendario":
        st.markdown("""
            <div style="background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)

col_linea, col_pie = st.columns([0.70, 0.30])

with col_linea:
    import locale
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    col_titulo, col_toggle = st.columns([0.65, 0.35])
    with col_titulo:
        titulo_linea = "Evolución diaria de homicidios"
        eje_x = 'tiempo'
        tickmode = None
        tickformat = '%d/%m/%Y'

        if tipo_filtro_tiempo == "Por calendario":
            fecha_inicio_dt = pd.to_datetime(fecha_inicio)
            fecha_fin_dt = pd.to_datetime(fecha_fin)
            if fecha_inicio_dt.year != fecha_fin_dt.year:
                df_filtrado["tiempo"] = df_filtrado["fecha"].dt.to_period("M").astype(str)
                titulo_linea = "Evolución mensual de homicidios"
                tickformat = '%m/%Y'
            else:
                df_filtrado["tiempo"] = pd.to_datetime(df_filtrado["fecha"])
                tickformat = '%d/%m/%Y'

        elif tipo_filtro_tiempo == "Por años":
            df_filtrado["tiempo"] = df_filtrado["fecha"].dt.to_period("M").astype(str)
            titulo_linea = "Evolución mensual de homicidios"
            tickformat = '%m/%Y'
        else:
            df_filtrado["tiempo"] = pd.to_datetime(df_filtrado["fecha"])
            if rango_reciente in ["Última semana", "Último mes"]:
                tickmode = 'linear'

        st.markdown(f"### {titulo_linea}")

    with col_toggle:
        st.markdown("""
        <style>
        div[data-testid=\"stToggle\"] label {
            background-color: #00AEEF !important;
            color: white !important;
            padding: 6px 16px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.15);
        }
        </style>
        """, unsafe_allow_html=True)
        tipo_vista_toggle = st.toggle("Mostrar por causa de muerte", value=False)
        tipo_vista = "Por causa de muerte" if tipo_vista_toggle else "Total general"

    if df_filtrado.empty:
        st.markdown("""
        <div style=\"background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;\">
            ⚠️ No hay datos disponibles para el filtro seleccionado.
        </div>
        """, unsafe_allow_html=True)
    else:
        if tipo_vista == "Total general":
            evolucion = df_filtrado.groupby("tiempo")["cantidad"].sum().reset_index()
        else:
            evolucion = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

        if evolucion.empty:
            st.markdown("""
            <div style=\"background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;\">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)
        else:
            mostrar_valores = False
            if tipo_filtro_tiempo == "Por años" and año_inicio == año_fin:
                mostrar_valores = True
                evolucion['tiempo'] = pd.to_datetime(evolucion['tiempo'], format='%Y-%m').dt.strftime('%B %Y').str.capitalize()

            # Asegurar que solo se usen etiquetas para los puntos existentes
            tickvals = evolucion['tiempo'].tolist() if tipo_filtro_tiempo == "Por años" and año_inicio == año_fin else None

            if tipo_vista == "Total general":
                fig_evolucion = px.line(
                    evolucion,
                    x='tiempo',
                    y='cantidad',
                    labels={'tiempo': 'Periodo', 'cantidad': 'Número de Homicidios'},
                    height=350
                )
                fig_evolucion.update_traces(
                    line_color='#00AEEF',
                    line_width=1,
                    mode='lines+markers' + ('+text' if mostrar_valores else ''),
                    marker=dict(size=7, color='#00AEEF'),
                    text=evolucion['cantidad'] if mostrar_valores else None,
                    textposition="bottom center"
                )
            else:
                causas_unicas = evolucion['causa_muerte'].unique()

                # 👉 Ordenar la leyenda como se desea
                orden_causas = ["Arma de fuego", "Asfixia", "Arma blanca", "Otra causa"]
                evolucion["causa_muerte"] = pd.Categorical(
                    evolucion["causa_muerte"],
                    categories=orden_causas,
                    ordered=True
                )
                evolucion = evolucion.sort_values(by=["causa_muerte", "tiempo"])
                
                color_map = {
                    "Arma de fuego": "#00AEEF",
                    "Asfixia": "#005EB8",
                    "Arma blanca": "#90A4AE",
                    "Otra causa": "#F39200"
                }

                fig_evolucion = px.line(
                    evolucion,
                    x='tiempo',
                    y='cantidad',
                    color='causa_muerte',
                    labels={
                        'tiempo': 'Periodo',
                        'cantidad': 'Número de Homicidios',
                        'causa_muerte': 'Causa'
                    },
                    color_discrete_map=color_map,
                    height=350
                )
                fig_evolucion.update_traces(
                    mode='lines+markers' + ('+text' if mostrar_valores else ''),
                    marker=dict(size=7),
                    line_width=1,
                )       

            fig_evolucion.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(family='Inter, sans-serif', color='#003366'),
                margin=dict(t=30, r=10, b=50, l=50),
                xaxis=dict(
                    tickformat=tickformat,
                    title='Periodo',
                    tickmode='array' if tickvals else tickmode,
                    tickvals=tickvals,
                    tickangle=-65,
                    tickfont=dict(size=14, color='#003366'),
                    gridcolor='rgba(145, 191, 219, 0.3)',
                    gridwidth=1
                ),
                yaxis=dict(
                    rangemode='tozero',
                    title_font=dict(size=16, color='#003366'),
                    tickfont=dict(size=14, color='#003366'),
                    gridcolor='rgba(145, 191, 219, 0.3)',
                    gridwidth=1,
                ),
                legend=dict(
                    title_font=dict(size=16, color='#003366'),
                    font=dict(size=14, color='#003366'),
                    bgcolor='#F0F2F5',
                ),
                legend_traceorder='normal'
            )

            st.plotly_chart(fig_evolucion, use_container_width=True)


with col_pie:
    with st.container():
        st.markdown("### Homicidios según sexo")

        sexo_data = df_filtrado.groupby('sexo')['cantidad'].sum().reset_index()

        if not sexo_data.empty:
            orden_sexo = [s for s in ["Mujer", "Hombre"] if s in sexo_data['sexo'].values]
            sexo_data = sexo_data.set_index('sexo').loc[orden_sexo].reset_index()

            total = sexo_data['cantidad'].sum()
            sexo_data['porcentaje_val'] = (sexo_data['cantidad'] / total * 100).round(1)
            sexo_data['etiqueta'] = sexo_data['porcentaje_val'].astype(str) + '%'

            fig_sexo = px.pie(
                sexo_data,
                values='cantidad',
                names='sexo',
                color='sexo',
                color_discrete_map={
                    "Mujer": "#00AEEF",
                    "Hombre": "#F39200"
                },
                category_orders={'sexo': ["Mujer", "Hombre"]},
                custom_data=['etiqueta', 'cantidad'],
                height=350
            )

            fig_sexo.update_traces(
                textposition='inside',
                textinfo='percent',
                textfont_size=24,
                textfont_color='#003366',
                textfont_family='Inter, sans-serif',
                hovertemplate='<b>%{label}</b><br>Cantidad= %{value}<br>Porcentaje= %{customdata[0]}<extra></extra>'
            )

            fig_sexo.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(family='Inter, sans-serif', color='#003366'),
                margin=dict(t=30, r=10, b=50, l=50),
                legend=dict(
                    title='Sexo:',
                    title_font=dict(size=16, color='#003366'),
                    font=dict(size=14, color='#003366'),
                    bgcolor='#F0F2F5',
                )
            )

            st.plotly_chart(fig_sexo, use_container_width=True)
        else:
            st.markdown("""
            <div style="background-color: #FFEBE6; border-left: 5px solid #FF6F61; padding: 12px; border-radius: 8px; color: #8B0000; font-weight: 600;">
                ⚠️ No hay datos disponibles para el filtro seleccionado.
            </div>
            """, unsafe_allow_html=True)

    # 🔹 Pie de página personalizado
st.markdown(f"""
    <div style="margin-top: 40px; text-align: right; font-size: 14px; color: #666;">
        Fuente de datos: <strong>SINADEF - Sistema Informático Nacional de Defunciones</strong><br>
        Para mayor información o consulta, escríbenos a <strong>xxxxxxx@cientifica.edu.pe</strong>.<br>
        Fecha de ultima actualización: <b>{fecha_actualizacion}</b>
    </div>
    """, unsafe_allow_html=True)    