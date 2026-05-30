import pandas as pd
from analisis import limpiar_cursos, limpiar_usuarios


def usuarios_con_cursos() -> pd.DataFrame:
    usuarios_raw = pd.read_csv("data/raw/usuarios.csv")
    cursos_raw = pd.read_csv("data/raw/cursos.csv")
    usuarios = limpiar_usuarios(usuarios_raw)
    cursos = limpiar_cursos(cursos_raw)
    return pd.merge(
        usuarios,
        cursos,
        on="idUsuarios",
        how="left",
        suffixes=("_usuarios", "_cursos"),
    )
