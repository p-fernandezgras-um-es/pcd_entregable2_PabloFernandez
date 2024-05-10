from abc import ABC, abstractmethod
import numpy as np
from functools import reduce
from enum import IntEnum
from functools import reduce
from math import sqrt


#Creamos una clase para almacenar los datos del sensor
class Datos:
    def __init__(self,tupla) -> tuple:

        timestamp,temperatura=tupla.split(",")
        self.temperatura=float(temperatura)
        self.dia,self.hora=timestamp.split(" ")


## R1: Singleton
#Como dice el enunciado utilizamos el patrón singleton para que solamente pueda haber una instancia del sistema.
class Sistema:
    _unicaInstancia = None

    def __init__(self):
        self.datos=[]
        self.umbral=30
    #función para cambiar el umbral de temperatura
    def cambiar_umbral(self,umbral:float):
        self.umbral=umbral

    #función que almacena las temperaturas de los datos
    def temperaturas(self):
        temperaturas=[]
        for dato in self.datos:
            temperaturas.append(dato.temperatura)
        return temperaturas

    #función para instanciar el sistema
    @classmethod
    def obtener_instancia(cls):
        if not cls._unicaInstancia :
            cls._unicaInstancia = cls()
        return cls._unicaInstancia
    
    #función para añadir datos al sistema
    def actualizar(self,dato):
        self.datos.append(dato)


    
## R2: Observer
#Utilizamos el patrón Observer para recibir actualizaciones de los datos en tiempo real y procesarlos adecuadamente.  
class Observable_Sensor:

    def __init__(self,nombre) -> None:
        self._nombre=nombre
        self.observers=[]

    #funcion para añadir observadores
    def añadir_observer(self,observer):

        self.observers.append(observer)

    #funcion para eliminar observadores
    def eliminar_observer(self,observer):

        self.observers.remove(observer)

    #funcion para enviar datos a los observadores
    def nuevo_dato(self,dato):
        for observers in self.observers:
            observers.actualizar(dato)

## R3 Chain of responsability
#Utilizamos el patrón Chain of responsability para la realización de una serie de pasos encadenados.

#Definimos una clase Paso para almacenar los pasos que debe seguir el sistema.
class Paso(IntEnum):
    Fin="0"
    Calcular_estadisticos="1"
    Supera_umbral="2"
    Aumento_brusco="3"

#Definimos la clase Operaciones para instanciar una operación indicandole los pasos que debe seguir.
class Operaciones():
    def __init__(self,pasos:Paso) -> None:
        self.pasos=pasos
    
    def terminado(self) ->bool:
        return self.pasos==Paso.Fin
    
#La clase Manejador como su nombre indica maneja el funcionamiento de las operaciones y establece sus prioridades.
class Manejador(ABC):
    def __init__(self) -> None:
        self._proxima_operacion : Manejador
        self._paso_actual : Paso
    
    def set_paso(self,paso:Paso):
        self.paso_actual = paso
    
    #clase para indicar que operación se realizará después.
    def set_proxima_operacion(self,operacion):
        self._proxima_operacion=operacion
    
    #clase para realizar la operación establecida.
    def realizar_operacion(self,operaciones:Operaciones,datos):
        if self._paso_actual==(operaciones.pasos and self._paso_actual):
            self._operar(operaciones,datos)
        
        if (operaciones.terminado() or self._proxima_operacion==None):
            return
        else:
            self._proxima_operacion.realizar_operacion(operaciones,datos)

    #método abstracto que deben implementar las clases hijas para realizar las operaciones.
    @abstractmethod 
    def _operar(self,operacion:Operaciones,datos):
        raise NotImplementedError

