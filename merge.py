import pandas as pd
from carga import get_cursos, get_usuarios
from analisis import limpiar_cursos, limpiar_usuarios


def usuarios_con_cursos() -> pd.DataFrame:
    usuarios = limpiar_usuarios(get_usuarios())
    cursos = limpiar_cursos(get_cursos())
    return pd.merge(
        usuarios,
        cursos,
        left_on="id",
        right_on="id",
        how="left",
        suffixes=("_usuarios", "_cursos"),
    )
