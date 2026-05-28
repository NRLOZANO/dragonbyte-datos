from io import BytesIO
import base64
import matplotlib
matplotlib.use("Agg")  # Backend sin pantalla, OBLIGATORIO para que FastAPI no se cuelgue
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns

# Importamos la función de unión desde el archivo merge.py
from merge import usuarios_con_cursos

# ════════════════════════════════════════════════════════
# HERRAMIENTAS DE CONVERSIÓN (RAM y Base64)
# ════════════════════════════════════════════════════════

def _fig_to_bytes(fig: Figure) -> bytes:
    """Convierte la gráfica en bytes puros para los endpoints PULL."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()

def _fig_to_base64(fig: Figure) -> dict:
    """Convierte la gráfica en una cadena de texto Base64 para endpoints HEADLESS."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return {"mime_type": "image/png", "imagen_base64": img_b64}


# ════════════════════════════════════════════════════════
# TUS FUNCIONES DE ANÁLISIS (Adaptadas para responder texto a la API)
# ════════════════════════════════════════════════════════

def analizar_usuarios():
    df = usuarios_con_cursos()
    if df is None or df.empty: 
        return {"error": "No hay datos de usuarios para analizar."}

    return {
        "titulo": "ANÁLISIS DE USUARIOS",
        "metricas_edad": {
            "edad_promedio": round(float(df['edad'].mean()), 2),
            "usuario_mas_joven": int(df['edad'].min()),
            "usuario_mayor": int(df['edad'].max())
        },
        "distribucion_genero": df['genero'].value_counts().to_dict(),
        "top_ciudades": df['ciudad'].value_counts().head(5).to_dict()
    }

def analizar_cursos():
    df = usuarios_con_cursos()
    if df is None or df.empty:
        return {"error": "No hay datos de cursos para analizar."}

    try:
        dificultad_top = df['dificultad'].mode()[0]
    except IndexError:
        dificultad_top = "No determinada"

    return {
        "titulo": "ANÁLISIS DE CURSOS",
        "promedio_niveles": round(float(df['numeroNiveles'].mean()), 1),
        "cursos_por_categoria": df['categoria'].value_counts().to_dict(),
        "dificultad_mas_comun": dificultad_top.lower()
    }


# ════════════════════════════════════════════════════════
# DIBUJO INTERNO DE LAS GRÁFICAS (Sin usar plt.show)
# ════════════════════════════════════════════════════════

def crear_grafico_top_ciudades(df) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    top_5_ciudades = df['ciudad'].value_counts().head(5)
    sns.barplot(x=top_5_ciudades.index, y=top_5_ciudades.values, palette='viridis', ax=ax)
    
    ax.set_title('Top 5 Ciudades con Más Usuarios', fontsize=16)
    ax.set_xlabel('Ciudad', fontsize=12)
    ax.set_ylabel('Cantidad de Usuarios', fontsize=12)
    ax.set_xticklabels(top_5_ciudades.index, rotation=45)
    fig.tight_layout()
    return fig

def crear_grafico_dificultad_cursos(df, top_n: int = 5) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    df_copy = df.copy()
    df_copy['dificultad'] = df_copy['dificultad'].str.lower()
    orden = df_copy['dificultad'].value_counts().head(top_n).index
    
    sns.countplot(data=df_copy, x='dificultad', palette='magma', order=orden, ax=ax)
    ax.set_title('Dificultad de Cursos Más Común', fontsize=16)
    ax.set_xlabel('Nivel de Dificultad', fontsize=12)
    ax.set_ylabel('Frecuencia', fontsize=12)
    fig.tight_layout()
    return fig


# ════════════════════════════════════════════════════════
# ENVOLTORIOS FINALES (Lo que exportamos al microservicio)
# ════════════════════════════════════════════════════════


def headless_usuarios_por_curso():
    df = usuarios_con_cursos()
    fig = crear_grafico_top_ciudades(df)
    return _fig_to_base64(fig)

def headless_cursos_mas_populares(top: int = 5):
    df = usuarios_con_cursos()
    fig = crear_grafico_dificultad_cursos(df, top_n=top)
    return _fig_to_base64(fig)

def pull_usuarios_por_curso():
    df = usuarios_con_cursos()
    fig = crear_grafico_top_ciudades(df)
    return _fig_to_bytes(fig)

def pull_cursos_mas_populares(top: int = 5):
    df = usuarios_con_cursos()
    fig = crear_grafico_dificultad_cursos(df, top_n=top)
    return _fig_to_bytes(fig)