#clase para calcular el estadístico indicado. 
class Calcular_estadisticos(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Calcular_estadisticos
        self._proxima_operacion = None
        # Asignamos el estadístico media por defecto.
        self.context=Context(Media)
    
    # Función para cambiar el estadístico.
    def cambiar_estadistico(self,estadistico):
        self.context.seleccionar_estadistico(estadistico)
    
    #función para calcular el estadístico
    def _operar(self,operacion: Operaciones,sistema:Sistema):
        print("Calculando estadisticos:")
        return self.context.aplicar(sistema)
    
#clase para comprobar si la temperatura actual supera el umbral establecido por el sistema. 
class Supera_umbral(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Supera_umbral
        self._proxima_operacion = None
    
    #función para realizar la comprobación.
    def _operar(self, operacion: Operaciones,sistema:Sistema):
        supera_umbral=False
        print(f"--------------------------------------------------------\nComprobando si la temperatura supera el umbral de {sistema.umbral}ºC:")
        if sistema.datos[-1].temperatura > sistema.umbral:
            supera_umbral=True
            print(f"¡¡¡PELIGRO!!!")
            print(f"La temperatura el dia {sistema.datos[-1].dia} a las {sistema.datos[-1].hora} es de {sistema.datos[-1].temperatura} y supera el umbral de {sistema.umbral}ºC")
        else:
            print(f"Temperatura en orden: {sistema.datos[-1].temperatura}ºC")
        return supera_umbral

# clase para comprobar si la temperatura aumenta más de 10ºC en los últimos 30 segundos.
class Aumento_brusco(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Aumento_brusco
        self._proxima_operacion = None
    
    #funcion para realizar la comprobación.
    def _operar(self, operacion:Operaciones,sistema:Sistema):
        print("--------------------------------------------------------\nComprobando si la temperatura ha aumentado más de 10ºC en los últimos 30 segundos:")
        aumenta=False
        #comprobamos si hay datos de los últimos 30 segundos antes de realizar la resta.
        if len(sistema.temperaturas())>=6:
            if (sistema.temperaturas()[-1] - sistema.temperaturas()[-6]) > 10:
                aumenta=True
                print(f"De la hora {sistema.datos[-6].hora} a la hora {sistema.datos[-6].hora} del día {sistema.datos[-6].dia} ha aumentado la temperatura más de 10ºC ({sistema.datos[-1].temperatura - sistema.datos[-6].temperatura}ºC)")
            else:
                print(f"Temperatura en orden, no ha aumentado más de 10ºC en los últimos 30 segundos")
        
        else:
            print("Todavía no hay datos de lo últimos 30 segundos")
        return aumenta

## R4: Strategy
#Utilizamos el patrón Strategy para tener diferentes estrategias para computar los estadísticos.

#clase Context para establecer el estadístico y para aplicarlo.
class Context:
    def __init__(self,estadistico) -> None:
        self.estadistico=estadistico

    #funcion para seleccionar el estadístico.
    def seleccionar_estadistico(self,estadistico):
        self.estadistico=estadistico
    #funcion para aplicar el estadístico.
    def aplicar(self,sistema:Sistema):
        return self.estadistico.calcular_estadistico(self.estadistico,sistema)

#clase abstracta para crear estadísticos.
class Estadistico(ABC):

    #método abstracto que deben implementar las clases hijas para calcular el estadístico.
    @abstractmethod
    def calcular_estadistico(self,sistema:Sistema):
        pass

#clase para calcular la media y la desviación típica de la temperatura en los 60 últimos segundos.
class Media(Estadistico):
    
    #función para calcular es estadístico.
    def calcular_estadistico(self,sistema:Sistema):
        # calculamos la media y la desviación típica haciendo uso de la programación funcional.
        media= reduce(lambda x, y: x + y, sistema.temperaturas()[-12:]) / len(sistema.temperaturas()[-12:])
        dt=sqrt(sum((x - media) ** 2 for x in sistema.temperaturas()) / len(sistema.temperaturas()))

        print(f"La temperatura media en los últimos 60 segundos es de: {round(media,2)}ºC y la deviación típica es de {round(dt,2)}ºC.")
        
        return media,dt
    
#clase para calcular los cuantiles de la temperatura.
class Cuantiles(Estadistico):

    #función para calcular es estadístico.
    def calcular_estadistico(self, sistema: Sistema):
        # Utilizamos la funcion np.quantile para calcular los diferentes cuantiles,
        primer_cuantil=np.quantile(0.25,sistema.temperaturas())
        segundo_cuantil=np.quantile(0.5,sistema.temperaturas())
        tercer_cuantil=np.quantile(0.75,sistema.temperaturas())

        print(f"Primer cuantil: {primer_cuantil}ºC.\nSegundo cuantil: {segundo_cuantil}ºC.\nTercer cuantil: {tercer_cuantil}ºC.")

        return primer_cuantil,segundo_cuantil,tercer_cuantil

#clase para encontrar la temperatura máxima y mínima en los últimos 60 segundos.
class MaxMin(Estadistico):

    #función para calcular es estadístico.
    def calcular_estadistico(self, sistema: Sistema):
        #Hallamos la temperatura máxima y mínima utilizando la programación funcional.
        t_max=reduce(lambda a, b: a if a > b else b, sistema.temperaturas()[-12:])
        t_min=reduce(lambda a, b: a if a < b else b, sistema.temperaturas()[-12:])

        print(f"Temperatura máxima y mínima alcanzada en los últimos 60 segundos:\nTemperatura máxima: {t_max}ºC\nTemperatura máxima: {t_min}ºC")
        return t_max,t_min