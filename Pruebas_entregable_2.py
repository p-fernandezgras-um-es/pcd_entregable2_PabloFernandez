from entregable_2 import *

datos=[
("2024-01-17 00:00:00, 25.5"),
("2024-01-17 01:00:00, 24.8"),
("2024-01-17 02:00:00, 23.9"),
("2024-01-17 03:00:00, 22.7"),
("2024-01-17 04:00:00, 21.3"),
("2024-01-17 05:00:00, 20.1"),
("2024-01-17 06:00:00, 19.8"),
("2024-01-17 07:00:00, 20.5"),
("2024-01-17 08:00:00, 21.9")]
sistema=Sistema.obtener_instancia()
sensor=Observable_Sensor("Sensor")
sensor.añadir_observer(sistema)
for i in datos:
    sensor.nuevo_dato(Datos(i))

calcular_estadisticos=Calcular_estadisticos()
supera_umbral=Supera_umbral()
aumento_brusco=Aumento_brusco()

calcular_estadisticos.set_proxima_operacion(supera_umbral)
supera_umbral.set_proxima_operacion(aumento_brusco)
problema=Operaciones(Paso)
calcular_estadisticos.realizar_operacion(problema,sistema)