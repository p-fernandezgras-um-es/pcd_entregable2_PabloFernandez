from entregable_2 import *
import random
import datetime

#creamos una clase auxiliar para generar datos de ejemplo
class Generar_datos():

    def __init__(self):
        self.fecha="12/05/2004"
        self.hora_inicio = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
        self.hora_actual = self.hora_inicio
    def obtener_hora(self):
        # Incrementa el tiempo en 5 segundos
        self.hora_actual += datetime.timedelta(seconds=5)
        # Formatea la hora como "dia:hora:segundo"
        hora = self.hora_actual.strftime("%d:%H:%M:%S")
        return hora
# La temperatura más común de un invernadero se encuentra entre los 18º y 24º por lo que creamos datos que se alejen  como mucho 5º de este intervalo. 

    def temperatura(self):
        return round(random.uniform(13,29),1)

    def nuevo_dato(self):
        return f"{self.fecha} {self.obtener_hora()}, {self.temperatura()}"

#Obtenemos la clase sistema
sistema=Sistema.obtener_instancia()

#Instanciamos la clase sensor
sensor=Observable_Sensor("Sensor Invernadero")

#Añadimos como observador del sensor al sistema
sensor.añadir_observer(sistema)

#Instanciamos las operaciones a realizar
calcular_estadisticos=Calcular_estadisticos()
supera_umbral=Supera_umbral()
aumento_brusco=Aumento_brusco()
calcular_estadisticos.set_proxima_operacion(supera_umbral)
supera_umbral.set_proxima_operacion(aumento_brusco)

#Instaciamos el problema a resolver
problema=Operaciones(Paso)

continuar=False
respuesta=input(f"\33[92mSi desea encender el sensor pulse *1*\033[0m")
if respuesta=="1":
    continuar=True

#creamos la clase para generar datos
generar_datos=Generar_datos()

while continuar:
    respuesta=input(f"\033[94m¿Que estadístico desea calcular los próximos 2 minutos?\n1:Media y desviación típica.\n2:Cuantiles.\n3:Máximo y mínimo.\033[0m")
    if respuesta=="2":
        calcular_estadisticos.cambiar_estadistico(Media)
    if respuesta=="2":
        calcular_estadisticos.cambiar_estadistico(Cuantiles)
    elif respuesta=="3":
        calcular_estadisticos.cambiar_estadistico(MaxMin)
    
    for i in range(24):
        dato=generar_datos.nuevo_dato()
        sensor.nuevo_dato(Datos(dato))
        calcular_estadisticos.realizar_operacion(problema,sistema)

    respuesta=input(f"\033[94m--------------------------------------------------------\n¿Desea mantener el sensor dos minutos más?\n1:Si\n2:No\033[0m")
    if respuesta=="2":
        continuar=False
    