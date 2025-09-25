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




