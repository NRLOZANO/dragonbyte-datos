from analisis import (
    usuarios_limpio,
    cursos_limpio
)


def probar_carga_y_limpieza():
    dfs = {
        "USUARIOS":usuarios_limpio(),
        "CURSOS": cursos_limpio()
    }

    for nombre, df in dfs.items():
        print(f"\n{'='*50}")
        print(f"  {nombre}  ({df.shape[0]} filas, {df.shape[1]} columnas)")
        print(f"{'='*50}")
        print(df.to_string(index=False))


if __name__ == "__main__":
    probar_carga_y_limpieza()