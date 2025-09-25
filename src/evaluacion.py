def puntos_equipo_ronda(stats):
    """
    Calcula el puntaje de una ronda para un equipo.
    stats: dict con 'innovacion' (int), 'presentacion' (int), 'errores' (bool)
    return: int
    """
    base = 3 * stats['innovacion'] + stats['presentacion']
    penalizacion = 1 if stats['errores'] else 0  # bool -> int
    return base - penalizacion


def calcular_puntajes_ronda(ronda_dict):
    """
    Transforma la ronda a un dict equipo -> métricas de ronda (incluye puntos).
    ronda_dict: dict equipo -> {'innovacion', 'presentacion', 'errores'}
    return: dict equipo -> {'pts','innovacion','presentacion','errores'}
    """
    def transformar(par):
        equipo, stats = par
        pts = puntos_equipo_ronda(stats)
        err = 1 if stats['errores'] else 0
        return (equipo, {
            'pts': pts,
            'innovacion': stats['innovacion'],
            'presentacion': stats['presentacion'],
            'errores': err
        })
    return dict(map(transformar, ronda_dict.items()))


def mejores_de_ronda(puntajes_ronda):
    """
    Devuelve lista con los equipos que empatan el máximo de puntos en la ronda.
    puntajes_ronda: dict equipo -> {'pts': int, ...}
    """
    max_pts = max(valor['pts'] for valor in puntajes_ronda.values())
    return list(filter(
        lambda eq: puntajes_ronda[eq]['pts'] == max_pts,
        puntajes_ronda.keys()
    ))


def inicializar_acumulado(equipos):
    """
    Crea el acumulador por equipo.
    equipos: iterable de nombres de equipo
    return: dict equipo -> totales
    """
    acum = {}
    for eq in equipos:
        acum[eq] = {
            'innovacion': 0,
            'presentacion': 0,
            'errores': 0,
            'mejores': 0,
            'puntos': 0
        }
    return acum


def actualizar_acumulado(acum, puntajes_ronda, mejores):
    """
    Suma al acumulado los valores de la ronda y marca MER.
    """
    for eq, dato in puntajes_ronda.items():
        acum[eq]['innovacion']   += dato['innovacion']
        acum[eq]['presentacion'] += dato['presentacion']
        acum[eq]['errores']      += dato['errores']
        acum[eq]['puntos']       += dato['pts']
        if eq in mejores:
            acum[eq]['mejores']  += 1


def ordenar_por_puntos(acum):
    """Ordena desc por puntos."""
    return sorted(acum.items(), key=lambda par: par[1]['puntos'], reverse=True)


def imprimir_tabla(acum):
    """Muestra la tabla ordenada de resultados."""
    ordenados = ordenar_por_puntos(acum)
    print("Equipo  Innovación  Presentación  Errores  Mejores  Puntos")
    for eq, d in ordenados:
        print(f"{eq:<7} {d['innovacion']:^11} {d['presentacion']:^13} {d['errores']:^7} {d['mejores']:^7} {d['puntos']:^6}")


# ===== Runner: ejecuta todo si se llama como script =====
def _puntaje(r):
    # 3*innovación + 1*presentación - 1 si hubo errores
    return 3 * r["innovacion"] + r["presentacion"] - (1 if r["errores"] else 0)

