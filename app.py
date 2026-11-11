import streamlit as st
import pandas as pd
import plotly.express as px
import gspread

from datetime import datetime, date, timedelta

# ======================================================
# CONFIGURACIÓN
# ======================================================

st.set_page_config(
    page_title="Dashboard de Obras y Servicios",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ Gestión Operativa de Obras y Servicios")

st.subheader("Municipalidad de Villa Ojo de Agua")

st.markdown("""
**Integrantes del proyecto:**

- Agustina Pieroni
- Tobias Escobedo Miranda
- Ana Laura Malagueño

**Carrera:** Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial
""")

st.caption("Proyecto de Prácticas Profesionalizantes | PP1 - PP2 - PP3")

st.divider()
st.markdown("### 📌 Sobre el proyecto")

st.markdown("""
Este dashboard forma parte del proyecto de **Prácticas Profesionalizantes PP1, PP2 y PP3**,
desarrollado para la **Municipalidad de Villa Ojo de Agua**.

Su objetivo es mejorar la gestión de la información de la Secretaría de Obras y Servicios
Públicos mediante herramientas digitales que permiten registrar, centralizar y visualizar
datos relacionados con la recolección de residuos y los accidentes laborales.

A través de la integración de **Telegram, Google Sheets y Python con Streamlit**,
se busca facilitar el seguimiento de las actividades operativas y brindar información
útil para la toma de decisiones.
""")

st.divider()


# Actualizar la información cada 30 segundos.
# Streamlit ejecutará nuevamente la aplicación.
if hasattr(st, "fragment"):
    @st.fragment(run_every="30s")
    def panel_datos():
        mostrar_dashboard()

    # La función se define más abajo.
else:
    pass

# ======================================================
# CONEXIÓN CON GOOGLE SHEETS
# ======================================================

@st.cache_resource
def conectar_google_sheets():

    if "gcp_service_account" in st.secrets:
       credentials = dict(st.secrets["gcp_service_account"])
       gc = gspread.service_account_from_dict(credentials)
    else:
       gc = gspread.service_account(
        filename="chatbot-para-registro-de-datos-b292d3d251a3.json"
    )

    return gc.open("Registro de accidentes")


# ======================================================
# CARGA DE DATOS
# ======================================================

@st.cache_data(ttl=30)
def cargar_datos():
    
    spreadsheet = conectar_google_sheets()

    hoja_volumen = spreadsheet.worksheet("Vol Recolectado")
    hoja_accidentes = spreadsheet.worksheet("Accidentes")

    df_volumen = pd.DataFrame(
        hoja_volumen.get_all_records()
    )

    df_accidentes = pd.DataFrame(
        hoja_accidentes.get_all_records()
    )

    # Normalizar los encabezados.
    df_volumen.columns = [
        str(col).strip() for col in df_volumen.columns
    ]

    df_accidentes.columns = [
        str(col).strip() for col in df_accidentes.columns
    ]

    # Convertir fechas.
    if "Fecha" in df_volumen.columns:
        df_volumen["Fecha"] = pd.to_datetime(
            df_volumen["Fecha"],
            dayfirst=True,
            errors="coerce"
        )

    if "Fecha" in df_accidentes.columns:
        df_accidentes["Fecha"] = pd.to_datetime(
            df_accidentes["Fecha"],
            dayfirst=True,
            errors="coerce"
        )

    # Convertir kilogramos a valores numéricos.
    if "Kg Recolectados" in df_volumen.columns:
        df_volumen["Kg Recolectados"] = pd.to_numeric(
            df_volumen["Kg Recolectados"],
            errors="coerce"
        )

    return df_volumen, df_accidentes


# ======================================================
# DASHBOARD
# ======================================================

def mostrar_dashboard():

    try:
        df_volumen, df_accidentes = cargar_datos()
        

    except Exception as error:
        st.error(
            "No se pudo acceder a Google Sheets. "
            "Revisá las credenciales, el nombre del documento "
            "y los permisos de acceso."
        )

        st.caption(f"Detalle técnico: {error}")
        st.stop()

    if df_volumen.empty and df_accidentes.empty:
        st.warning("Todavía no hay registros en las pestañas.")
        st.stop()

    # ==============================================
    # FILTROS
    # ==============================================

    st.sidebar.header("Filtros")

    fechas_disponibles = []

    for df in [df_volumen, df_accidentes]:
        if "Fecha" in df.columns:
            fechas_disponibles.extend(
                df["Fecha"].dropna().tolist()
            )

    if fechas_disponibles:

        fecha_min = min(fechas_disponibles).date()
        fecha_max = max(fechas_disponibles).date()

        rango = st.sidebar.date_input(
            "Período de análisis",
            value=(fecha_min, fecha_max),
            min_value=fecha_min,
            max_value=fecha_max
        )

        if isinstance(rango, tuple) and len(rango) == 2:
            inicio, fin = rango
        else:
            inicio = rango[0] if isinstance(rango, tuple) else rango
            fin = inicio

        if "Fecha" in df_volumen.columns:
            df_volumen = df_volumen[
                df_volumen["Fecha"].dt.date.between(inicio, fin)
            ]

        if "Fecha" in df_accidentes.columns:
            df_accidentes = df_accidentes[
                df_accidentes["Fecha"].dt.date.between(inicio, fin)
            ]

    # ==============================================
    # INDICADORES PRINCIPALES
    # ==============================================

    total_kg = (
        df_volumen["Kg Recolectados"].sum()
        if "Kg Recolectados" in df_volumen.columns
        else 0
    )

    cantidad_registros = len(df_volumen)
    cantidad_accidentes = len(df_accidentes)

    promedio_kg = (
        total_kg / cantidad_registros
        if cantidad_registros > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Kilogramos recolectados",
        f"{total_kg:,.0f} kg"
    )

    c2.metric(
        "Registros de recolección",
        cantidad_registros
    )

    c3.metric(
        "Promedio por registro",
        f"{promedio_kg:,.1f} kg"
    )

    c4.metric(
        "Accidentes registrados",
        cantidad_accidentes
    )

    st.divider()

    # ==============================================
    # GRÁFICO POR CAMIÓN
    # ==============================================

    st.subheader("Kilogramos recolectados por camión")

    if (
        not df_volumen.empty
        and {"Camion", "Kg Recolectados"}.issubset(df_volumen.columns)
    ):

        por_camion = (
            df_volumen.groupby("Camion", as_index=False)
            ["Kg Recolectados"].sum()
            .sort_values("Kg Recolectados", ascending=False)
        )

        fig_camion = px.bar(
            por_camion,
            x="Camion",
            y="Kg Recolectados",
            text_auto=".0f",
            title="Volumen total por vehículo"
        )

        st.plotly_chart(
            fig_camion,
            use_container_width=True
        )

    else:
        st.info("No hay datos suficientes para el gráfico por camión.")

    # ==============================================
    # EVOLUCIÓN TEMPORAL
    # ==============================================

    st.subheader("Evolución de la recolección")

    if (
        not df_volumen.empty
        and {"Fecha", "Kg Recolectados"}.issubset(df_volumen.columns)
    ):

        por_fecha = (
            df_volumen.dropna(subset=["Fecha"])
            .groupby("Fecha", as_index=False)
            ["Kg Recolectados"].sum()
            .sort_values("Fecha")
        )

        fig_fecha = px.line(
            por_fecha,
            x="Fecha",
            y="Kg Recolectados",
            markers=True,
            title="Kilogramos registrados por fecha"
        )

        st.plotly_chart(
            fig_fecha,
            use_container_width=True
        )

    # ==============================================
    # COMPARACIÓN POR TURNO
    # ==============================================

    st.subheader("Recolección por turno")

    if (
        not df_volumen.empty
        and {"Turno", "Kg Recolectados"}.issubset(df_volumen.columns)
    ):

        por_turno = (
            df_volumen.groupby("Turno", as_index=False)
            ["Kg Recolectados"].sum()
        )

        fig_turno = px.bar(
            por_turno,
            x="Turno",
            y="Kg Recolectados",
            color="Turno",
            title="Comparación entre turnos"
        )

        st.plotly_chart(
            fig_turno,
            use_container_width=True
        )

    # ==============================================
    # ACCIDENTES
    # ==============================================

    st.divider()
    st.header("🦺 Análisis de accidentes laborales")

    if not df_accidentes.empty:

        if "Tipo" in df_accidentes.columns:

            por_tipo = (
                df_accidentes["Tipo"]
                .fillna("Sin especificar")
                .value_counts()
                .rename_axis("Tipo")
                .reset_index(name="Cantidad")
            )

            fig_tipo = px.bar(
                por_tipo,
                x="Tipo",
                y="Cantidad",
                title="Accidentes por tipo"
            )

            st.plotly_chart(
                fig_tipo,
                use_container_width=True
            )

        if "Lesion" in df_accidentes.columns:

            por_lesion = (
                df_accidentes["Lesion"]
                .fillna("Sin especificar")
                .value_counts()
                .rename_axis("Lesion")
                .reset_index(name="Cantidad")
            )

            fig_lesion = px.pie(
                por_lesion,
                names="Lesion",
                values="Cantidad",
                title="Distribución de lesiones o tipos registrados"
            )

            st.plotly_chart(
                fig_lesion,
                use_container_width=True
            )

        if "Barrio" in df_accidentes.columns:

            por_barrio = (
                df_accidentes["Barrio"]
                .fillna("Sin especificar")
                .value_counts()
                .rename_axis("Barrio")
                .reset_index(name="Cantidad")
            )

            st.subheader("Accidentes por barrio")

            st.bar_chart(
                por_barrio.set_index("Barrio")
            )

    else:
        st.info("No hay accidentes registrados en el período seleccionado.")

    # ==============================================
    # TABLAS DE DETALLE
    # ==============================================

    st.divider()

    with st.expander("Ver registros de recolección"):
        st.dataframe(
            df_volumen,
            use_container_width=True
        )

    with st.expander("Ver registros de accidentes"):
        st.dataframe(
            df_accidentes,
            use_container_width=True
        )

    st.caption(
        "Fuente: Google Sheets. Los datos simulados se utilizan "
        "para validar el dashboard y no deben interpretarse "
        "como resultados operativos reales."
    )


# Ejecutar el dashboard con actualización periódica.
if hasattr(st, "fragment"):
    panel_datos()
else:
    mostrar_dashboard()
  