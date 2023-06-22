from datetime import datetime, timedelta
from models.MVacuna import Vacuna


def calcular_fecha_turno(dias_adicionales):
    fecha_actual = datetime.now()
    fecha_turno = fecha_actual + timedelta(days=dias_adicionales)
    return fecha_turno.strftime("%Y-%m-%d")


def es_menor_4_meses(fecha_nacimiento):
    fecha_actual = datetime.now()

    dif_en_meses = abs((fecha_actual.year - fecha_nacimiento.year)
                       * 12 + (fecha_actual.month - fecha_nacimiento.month))

    return dif_en_meses <= 4


def ha_pasado_1_año_desde_ultima_vacuna(mascota, nombre_vacuna):
    ultima_vacuna = Vacuna.ultima_vacuna(mascota, nombre_vacuna)
    if not ultima_vacuna:
        return False

    fecha_actual = datetime.now()
    fecha_ultima_vacuna = ultima_vacuna.fecha
    diferencia = fecha_actual - fecha_ultima_vacuna

    return diferencia.days >= 365
