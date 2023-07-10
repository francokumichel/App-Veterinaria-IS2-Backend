from datetime import datetime, timedelta
from datetime import date


def calcular_fecha_turno(dias_adicionales):
    fecha_actual = datetime.now()
    fecha_turno = fecha_actual + timedelta(days=dias_adicionales)
    return fecha_turno.strftime("%Y-%m-%d")


def es_menor_4_meses(fecha_nacimiento):
    fecha_actual = datetime.now()

    dif_en_meses = abs((fecha_actual.year - fecha_nacimiento.year)
                       * 12 + (fecha_actual.month - fecha_nacimiento.month))

    return dif_en_meses <= 4

def es_menor_1_anio(fecha_nacimiento):
    return (date.today() - fecha_nacimiento).days < 365

def ha_pasado_1_año_desde_ultima_vacuna(mascota, nombre_vacuna):
    # Si no tiene vacunas, devuelvo true
    if not mascota.vacunas:
        return True

    vacunas_ordenadas = sorted((vacuna for vacuna in mascota.vacunas if vacuna.nombre.lower() ==
                               nombre_vacuna.lower()), key=lambda vacuna: vacuna.fecha, reverse=True)
    # Verifico si existen vacunas con el nombre pasado por parámetro
    if not vacunas_ordenadas:
        return True

    ultima_vacuna = vacunas_ordenadas[0]
    fecha_actual = datetime.now()
    fecha_ultima_vacuna = ultima_vacuna.fecha
    diferencia = fecha_actual - fecha_ultima_vacuna

    return diferencia.days >= 365
