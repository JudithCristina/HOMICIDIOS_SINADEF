import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard de Muertes Violentas", layout="wide")

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
    h1 { font-size: 38px !important; }
    h2 { font-size: 30px !important; }
    h3 { font-size: 24px !important; }
    h4, label { font-size: 18px !important; }
    p{
        font-size: 16px!important
    }
    /* Sidebar */
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

    /* Inputs generales */
    .stSelectbox div, .stMultiSelect div, .stTextInput input {
        color: white !important;
        font-weight: 700 !important;
        font-size: 15px !important;
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

    /* Radio buttons */
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

    /* Botones */
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
    canvas {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .st-do {
   linear-gradient(
    to right,
    rgba(172, 177, 195, 0.25) 0%,
    rgba(172, 177, 195, 0.25) 50%,
    #F39200 50%,
    #F39200 100%,
    rgba(172, 177, 195, 0.25) 100%
) !important;
}
.st-eq {
      linear-gradient(
    to right,
    rgba(172, 177, 195, 0.25) 0%,
    rgba(172, 177, 195, 0.25) 50%,
    #F39200 50%,
    #F39200 100%,
    rgba(172, 177, 195, 0.25) 100%
) !important;
}
.st-emotion-cache-b92z60{
      color: #F39200 !important; 
              font-weight: bold;s
}
.st-emotion-cache-1dj3ksd {
   background-color: #F39200 !important; 
}
    </style>
""", unsafe_allow_html=True)

# =====================
# CONFIG ALT STYLE
# =====================
def aplicar_estilo_altair(chart):
    return chart.configure_axis(
        grid=True,
        gridColor='#91BFDB',
        gridOpacity=0.3,
        labelColor='#003366',
        titleColor='#003366',
        labelFontSize=14,
        titleFontSize=16
    ).configure_legend(
        labelColor='#003366',
        titleColor='#003366',
        orient='right',
        labelFontSize=16,
        titleFontSize=16
    ).configure_view(
        stroke=None
    ).configure_title(
        color='#003366',
        fontSize=22,
        anchor='start'
    ).properties(
        background='#ffffff',
        padding={"left": 10, "top": 10, "right": 10, "bottom": 10}
    )

plt.rcParams.update({
    'font.size': 11,
    'text.color': '#003366',
    'font.family': 'Segoe UI'
})

# =====================
# CARGA BASE
# =====================
mes_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
df_base = pd.read_csv("data/processed/BASE_FINAL_GENERAL.csv")
df = pd.DataFrame()
df["sexo"] = df_base["SEXO"]
df["edad"] = df_base["EDADES"]
df["causa_muerte"] = df_base["Grupo_Causa"]
df["mes"] = df_base["MES"].map(mes_dict)
df["año"] = df_base["ANIO"]
df["fecha"] = df_base["FECHA"]
df["cantidad"] = 1

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("## 🔎 Filtros del Dashboard")
    sexo_sel = st.multiselect("Sexo", df["sexo"].unique(), default=df["sexo"].unique())
    causa_sel = st.multiselect("Causa", df["causa_muerte"].unique(), default=df["causa_muerte"].unique())
    edad_sel = st.multiselect("Grupo etario", df["edad"].unique(), default=df["edad"].unique())
    meses_sel = st.multiselect("Mes", sorted(df["mes"].unique()), default=sorted(df["mes"].unique()))
    # 🔽 Nuevo filtro temporal unificado
    st.markdown("### 🗓️ Filtro temporal")
    tipo_filtro_tiempo = st.radio("¿Cómo deseas filtrar el tiempo?", ["Por años", "Por rango reciente"])

    if tipo_filtro_tiempo == "Por años":
        año_inicio, año_fin = st.slider("Año", min_value=int(df["año"].min()), max_value=int(df["año"].max()),
                                        value=(int(df["año"].min()), int(df["año"].max())), step=1)
        rango_reciente = None
    else:
        rango_reciente = st.selectbox("Selecciona un rango reciente:", [
            "Última semana", "Último mes", "Últimos 3 meses", "Últimos 6 meses"
        ])
        año_inicio, año_fin = None, None
    tipo_vista = st.radio(
        "Filtro de visualización de evolución mensual:",
        ["Total general", "Por causa de muerte"]
    )

if not sexo_sel or not causa_sel or not edad_sel or not meses_sel:
    st.warning("⚠️ Por favor, selecciona al menos una opción en todos los filtros.")
    st.stop()

# Asegurarse que la columna fecha esté en formato datetime
df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')

# Aplicar el filtro temporal según la selección del sidebar
hoy = pd.Timestamp.today()
if rango_reciente:
    if rango_reciente == "Última semana":
        df = df[df["fecha"] >= hoy - timedelta(weeks=1)]
    elif rango_reciente == "Último mes":
        df = df[df["fecha"] >= hoy - pd.DateOffset(months=1)]
    elif rango_reciente == "Últimos 3 meses":
        df = df[df["fecha"] >= hoy - pd.DateOffset(months=3)]
    elif rango_reciente == "Últimos 6 meses":
        df = df[df["fecha"] >= hoy - pd.DateOffset(months=6)]
else:
    df = df[df["año"].between(año_inicio, año_fin)]
# =====================
# FILTRADO
# =====================
df_filtrado = df[
    (df["sexo"].isin(sexo_sel)) &
    (df["causa_muerte"].isin(causa_sel)) &
    (df["edad"].isin(edad_sel)) &
    (df["mes"].isin(meses_sel))
]
total_muertes = df_filtrado["cantidad"].sum()

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;
                background-color: #F39200; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <h1 style=" font-size: 40px; margin: 0;">Muertes violentas {año_inicio} - {año_fin}</h1>
        <div style="text-align: right;">
            <p style="color: white; font-size: 25px; margin: 0;">Total de Muertes</p>
            <p style="color: white; font-size: 40px; font-weight: bold; margin: 0;">{total_muertes:,}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================
# GRAFICOS
# =====================
col_causa, col_edad = st.columns(2)

with col_causa:
    st.markdown("### Causas de Muerte por Año")
    causa_año = df_filtrado.groupby(['año', 'causa_muerte'])['cantidad'].sum().reset_index()
    chart_causa = alt.Chart(causa_año).mark_bar().encode(
         x=alt.X('año:O',title='Año'),
        y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
        color=alt.Color('causa_muerte:N', title='Causa',  scale=alt.Scale(range=['#C7E9F1', '#00AEEF', '#005EB8', '#F39200']),
                        ),
        tooltip=[
             alt.Tooltip('año:O', title='Año'),
            alt.Tooltip('causa_muerte:N', title='Causa'),
            alt.Tooltip('cantidad:Q', title='Cantidad')
        ]
    )
    st.altair_chart(aplicar_estilo_altair(chart_causa), use_container_width=True)


# Agrupar y luego mapear los nombres amigables
edad_año = df_filtrado.groupby(['año', 'edad'])['cantidad'].sum().reset_index()

# Orden personalizado basado en los valores reales de EDADES
orden_personalizado = ['Niño', 'Adolescente', 'Joven', 'Adulto', 'Adulto mayor']

with col_edad:
    st.markdown("### Distribución Etaria por Año")

    chart_edad = alt.Chart(edad_año).mark_bar().encode(
        x=alt.X('año:O', title='Año'),
        y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
        color=alt.Color('edad:N', title='Grupo etario',
                        scale=alt.Scale(range=['#005EB8', '#F39200', '#90A4AE', '#00AEEF', '#B2EBF2']),
                        sort=alt.Sort(orden_personalizado)),
        tooltip=[
            alt.Tooltip('año:O', title='Año'),
            alt.Tooltip('edad:N', title='Grupo etario'),
            alt.Tooltip('cantidad:Q', title='Cantidad')
        ]
    )

    st.altair_chart(aplicar_estilo_altair(chart_edad), use_container_width=True)


col_linea, col_pie = st.columns([0.70, 0.30])

with col_linea:
    if tipo_vista == "Total general":
        st.markdown("### Evolución Mensual de Muertes (Total General)")
    else:
        st.markdown("### Evolución Mensual de Muertes por Causa")

    df_filtrado["fecha"] = pd.to_datetime(df_filtrado["fecha"], errors='coerce')
    df_filtrado["año_mes"] = df_filtrado["fecha"].dt.to_period("M").astype(str)

    if tipo_vista == "Total general":
        evolucion_total = df_filtrado.groupby("año_mes")["cantidad"].sum().reset_index()

        chart_general = alt.Chart(evolucion_total).mark_line(
            point=alt.OverlayMarkDef(filled=True, size=60),
            strokeWidth=3,
            color="#00AEEF"
        ).encode(
            x=alt.X('año_mes:N', title='Año-Mes'),
            y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
            tooltip=[
                alt.Tooltip('año_mes:N', title='Año-Mes'),
                alt.Tooltip('cantidad:Q', title='Total de muertes')
            ]
        )
        st.altair_chart(aplicar_estilo_altair(chart_general), use_container_width=True)

    else:
        evolucion_causa = df_filtrado.groupby(['año_mes', 'causa_muerte'])['cantidad'].sum().reset_index()

        chart_causas = alt.Chart(evolucion_causa).mark_line(
            point=alt.OverlayMarkDef(filled=True, size=50),
            strokeWidth=2
        ).encode(
            x=alt.X('año_mes:N', title='Año-Mes'),
            y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
            color=alt.Color('causa_muerte:N', title='Causa', scale=alt.Scale(range=['#C7E9F1', '#00AEEF', '#005EB8', '#F39200'])),
            tooltip=[
                alt.Tooltip('año_mes:N', title='Fecha'),
                alt.Tooltip('causa_muerte:N', title='Causa'),
                alt.Tooltip('cantidad:Q', title='Muertes')
            ]
        )
        st.altair_chart(aplicar_estilo_altair(chart_causas), use_container_width=True)



with col_pie:
    with st.container():
        st.markdown("### Distribución por Sexo")

        # ✅ Agrupar primero
        sexo_data = df_filtrado.groupby('sexo')['cantidad'].sum().reset_index()

        if not sexo_data.empty:
            # ✅ Luego agregar etiquetas personalizadas
            sexo_data['sexo_etiqueta'] = sexo_data['sexo'].map({
                'FEMENINO': 'Femenino',
                'MASCULINO': 'Masculino'
            })

            # Calcular porcentaje
            total = sexo_data['cantidad'].sum()
            sexo_data['porcentaje_val'] = (sexo_data['cantidad'] / total * 100).round(1)
            sexo_data['etiqueta'] = sexo_data['porcentaje_val'].astype(str) + '%'

            # Paleta personalizada
            color_scale = alt.Scale(
                domain=["Femenino", "Masculino"],
                range=["#00AEEF", "#F39200"]
            )

            base = alt.Chart(sexo_data).encode(
                theta=alt.Theta("cantidad:Q"),
                color=alt.Color("sexo_etiqueta:N", scale=color_scale, title="Sexo"),
                tooltip=[
                    alt.Tooltip("sexo_etiqueta:N", title="Sexo"),
                    alt.Tooltip("cantidad:Q", title="Cantidad"),
                    alt.Tooltip("etiqueta:N", title="Porcentaje")
                ]
            )

            donut = base.mark_arc(innerRadius=60)

            texto = base.mark_text(
                radius=85,
                size=22,
                font='Inter',
                fontWeight='bold',
                align='center',
                baseline='middle'
            ).encode(
                text="etiqueta:N",
                color=alt.value("#003366")
            )

            chart_final = (donut + texto).configure_view(stroke=None)
            st.altair_chart(aplicar_estilo_altair(chart_final), use_container_width=True)

        else:
            st.warning("⚠️ No hay datos disponibles para el gráfico de sexo con los filtros aplicados.")


# =====================
# TABLA FINAL
# =====================
with st.expander("📋 Ver tabla de datos filtrados"):
    st.dataframe(df_filtrado)
