from entregable_2 import *


### Hacemos unos tests unitarios para ver el correcto funcionamiento de las clases.
def test_calcular_estadistico_media():
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
    temperaturas=[25.5, 24.8, 23.9, 22.7, 21.3, 20.1, 19.8, 20.5, 21.9]
    sistema=Sistema.obtener_instancia()
    sensor=Observable_Sensor("Sensor")
    sensor.añadir_observer(sistema)
    for i in datos:
        sensor.nuevo_dato(Datos(i))
    print(sistema.temperaturas())
    estadistico=Calcular_estadisticos()
    pasos=Paso
    #como el estadistico se ha dejado por defecto corresponde a la media
    assert estadistico._operar(pasos,sistema)[0] ==np.mean(temperaturas)
    assert round(estadistico._operar(pasos,sistema)[1]) ==round(np.std(temperaturas))

def test_calcular_estadistico_cuantiles():
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
    temperaturas=[25.5, 24.8, 23.9, 22.7, 21.3, 20.1, 19.8, 20.5, 21.9]
    sistema=Sistema.obtener_instancia()
    sensor=Observable_Sensor("Sensor")
    sensor.añadir_observer(sistema)
    for i in datos:
        sensor.nuevo_dato(Datos(i))
    print(sistema.temperaturas())
    estadistico=Calcular_estadisticos()
    estadistico.cambiar_estadistico(Cuantiles)
    pasos=Paso
    
    assert round(estadistico._operar(pasos,sistema)[0]) ==round(np.quantile(temperaturas,0.25))
    assert round(estadistico._operar(pasos,sistema)[1]) ==round(np.quantile(temperaturas,0.5))
    assert round(estadistico._operar(pasos,sistema)[2]) ==round(np.quantile(temperaturas,0.75))

def test_calcular_estadistico_maxmin():
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
    temperaturas=[25.5, 24.8, 23.9, 22.7, 21.3, 20.1, 19.8, 20.5, 21.9]
    sistema=Sistema.obtener_instancia()
    sensor=Observable_Sensor("Sensor")
    sensor.añadir_observer(sistema)
    for i in datos:
        sensor.nuevo_dato(Datos(i))
    print(sistema.temperaturas())
    estadistico=Calcular_estadisticos()
    estadistico.cambiar_estadistico(MaxMin)
    pasos=Paso

    assert estadistico._operar(pasos,sistema)[0] ==np.max(temperaturas)
    assert estadistico._operar(pasos,sistema)[1] ==np.min(temperaturas)


def test_supera_umbral():
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
    temperaturas=[25.5, 24.8, 23.9, 22.7, 21.3, 20.1, 19.8, 20.5, 21.9]
    sistema=Sistema.obtener_instancia()
    sensor=Observable_Sensor("Sensor")
    sensor.añadir_observer(sistema)
    for i in datos:
        sensor.nuevo_dato(Datos(i))
    print(sistema.temperaturas())
    estadistico=Supera_umbral()
    pasos=Paso

    assert estadistico._operar(pasos,sistema) ==False

def test_aumento_brusco():
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
    temperaturas=[25.5, 24.8, 23.9, 22.7, 21.3, 20.1, 19.8, 20.5, 21.9]
    sistema=Sistema.obtener_instancia()
    sensor=Observable_Sensor("Sensor")
    sensor.añadir_observer(sistema)
    for i in datos:
        sensor.nuevo_dato(Datos(i))
    print(sistema.temperaturas())
    estadistico=Aumento_brusco()
    pasos=Paso

    assert estadistico._operar(pasos,sistema) ==False
