import pandas as pd


def limpiar_usuarios(df):
    df_limpio = df.copy()
    
    # 1. Limpieza de la "Llave" para el Merge (Asumiendo que es id_usuario)
    # Esto asegura que si en un CSV es " 123" y en otro es "123", coincidan.
    if "id_usuario" in df_limpio.columns:
        df_limpio["id_usuario"] = df_limpio["id_usuario"].astype(str).str.strip()

    # 2. Filtros de integridad
    df_limpio = df_limpio.dropna(subset=["nombre", "apellido"])
    df_limpio = df_limpio[df_limpio["apellido"].str.strip() != ""]
    df_limpio = df_limpio[(df_limpio["edad"] >= 0) & (df_limpio["edad"] <= 100)]
    df_limpio = df_limpio[df_limpio["email"].str.contains(r"@.*\.", na=False, regex=True)]

    # 3. Estandarización de texto
    df_limpio["genero"] = df_limpio["genero"].replace({
        "M": "Masculino", "F": "Femenino",
        "masculino": "Masculino", "femenino": "Femenino"
    })

    for col in ["ciudad", "departamento", "pais"]:
        if col in df_limpio.columns:
            df_limpio[col] = df_limpio[col].str.strip().str.capitalize()

    # 4. Seguridad y formato final
    df_limpio["password"] = df_limpio["password"].astype(str)
    df_limpio = df_limpio[df_limpio["password"].str.len() >= 3]
    
    return df_limpio.reset_index(drop=True)

def limpiar_cursos(df):
    df_limpio = df.copy()
    
    # 1. Limpieza de columnas y valores nulos iniciales
    df_limpio.columns = df_limpio.columns.str.strip()
    
    # Asegurar que la llave coincida con la de usuarios
    if "id_usuario" in df_limpio.columns:
        df_limpio["id_usuario"] = df_limpio["id_usuario"].astype(str).str.strip()

    df_limpio = df_limpio.replace(["", " ", "null", "None"], pd.NA)
    
    # 2. Formateo de texto
    columnas_texto = ["nombreCurso", "descripcionCurso", "categoria", "dificultad"]
    for col in columnas_texto:
        if col in df_limpio.columns:
            df_limpio[col] = df_limpio[col].astype(str).str.strip()

    # 3. Reglas de negocio
    df_limpio["dificultad"] = df_limpio["dificultad"].replace({
        "medio": "intermedio",
        "basico": "básico",
        "avanzado": "avanzado"
    })

    df_limpio["numeroNiveles"] = pd.to_numeric(df_limpio["numeroNiveles"], errors="coerce")
    df_limpio = df_limpio[(df_limpio["numeroNiveles"] >= 1) & (df_limpio["numeroNiveles"] <= 10)]
    
    # 4. Eliminar nulos en campos críticos
    df_limpio = df_limpio.dropna(subset=["nombreCurso", "numeroNiveles"])

    # Estandarizar nombres de cursos específicos
    df_limpio["nombreCurso"] = df_limpio["nombreCurso"].str.lower().replace({
        "fundamentos java": "fundamentos de java",
        "spring boot avanzado": "spring boot avanzado",
        "arquitectura microservicios spring cloud": "arquitectura de microservicios con spring cloud"
    })

    return df_limpio.reset_index(drop=True)
