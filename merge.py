import pandas as pd
from analisis import limpiar_cursos, limpiar_usuarios, pacientes_limpio, medicos_limpio, prescripciones_limpio

# ─────────────────────────────────────────────
# Carga de DataFrames limpios
# ─────────────────────────────────────────
usuarios = limpiar_usuarios()
cursos = limpiar_cursos()


def usuarios_con_cursos() -> pd.DataFrame:
    return pd.merge(
        usuarios,
        cursos,
        left_on="id",
        right_on="id",
        how="left",
        suffixes=("_usuarios", "_cursos"),
    )
