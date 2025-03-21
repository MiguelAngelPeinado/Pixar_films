import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------------
# ---- CONFIGURACIÓN GLOBAL ----
st.set_page_config(
    page_title="Pixar Films Dashboard",
    layout="wide",
)

# ---- CARGAR DATOS ----
df = pd.read_csv("Data/pixar_clean_streamlit.csv")

# ---- ESTILOS ----
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        body, .stApp {
            background-color: #f5f5f5;
        }
        .block-container {
            padding-top: 3.5rem;
        }
        h1, h2, h3, h4 {
            color: #333333;
        }
        .custom-title {
            font-family: 'Cinzel', serif;
            font-size: 40px;
            color: #333333;
        }
        .kpi-container {
            display: flex;
            justify-content: center;
            flex-wrap: nowrap;
            gap: 10px;
            margin-bottom: 30px;
        }
        .kpi-box {
            flex: 1 1 215px;
            max-width: 260px;
            min-width: 180px;
            background-color: lightgray;
            padding: 6px 4px;
            height: auto;
            border-radius: 10px;
            text-align: center;
        }
        .kpi-title {
            color: #333;
            font-size: 15px;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .kpi-value {
            color: #1f77b4;
            font-size: 16px;
            margin-top: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------------
# ---- TÍTULO ----
def render_title():
    st.markdown(
        """
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Pixar_logo.svg/320px-Pixar_logo.svg.png' width='300'>
            <h1 class='custom-title' style='margin-right: 0px;'>DASHBOARD</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------------
# ---- KPIs ----
def render_kpis():
    total_box_office = df["box_office_worldwide"].sum()
    most_productive_year = int(
        df.groupby("year")["box_office_worldwide"].sum().idxmax()
    )
    most_profitable_film = df.loc[df["profit_margin"].idxmax()]["film"]

    st.subheader("Key Metrics")

    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-title">💰 Total Worldwide Box Office</div>
                <div class="kpi-value">$ {total_box_office:,.1f} M. (USD)</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-title">📅 Most Productive Year</div>
                <div class="kpi-value">{most_productive_year}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-title">🏆 Most Profitable Film</div>
                <div class="kpi-value">{most_profitable_film}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------------
# ---- FILTROS SIDEBAR ----
def render_sidebar_filters():
    st.sidebar.markdown(
        """
        <style>
        .sidebar-title {
            color: #ff4b4b;
            font-size: 22px;
            font-weight: bold;
            text-transform: uppercase;
            font-family: 'Source Sans Pro', sans-serif;
            margin-bottom: 10px;
        }
        </style>
        <div class="sidebar-title">Interactive Filters</div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Slider de años
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    selected_year = st.sidebar.slider(
        "Select Year Range:", min_year, max_year, (min_year, max_year)
    )
    st.sidebar.markdown("---")

    # Film rating filter
    rating_options = df["film_rating"].dropna().unique()
    selected_ratings = st.sidebar.multiselect(
        "Select Film Rating:", rating_options, default=rating_options
    )
    st.sidebar.markdown(
        "<span style='color:#f5f5f5;'>*G: General Audiences (All ages admitted)*  <br>*PG: Parental Guidance Suggested*</span>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # 🚀 CITA MOTIVACIONAL
    st.sidebar.markdown(
        """
        <p style='color: #333; font-size:16px; text-align:center; margin-top:210px;'>
            "To infinity... and beyond!"
        </p>
        """,
        unsafe_allow_html=True,
    )

    # LINK Y COPYRIGHT
    st.sidebar.markdown(
        """
        <p style='text-align:center; font-size:15px; margin-top:16px;'>
            <a href='https://www.pixar.com' target='_blank' style='color:#ff4b4b; text-decoration:none;'>www.pixar.com</a> <br>
            <span style='color:#333;'>© Disney / Pixar</span>
        </p>
        """,
        unsafe_allow_html=True,
    )

    return selected_year, selected_ratings


# -----------------------------------------------------------------------------------
# ---- GRAFICO FILTRADO ----
def render_filtered_graph(selected_year, selected_ratings, df):
    filtered_df = df[
        (df["year"] >= selected_year[0])
        & (df["year"] <= selected_year[1])
        & (df["film_rating"].isin(selected_ratings))
    ]

    filtered_sorted = filtered_df.sort_values(by="year").reset_index(drop=True)

    fig_filtered = go.Figure()
    fig_filtered.add_trace(
        go.Bar(
            x=filtered_sorted["film"],
            y=filtered_sorted["budget"],
            name="Budget (M USD)",
            marker_color="tomato",
        )
    )
    fig_filtered.add_trace(
        go.Bar(
            x=filtered_sorted["film"],
            y=filtered_sorted["profit_margin"],
            name="Profit Margin (M USD)",
            marker_color="darkgrey",
        )
    )

    filtered_years = filtered_sorted["year"].unique()

    for year in filtered_years:
        year_idx = filtered_sorted[filtered_sorted["year"] == year].index[0]
        fig_filtered.add_vline(
            x=year_idx,
            line_width=1.5,
            line_dash="dot",
            line_color="darkgray",
            opacity=0.6,
        )
        fig_filtered.add_annotation(
            x=year_idx,
            y=filtered_sorted[["budget", "profit_margin"]].max().max() + 50,
            text=str(int(year)),
            showarrow=False,
            font=dict(color="darkgray", size=14, family="Arial"),
            textangle=-90,
            xanchor="center",
            yanchor="bottom",
            xshift=-8,
            yshift=-20,
        )

    fig_filtered.update_layout(
        barmode="group",
        title=dict(
            text="Budget vs Profit Margin (Interactive Filter)",
            font=dict(size=18, family="Arial Black", color="#333333"),
            x=0.0,  # 👈🏽 Alinear a la izquierda
            xanchor="left",
        ),
        xaxis_title="Film",
        yaxis_title="Millions USD",
        xaxis_title_font=dict(size=17, color="#333333", family="Arial Black"),
        yaxis_title_font=dict(size=17, color="#333333", family="Arial Black"),
        xaxis_tickangle=-45,
        xaxis=dict(tickfont=dict(color="#333333")),
        yaxis=dict(tickfont=dict(color="#333333")),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="right",
            x=1,
            bgcolor="lightgray",
            borderwidth=0,
            bordercolor="lightgray",
            font=dict(size=12, color="#333333"),
        ),
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        height=650,
    )

    return fig_filtered


# ----------------------------------------------------------------------------
# ---- GRAFICOS ADICIONALES ----


def render_additional_charts(df, selected_year):
    st.markdown(
        """<h2 style='text-align: left; color: #333333;'>Additional Insights</h2>""",
        unsafe_allow_html=True,
    )

    # Filtramos años seleccionados
    filtered_df = df[
        (df["year"] >= selected_year[0]) & (df["year"] <= selected_year[1])
    ]

    # -------------- PRIMER GRÁFICO -----------------
    fig_scatter = px.scatter(
        filtered_df,
        x="budget",
        y="box_office_worldwide",
        color="year",
        hover_data={
            "film": True,
            "year": True,
            "budget": ":.1f",
            "box_office_worldwide": ":.1f",
        },
        color_continuous_scale="Magma",
        labels={
            "budget": "Budget (M USD)",
            "box_office_worldwide": "Worldwide Box Office (M USD)",
            "year": "Year",
        },
        title="Worldwide Box Office vs Budget",
    )

    fig_scatter.update_traces(marker=dict(size=12, line=dict(width=1, color="#333333")))
    fig_scatter.update_layout(
        title_font=dict(size=18, family="Arial Black", color="#333333"),
        xaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
        yaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        coloraxis_colorbar=dict(
            tickfont=dict(color="#333333"),
            title=dict(  # Aquí es donde cambia
                text="Year",  # Texto que aparece en la barra de colores
                font=dict(color="#333333"),
            ),
        ),
        height=600,
        xaxis=dict(
            tickfont=dict(color="#333333"),
            title_font=dict(size=14, family="Arial Black", color="#333333"),
            showgrid=True,
            gridcolor="lightgrey",
        ),
        yaxis=dict(
            tickfont=dict(color="#333333"),
            title_font=dict(size=14, family="Arial Black", color="#333333"),
            showgrid=True,
            gridcolor="lightgrey",
        ),
    )

    # -------------- SEGUNDO GRÁFICO -----------------
    pixar_sorted = filtered_df.sort_values("year")

    fig_scores = go.Figure()

    fig_scores.add_trace(
        go.Scatter(
            x=pixar_sorted["year"],
            y=pixar_sorted["rotten_tomatoes"],
            mode="lines+markers",
            name="Rotten Tomatoes",
            line=dict(color="tomato", shape="spline"),
            marker=dict(size=8),
        )
    )

    fig_scores.add_trace(
        go.Scatter(
            x=pixar_sorted["year"],
            y=pixar_sorted["metacritic"],
            mode="lines+markers",
            name="Metacritic",
            line=dict(color="dimgrey", shape="spline"),
            marker=dict(size=8),
        )
    )

    fig_scores.update_layout(
        title="Score Evolution",
        title_font=dict(size=18, family="Arial Black", color="#333333"),
        xaxis_title="Year",
        yaxis_title="Score (0-100)",
        height=600,
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="right",
            x=1,
            bgcolor="lightgray",
            bordercolor="lightgray",
            borderwidth=1,
            font=dict(size=12, color="#333333"),
        ),
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        xaxis=dict(
            tickfont=dict(color="#333333"),
            title_font=dict(size=14, family="Arial Black", color="#333333"),
            showgrid=True,
            gridcolor="lightgrey",
        ),
        yaxis=dict(
            tickfont=dict(color="#333333"),
            title_font=dict(size=14, family="Arial Black", color="#333333"),
            showgrid=True,
            gridcolor="lightgrey",
        ),
    )

    fig_scores.update_xaxes(dtick=2, tickangle=45)

    # -------------- MOSTRAR EN DOS COLUMNAS -----------------
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown(
            "<p style='color: #333333; font-size: 16px; text-align: center;'>Higher budgets often correlate with higher worldwide box office revenue, but outliers suggest budget alone doesn't guarantee success.</p>",
            unsafe_allow_html=True,
        )
    with col2:
        st.plotly_chart(fig_scores, use_container_width=True)
        st.markdown(
            "<p style='color: #333333; font-size: 16px; text-align: center;'>Critics' ratings fluctuate over the years, with some years showing a clear divergence between Rotten Tomatoes and Metacritic scores.</p>",
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------------
# ---- GRÁFICOS ADICIONALES EN EXPANDER ----
def render_extra_critics_charts(df):
    st.markdown(
        """<hr style="border: none; height: 2px; background-color: #999999; margin: 30px 0;">""",
        unsafe_allow_html=True,
    )

    # ---- Personalizar estilo del expander ----
    st.markdown(
        """
        <style>
        /* Apunta directamente al resumen (header) del expander */
        div[data-testid="stExpander"] > details > summary {
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 20px;
            color: #f5f5f5;
            background-color: #262730;
            padding: 10px;
            border-radius: 10px;
        }
        div[data-testid="stExpander"] > details > summary:hover {
            background-color: #999999;
            color: #f5f5f5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Expander con estilo
    with st.expander(
        "🔍 SEE ADDITIONAL CRITICS INSIGHTS  -   👉🏻  Click here if you'd like to explore how critics' scores influence box office performance.",
        expanded=False,
    ):
        # --- Primer gráfico: Box Office vs Rotten Tomatoes ---
        fig_box_vs_rt = px.scatter(
            df,
            x="rotten_tomatoes",
            y="box_office_worldwide",
            hover_data={"film": True, "year": True},
            labels={
                "rotten_tomatoes": "Rotten Tomatoes Score",
                "box_office_worldwide": "Worldwide Box Office (M USD)",
            },
            trendline="ols",
            title="Worldwide Box Office vs Rotten Tomatoes Score",
        )

        fig_box_vs_rt.update_traces(
            marker=dict(color="tomato", size=10, line=dict(width=1, color="#333333"))
        )
        fig_box_vs_rt.update_traces(
            selector=dict(mode="lines"), line=dict(dash="dot", color="darkred")
        )
        fig_box_vs_rt.update_layout(
            width=700,
            height=600,
            title_font=dict(size=18, family="Arial Black", color="#333333"),
            xaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
            yaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
            plot_bgcolor="#f5f5f5",
            paper_bgcolor="#f5f5f5",
            xaxis=dict(tickfont=dict(color="#333333")),
            yaxis=dict(tickfont=dict(color="#333333")),
        )

        # --- Segundo gráfico: Box Office vs Metacritic ---
        fig_box_vs_meta = px.scatter(
            df,
            x="metacritic",
            y="box_office_worldwide",
            hover_data={"film": True, "year": True},
            labels={
                "metacritic": "Metacritic Score",
                "box_office_worldwide": "Worldwide Box Office (M USD)",
            },
            trendline="ols",
            title="Worldwide Box Office vs Metacritic Score",
        )

        fig_box_vs_meta.update_traces(
            marker=dict(color="dimgrey", size=10, line=dict(width=1, color="#333333"))
        )
        fig_box_vs_meta.update_traces(
            selector=dict(mode="lines"), line=dict(dash="dot", color="black")
        )
        fig_box_vs_meta.update_layout(
            width=700,
            height=600,
            title_font=dict(size=18, family="Arial Black", color="#333333"),
            xaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
            yaxis_title_font=dict(size=14, family="Arial Black", color="#333333"),
            plot_bgcolor="#f5f5f5",
            paper_bgcolor="#f5f5f5",
            xaxis=dict(tickfont=dict(color="#333333")),
            yaxis=dict(tickfont=dict(color="#333333")),
        )

        # ---- Mostrar en 2 columnas ----
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_box_vs_rt)
        with col2:
            st.plotly_chart(fig_box_vs_meta)
        # ---- TEXTO EXPLICATIVO ----
        st.markdown(
            """
            <p style='color: #262730; font-size: 18px; text-align: center; margin-top: 20px;'>
                Critics' ratings can influence worldwide box office performance, but as shown, high scores do not always guarantee higher earnings. 
                Audience preferences, marketing, and other factors also play crucial roles.
            </p>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------------
# ---- SELECTOR DE PELÍCULAS ----
def render_film_selector(df):
    from streamlit.components.v1 import html

    # Solo estilizamos el selectbox
    st.markdown(
        """
        <style>
        /* Fondo y borde para el selectbox */
        div[data-baseweb="select"] {
            background-color: #bcbcbc;
            border: 1px solid tomato;
            border-radius: 8px;
            padding: 5px;
        }
        /* Cambiar fondo del valor seleccionado */
        div[data-baseweb="select"] div[role="button"] {
            background-color: #bcbcbc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Título
    st.markdown(
        """
        <div style="text-align: right; padding-right: 10px;">
            <h3 style="display: inline-block; font-family: 'Source Sans Pro', sans-serif;">🎞️ Select Film</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Selectbox
    selected_film = st.selectbox("", df["film"].unique())

    film_data = df[df["film"] == selected_film].iloc[0]

    # Tarjeta de datos SIN borde, solo con fondo gris claro
    html(
        f"""
        <div style="background-color: #bcbcbc; padding: 15px; border-radius: 12px; color: #333333; text-align: center; font-family: 'Source Sans Pro', sans-serif;">

            <h3 style="color: #1f77b4; margin-bottom: 10px;">{film_data['film'].upper()} ({int(film_data['year'])})</h3>

            <hr style="border: none; height: 1px; background-color: tomato; margin: 10px 0;">

            <h4>📊 CRITICS</h4>
            <p><strong>🍅 Rotten Tomatoes:</strong> {film_data['rotten_tomatoes']}</p>
            <p><strong>🎯 Metacritic:</strong> {film_data['metacritic']}</p>

            <hr style="border: none; height: 1px; background-color: #999; margin: 10px 0;">

            <h4>🎬 AGE RATING</h4>
            <p><strong>{film_data['film_rating']}</strong></p>

            <hr style="border: none; height: 1px; background-color: #999; margin: 10px 0;">

            <h4>⏱️ RUN TIME</h4>
            <p><strong>{film_data['run_time']} mins</strong></p>

            <hr style="border: none; height: 1px; background-color: #999; margin: 10px 0;">

            <h4>💵 ECONOMICS</h4>
            <p><strong>💰 Budget:</strong> $ {film_data['budget']:.1f} M.</p>
            <p><strong>🌎 Box Office:</strong> $ {film_data['box_office_worldwide']:.1f} M.</p>
            <p><strong>📈 Profit Margin:</strong> $ {film_data['profit_margin']:.1f} M.</p>

        </div>
        """,
        height=720,
    )


# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# ---- MAIN ----
render_title()

selected_year, selected_ratings = render_sidebar_filters()

col_left, col_right = st.columns([4, 1])

with col_left:
    render_kpis()
    st.plotly_chart(
        render_filtered_graph(selected_year, selected_ratings, df),
        use_container_width=True,
    )

    # 🚀 Línea divisoria aquí
    st.markdown(
        """
        <hr style="border: none; height: 2px; background-color: #999999; margin: 30px 0;">
        """,
        unsafe_allow_html=True,
    )

with col_right:
    render_film_selector(df)

# Aquí, fuera de las columnas, para que use el ancho completo:
render_additional_charts(df, selected_year)


render_extra_critics_charts(df)
