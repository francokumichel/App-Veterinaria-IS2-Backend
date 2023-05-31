from datetime import datetime, timedelta


def calcular_fecha_turno(dias_adicionales):
    fecha_actual = datetime.now()
    fecha_turno = fecha_actual + timedelta(days=dias_adicionales)
    return fecha_turno.strftime("%Y-%m-%d")


def es_menor_4_meses(fecha_nacimiento):
    fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    fecha_actual = datetime.strptime(datetime.now(), "%Y-%m-%d")

    dif_en_meses = abs((fecha_actual.year - fecha_nacimiento.year)
                       * 12 + (fecha_actual.month - fecha_nacimiento.month))

    return dif_en_meses <= 4
