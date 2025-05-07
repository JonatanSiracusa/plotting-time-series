import plotly.io as pio
import plotly.graph_objects as go

# 1. Paleta de colores estilo Bloomberg (básica y extendida)
BLOOMBERG_COLORS = [
    "#00FF00",  # verde flúo
    "#FF8000",  # naranja
    "#1E90FF",  # azul Bloomberg
    "#FF0000",  # rojo
    "#FFFF00",  # amarillo
    "#00FFFF",  # celeste
    "#FF00FF",  # magenta
    "#FFFFFF",  # blanco
    "#7FFF00",  # verde claro
    "#FF1493",  # rosa fuerte
    "#20B2AA",  # turquesa
    "#FFD700",  # dorado
    "#ADFF2F",  # verde lima
    "#DC143C",  # rojo carmesí
]


# 2. Funciones para manejar colores
def get_color(index):
    """Devuelve un color de la paleta extendida ciclando si se pasa el largo."""
    return BLOOMBERG_COLORS[index % len(BLOOMBERG_COLORS)]


BLOOMBERG_COLOR_SCALE = [
    "px.colors.sequential.Viridis",
    "plotly3",  # naranja
    "blackbody",  # azul Bloomberg
    "cividis",  # rojo
    "inferno",  # amarillo
    "magma",  # celeste
]

def get_colorscale(index):
    """Devuelve un color de la paleta de colorscale ciclando si se pasa el largo."""
    return BLOOMBERG_COLOR_SCALE[index % len(BLOOMBERG_COLOR_SCALE)]

# 3. Template oscuro estilo Bloomberg
bloomberg_dark_template = go.layout.Template(
    layout=dict(
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E",
        font=dict(
            family="Calibri, sans-serif",
            size=14,
            color="white"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#2E2E2E",
            zeroline=False,
            showline=True,
            linecolor="#2E2E2E",
            tickfont=dict(size=12),
            # titlefont=dict(size=16),
            title=dict(font=dict(size=16)),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#2E2E2E",
            zeroline=False,
            showline=True,
            linecolor="#2E2E2E",
            tickfont=dict(size=12),
            # titlefont=dict(size=16),
            title=dict(font=dict(size=16)),
        ),
        legend=dict(
            bgcolor="rgba(40,40,40,0.7)",
            bordercolor="#3A3A3A",
            borderwidth=1,
            font=dict(size=12),
        ),
        title=dict(
            font=dict(
                size=22,
                color="white"
            ),
            x=0.5,
            xanchor="center",
            yanchor="top",
        )
    )
)

# 4. Template claro estilo Bloomberg
bloomberg_light_template = go.layout.Template(
    layout=dict(
        paper_bgcolor="#F7F7F7",
        plot_bgcolor="#F7F7F7",
        font=dict(
            family="Calibri, sans-serif",
            size=14,
            color="#000000"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#CCCCCC",
            zeroline=False,
            showline=True,
            linecolor="#CCCCCC",
            tickfont=dict(size=12),
            title=dict(font=dict(size=16)),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#CCCCCC",
            zeroline=False,
            showline=True,
            linecolor="#CCCCCC",
            tickfont=dict(size=12),
            title=dict(font=dict(size=16)),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="#CCCCCC",
            borderwidth=1,
            font=dict(size=12),
        ),
        title=dict(
            font=dict(
                size=22,
                color="#000000"
            ),
            x=0.5,
            xanchor="center",
            yanchor="top",
        )
    )
)

# 5. Registrar los templates
pio.templates["bloomberg_dark"] = bloomberg_dark_template
pio.templates["bloomberg_light"] = bloomberg_light_template

# 6. Funciones para setear templates rápidamente
def set_bloomberg_dark(fig):
    fig.update_layout(template="bloomberg_dark")
    return fig

def set_bloomberg_light(fig):
    fig.update_layout(template="bloomberg_light")
    return fig

# 7. Mini ayuda para saber qué hay
TEMPLATES_BLOOMBERG = ["bloomberg_dark", "bloomberg_light"]
