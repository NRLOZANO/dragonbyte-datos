from merge import (
    usuarios_con_cursos
)


def probar_merges():
    merges = {
        "USUARIOS  ←→  CURSOS":          usuarios_con_cursos,
    }

    for nombre, fn in merges.items():
        print(f"\n{'='*55}")
        print(f"  {nombre}")
        print(f"{'='*55}")
        try:
            df = fn()
            print(f"  {df.shape[0]} filas  |  {df.shape[1]} columnas")
            print(f"  Columnas: {list(df.columns)}\n")
            print(df.to_string(index=False))
        except Exception as e:
            print(f"  [ERROR] {type(e).__name__}: {e}")


if __name__ == "__main__":
    probar_merges()
