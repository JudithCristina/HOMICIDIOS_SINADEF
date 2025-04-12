import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
import locale

# Configurar idioma español para fechas

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # tu preferencia
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')  # fallback al default del sistema (probablemente inglés)
    
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
        font-size: 18px!important
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
h1{
    padding: 0px !important
}
 .fecha-rango {
        font-size: 28px!important;
    }
 .total-muertes {
        font-size: 45px!important;
    }
 .st-emotion-cache-1y9tyez .st-emotion-cache-i0ptax{
       background: #003366 !important;
  }
   /* Cambiar color del título al pasar el mouse (hover) */
.streamlit-expanderHeader:hover {
        color: #F39200 !important;  /* Amarillo personalizado */
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
df_base = pd.read_csv("https://raw.githubusercontent.com/JudithCristina/sinadef-automatizado/main/data/processed/BASE_FINAL_GENERAL.csv")
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

    with st.expander("🎯 Filtros demográficos", expanded=True):
        sexo_sel = st.multiselect("Sexo", df["sexo"].unique(), default=df["sexo"].unique())
        causa_sel = st.multiselect("Causa", df["causa_muerte"].unique(), default=df["causa_muerte"].unique())
        edad_sel = st.multiselect("Grupo etario", df["edad"].unique(), default=df["edad"].unique())
        meses_sel = st.multiselect("Mes", sorted(df["mes"].unique()), default=sorted(df["mes"].unique()))

    with st.expander("🗓️ Filtro temporal", expanded=False):
        tipo_filtro_tiempo = st.radio("¿Cómo deseas filtrar el tiempo?", ["Por años", "Por rango reciente"])
        if tipo_filtro_tiempo == "Por años":
            año_inicio, año_fin = st.slider("Año", min_value=int(df["año"].min()),
                                            max_value=int(df["año"].max()),
                                            value=(int(df["año"].min()), int(df["año"].max())),
                                            step=1)
            rango_reciente = None
        else:
            rango_reciente = st.selectbox("Selecciona un rango reciente:", [
                "Última semana", "Último mes", "Últimos 3 meses", "Últimos 6 meses"
            ])
            año_inicio, año_fin = None, None

    with st.expander("📊 Visualización de la evolución de homicidios", expanded=False):
        tipo_vista = st.radio(
            "¿Cómo deseas visualizar la evolución de homicidios?",
            ["Total general", "Por causa del homicidio"]
        )
        
if not sexo_sel or not causa_sel or not edad_sel or not meses_sel:
    st.markdown("""
        <div style="background-color: #FFF3CD; 
                    border-left: 6px solid #F39200; 
                    padding: 12px 20px; 
                    margin-bottom: 20px; 
                    border-radius: 8px; 
                    color: #856404; 
                    font-size: 16px;">
            ⚠️ <strong>Por favor</strong>, selecciona al menos una opción en todos los filtros.
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# =====================
# APLICAR FILTRO TEMPORAL INTELIGENTE
# =====================
df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')
hoy = pd.Timestamp.today()
inicio, fin = None, None

if rango_reciente:
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

else:
    df = df[df["año"].between(año_inicio, año_fin)]
    inicio = df["fecha"].min()
    fin = df["fecha"].max()
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

# Mostrar título adaptado según el tipo de filtro temporal
# Mostrar título adaptado según el tipo de filtro temporal
if rango_reciente:
    if inicio.year == fin.year:
        if inicio.month == fin.month:
            # Mismo mes y año: solo mostrar mes
            titulo_rango = f"{inicio.strftime('%B de %Y')}"
        else:
            # Diferentes meses, mismo año
            titulo_rango = f"{inicio.strftime('%-d de %B')} al {fin.strftime('%-d de %B de %Y')}"
    else:
        # Años diferentes
        titulo_rango = f"{inicio.strftime('%-d de %B de %Y')} al {fin.strftime('%-d de %B de %Y')}"
else:
    titulo_rango = f"{año_inicio} - {año_fin}"

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;
                background-color: #F39200; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <div>
            <h1 style="font-size: 38px; margin: 0; color: #003366;">Homicidios con necropsia registrados en SINADEF</h1>
            <p class="fecha-rango" style="font-size: 20px; font-style: italic; margin: 4px 0 0 0; color: #003366;">
                ({titulo_rango})
            </p>
        </div>
        <div style="text-align: right;">
            <p class="fecha-rango" style="color: white; font-size: 25px; margin: 0;">Número de homicidios:</p>
            <p class="total-muertes" style="color: white; font-size: 40px; font-weight: bold; margin: 0;">{total_muertes:,}</p>
        </div>
    </div>
""", unsafe_allow_html=True)
# =====================
# GRAFICOS
# =====================
col_causa, col_edad = st.columns(2)

with col_causa:
    if rango_reciente == "Última semana":
        st.markdown("### Causas de muerte según día de ocurrencia")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%A')
        orden_x = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    elif rango_reciente == "Último mes":
        st.markdown("### Causas de muerte según día de ocurrencia")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%d/%m')
        orden_x = sorted(df_filtrado["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m'))

    elif rango_reciente in ["Últimos 3 meses", "Últimos 6 meses"]:
        st.markdown("### Causas de muerte según mes de ocurrencia")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%B %Y')
        meses_orden = df_filtrado["fecha"].dt.to_period("M").sort_values().unique()
        orden_x = [d.strftime('%B %Y') for d in meses_orden.to_timestamp()]

    else:
        st.markdown("### Causas de muerte según año de ocurrencia")

        df_filtrado["tiempo"] = df_filtrado["año"].astype(str)
        orden_x = sorted(df_filtrado["tiempo"].unique())

    # Agrupar por tiempo y causa
    causa_tiempo = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

    # Gráfico Altair
    chart_causa = alt.Chart(causa_tiempo).mark_bar().encode(
        x=alt.X('tiempo:N', title='Periodo', sort=orden_x),
        y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
        color=alt.Color('causa_muerte:N', title='Causa',
                        scale=alt.Scale(range=['#C7E9F1', '#00AEEF', '#005EB8', '#F39200'])),
        tooltip=[
            alt.Tooltip('tiempo:N', title='Periodo'),
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
    if rango_reciente == "Última semana":
        st.markdown("### Homicidios por etapas de vida según día")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%A')
        orden_x = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    elif rango_reciente == "Último mes":
        st.markdown("### Homicidios por etapas de vida según día")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%d/%m')
        orden_x = sorted(df_filtrado["tiempo"].unique(), key=lambda x: datetime.strptime(x, '%d/%m'))

    elif rango_reciente in ["Últimos 3 meses", "Últimos 6 meses"]:
        st.markdown("### Homicidios por etapas de vida según mes")

        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%B %Y')
        meses_orden = df_filtrado["fecha"].dt.to_period("M").sort_values().unique()
        orden_x = [d.strftime('%B %Y') for d in meses_orden.to_timestamp()]

    else:
        st.markdown("### Homicidios por etapas de vida según año")

        df_filtrado["tiempo"] = df_filtrado["año"].astype(str)
        orden_x = sorted(df_filtrado["tiempo"].unique())

    # Orden personalizado de grupos etarios
    orden_edad = ['Niño', 'Adolescente', 'Joven', 'Adulto', 'Adulto mayor']

    # Agrupar por tiempo y edad
    edad_tiempo = df_filtrado.groupby(['tiempo', 'edad'])['cantidad'].sum().reset_index()

    # Gráfico Altair
    chart_edad = alt.Chart(edad_tiempo).mark_bar().encode(
        x=alt.X('tiempo:N', title='Periodo', sort=orden_x),
        y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
        color=alt.Color('edad:N', title='Grupo etario',
                        scale=alt.Scale(range=['#005EB8', '#F39200', '#90A4AE', '#00AEEF', '#B2EBF2']),
                        sort=alt.Sort(orden_edad)),
        tooltip=[
            alt.Tooltip('tiempo:N', title='Periodo'),
            alt.Tooltip('edad:N', title='Grupo etario'),
            alt.Tooltip('cantidad:Q', title='Cantidad')
        ]
    )

    st.altair_chart(aplicar_estilo_altair(chart_edad), use_container_width=True)


col_linea, col_pie = st.columns([0.70, 0.30])

with col_linea:
    if tipo_filtro_tiempo == "Por años":
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.to_period("M").astype(str)
        sort_x = sorted(df_filtrado["tiempo"].unique())
        titulo_linea = "Evolución mensual de homicidios"
        titulo_linea += " (Total General)" if tipo_vista == "Total general" else " por Causa"

    else:
        df_filtrado["tiempo"] = df_filtrado["fecha"].dt.strftime('%d/%m')
        sort_x = sorted(df_filtrado["tiempo"].unique(), key=lambda x: datetime.strptime(x, "%d/%m"))
        titulo_linea = "Evolución diaria de homicidios"
        titulo_linea += " (Total General)" if tipo_vista == "Total general" else " por Causa"

    st.markdown(f"### {titulo_linea}")

    if tipo_vista == "Total general":
        evolucion = df_filtrado.groupby("tiempo")["cantidad"].sum().reset_index()

        chart = alt.Chart(evolucion).mark_line(
            point=alt.OverlayMarkDef(filled=True, size=60),
            strokeWidth=3,
            color="#00AEEF"
        ).encode(
            x=alt.X('tiempo:N', title='Periodo', sort=sort_x),
            y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
            tooltip=[
                alt.Tooltip('tiempo:N', title='Periodo'),
                alt.Tooltip('cantidad:Q', title='Muertes')
            ]
        )

    else:
        evolucion = df_filtrado.groupby(['tiempo', 'causa_muerte'])['cantidad'].sum().reset_index()

        chart = alt.Chart(evolucion).mark_line(
            point=alt.OverlayMarkDef(filled=True, size=50),
            strokeWidth=2
        ).encode(
            x=alt.X('tiempo:N', title='Periodo', sort=sort_x),
            y=alt.Y('cantidad:Q', title='Cantidad de muertes'),
            color=alt.Color('causa_muerte:N', title='Causa',
                            scale=alt.Scale(range=['#C7E9F1', '#00AEEF', '#005EB8', '#F39200'])),
            tooltip=[
                alt.Tooltip('tiempo:N', title='Periodo'),
                alt.Tooltip('causa_muerte:N', title='Causa'),
                alt.Tooltip('cantidad:Q', title='Muertes')
            ]
        )

    st.altair_chart(aplicar_estilo_altair(chart), use_container_width=True)


with col_pie:
    with st.container():
        st.markdown("### Homicidios según sexo")

        # ✅ Agrupar por sexo directamente
        sexo_data = df_filtrado.groupby('sexo')['cantidad'].sum().reset_index()

        if not sexo_data.empty:
            # ✅ Calcular porcentaje
            total = sexo_data['cantidad'].sum()
            sexo_data['porcentaje_val'] = (sexo_data['cantidad'] / total * 100).round(1)
            sexo_data['etiqueta'] = sexo_data['porcentaje_val'].astype(str) + '%'

            # Paleta personalizada (ya con nombres bonitos)
            color_scale = alt.Scale(
                domain=["Femenino", "Masculino"],
                range=["#00AEEF", "#F39200"]
            )

            base = alt.Chart(sexo_data).encode(
                theta=alt.Theta("cantidad:Q"),
                color=alt.Color("sexo:N", scale=color_scale, title="Sexo"),
                tooltip=[
                    alt.Tooltip("sexo:N", title="Sexo"),
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