if __name__ == "__main__":
    evaluaciones = [
        {  # Ronda 1
            "EquipoA": {"innovacion": 2, "presentacion": 1, "errores": True},
            "EquipoB": {"innovacion": 1, "presentacion": 0, "errores": False},
            "EquipoC": {"innovacion": 1, "presentacion": 2, "errores": True},
            "EquipoD": {"innovacion": 0, "presentacion": 1, "errores": False},
            "EquipoE": {"innovacion": 1, "presentacion": 1, "errores": False},
        },
        {  # Ronda 2
            "EquipoA": {"innovacion": 0, "presentacion": 2, "errores": False},
            "EquipoB": {"innovacion": 2, "presentacion": 0, "errores": True},
            "EquipoC": {"innovacion": 1, "presentacion": 1, "errores": False},
            "EquipoD": {"innovacion": 2, "presentacion": 1, "errores": True},
            "EquipoE": {"innovacion": 0, "presentacion": 1, "errores": False},
        },
        {  # Ronda 3
            "EquipoA": {"innovacion": 3, "presentacion": 2, "errores": False},
            "EquipoB": {"innovacion": 1, "presentacion": 1, "errores": True},
            "EquipoC": {"innovacion": 2, "presentacion": 0, "errores": False},
            "EquipoD": {"innovacion": 1, "presentacion": 3, "errores": True},
            "EquipoE": {"innovacion": 2, "presentacion": 2, "errores": False},
        },
        {  # Ronda 4
            "EquipoA": {"innovacion": 1, "presentacion": 3, "errores": True},
            "EquipoB": {"innovacion": 2, "presentacion": 2, "errores": False},
            "EquipoC": {"innovacion": 3, "presentacion": 1, "errores": False},
            "EquipoD": {"innovacion": 0, "presentacion": 2, "errores": True},
            "EquipoE": {"innovacion": 2, "presentacion": 0, "errores": False},
        },
        {  # Ronda 5
            "EquipoA": {"innovacion": 2, "presentacion": 2, "errores": False},
            "EquipoB": {"innovacion": 1, "presentacion": 3, "errores": True},
            "EquipoC": {"innovacion": 0, "presentacion": 2, "errores": False},
            "EquipoD": {"innovacion": 3, "presentacion": 1, "errores": False},
            "EquipoE": {"innovacion": 2, "presentacion": 3, "errores": True},
        },
    ]

    # Acumulados por equipo
    stats = {}
    for ronda_idx, ronda in enumerate(evaluaciones, start=1):
        # Inicializar equipos
        for eq in ronda:
            if eq not in stats:
                stats[eq] = {
                    "innovacion": 0,
                    "presentacion": 0,
                    "errores": 0,
                    "mejores": 0,
                    "puntos": 0,
                }

        # Puntajes de la ronda
        puntajes_ronda = {eq: _puntaje(datos) for eq, datos in ronda.items()}
        max_puntos = max(puntajes_ronda.values())
        ganadores = [eq for eq, p in puntajes_ronda.items() if p == max_puntos]

        # Actualizar acumulados
        for eq, datos in ronda.items():
            stats[eq]["innovacion"] += datos["innovacion"]
            stats[eq]["presentacion"] += datos["presentacion"]
            stats[eq]["errores"] += 1 if datos["errores"] else 0
            stats[eq]["puntos"] += puntajes_ronda[eq]
        for eq in ganadores:
            stats[eq]["mejores"] += 1

        # Ranking (descendente por puntos)
        ranking = sorted(stats.items(), key=lambda it: it[1]["puntos"], reverse=True)

        # Mostrar ronda
        print(f"Ronda {ronda_idx}")
        print(f"Mejor(es) equipo(s): {', '.join(ganadores)} — puntos: {max_puntos}")
        print("Equipo  Innovación  Presentación  Errores  Mejores  Puntos")
        for eq, s in ranking:
            print(
                f"{eq:<7} {s['innovacion']:>6} {s['presentacion']:>12} {s['errores']:>9} {s['mejores']:>8} {s['puntos']:>7}"
            )
        print()

    # Final
    max_final = max(s["puntos"] for s in stats.values())
    ganadores_finales = [eq for eq, s in stats.items() if s["puntos"] == max_final]
    print("Resultados Finales")
    print(f"Equipos Ganadores: {', '.join(ganadores_finales)} ({max_final} puntos)\n")
    print("Tabla Final de Resultados")
    print("Equipo  Innovación  Presentación  Errores  Mejores  Puntos")
    for eq, s in sorted(stats.items(), key=lambda it: it[1]["puntos"], reverse=True):
        print(
            f"{eq:<7} {s['innovacion']:>6} {s['presentacion']:>12} {s['errores']:>9} {s['mejores']:>8} {s['puntos']:>7}"
        )

