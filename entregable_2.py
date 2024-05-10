from abc import ABC, abstractmethod
import numpy as np
from functools import reduce
from enum import IntEnum
from functools import reduce
from math import sqrt

class Datos:
    def __init__(self,tupla) -> tuple:

        timestamp,temperatura=tupla.split(",")
        self.temperatura=float(temperatura)
        self.dia,self.hora=timestamp.split(" ")


## R1: Singleton
class Sistema:
    _unicaInstancia = None

    def __init__(self):
        self.datos=[]
        self.umbral=30
         
    def cambiar_umbral(self,umbral:float):
        self.umbral=umbral

    def temperaturas(self):
        temperaturas=[]
        for dato in self.datos:
            temperaturas.append(dato.temperatura)
        return temperaturas

    @classmethod
    def obtener_instancia(cls):
        if not cls._unicaInstancia :
            cls._unicaInstancia = cls()
        return cls._unicaInstancia
    
    def actualizar(self,dato):
        self.datos.append(dato)


    
## R2: Observer

class Observable_Sensor:

    def __init__(self,nombre) -> None:
        self._nombre=nombre
        self.observers=[]
    
    def añadir_observer(self,observer):

        self.observers.append(observer)

    def eliminar_observer(self,observer):

        self.observers.remove(observer)

    def nuevo_dato(self,dato):
        for observers in self.observers:
            observers.actualizar(dato)

## R3 Chain of responsability

class Paso(IntEnum):
    Fin="0"
    Calcular_estadisticos="1"
    Supera_umbral="2"
    Aumento_brusco="3"

class Operaciones():
    def __init__(self,pasos:Paso) -> None:
        self.pasos=pasos
    
    def terminado(self) ->bool:
        return self.pasos==Paso.Fin

class Manejador(ABC):
    def __init__(self) -> None:
        self._proxima_operacion : Manejador
        self._paso_actual : Paso
    
    def set_paso(self,paso:Paso):
        self.paso_actual = paso
    
    def set_proxima_operacion(self,operacion):
        self._proxima_operacion=operacion
    
    def realizar_operacion(self,operaciones:Operaciones,datos):
        if self._paso_actual==(operaciones.pasos and self._paso_actual):
            self._operar(operaciones,datos)
        
        if (operaciones.terminado() or self._proxima_operacion==None):
            return
        else:
            self._proxima_operacion.realizar_operacion(operaciones,datos)

    @abstractmethod 
    def _operar(self,operacion:Operaciones,datos):
        raise NotImplementedError
    
class Calcular_estadisticos(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Calcular_estadisticos
        self._proxima_operacion = None
        # Asignamos el estadístico media por defecto.
        self.context=Context(Media)
    
    # Función para cambiar el estadístico.
    def cambiar_estadistico(self,estadistico):
        self.context.seleccionar_estadistico(estadistico)
    
    def _operar(self,operacion: Operaciones,sistema:Sistema):
        print("Calculando estadisticos:")
        return self.context.aplicar(sistema)

class Supera_umbral(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Supera_umbral
        self._proxima_operacion = None
 
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


class Aumento_brusco(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Aumento_brusco
        self._proxima_operacion = None
    
    def _operar(self, operacion:Operaciones,sistema:Sistema):
        print("--------------------------------------------------------\nComprobando si la temperatura ha aumentado más de 10ºC en los últimos 30 segundos:")
        aumenta=False
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

class Context:
    def __init__(self,estadistico) -> None:
        self.estadistico=estadistico

    def seleccionar_estadistico(self,estadistico):
        self.estadistico=estadistico
    
    def aplicar(self,sistema:Sistema):
        return self.estadistico.calcular_estadistico(self.estadistico,sistema)

class Estadistico(ABC):

    @abstractmethod
    def calcular_estadistico(self,sistema:Sistema):
        pass

class Media(Estadistico):
    
    def calcular_estadistico(self,sistema:Sistema):
        # calculamos la media y la desviación típica haciendo uso de la programación funcional.
        media= reduce(lambda x, y: x + y, sistema.temperaturas()[-12:]) / len(sistema.temperaturas()[-12:])
        dt=sqrt(sum((x - media) ** 2 for x in sistema.temperaturas()) / len(sistema.temperaturas()))

        print(f"La temperatura media en los últimos 60 segundos es de: {round(media,2)}ºC y la deviación típica es de {round(dt,2)}ºC.")
        return media,dt
    
class Cuantiles(Estadistico):

    def calcular_estadistico(self, sistema: Sistema):
        # Utilizamos la funcion np.quantile para calcular los diferentes cuantiles,
        primer_cuantil=np.quantile(0.25,sistema.temperaturas())
        segundo_cuantil=np.quantile(0.5,sistema.temperaturas())
        tercer_cuantil=np.quantile(0.75,sistema.temperaturas())

        print(f"Primer cuantil: {primer_cuantil}ºC.\nSegundo cuantil: {segundo_cuantil}ºC.\nTercer cuantil: {tercer_cuantil}ºC.")

        return primer_cuantil,segundo_cuantil,tercer_cuantil

class MaxMIn(Estadistico):

    def calcular_estadistico(self, sistema: Sistema):
        #Hallamos la temperatura máxima y mínima utilizando la programación funcional.
        t_max=reduce(lambda a, b: a if a > b else b, sistema.temperaturas()[-12:])
        t_min=reduce(lambda a, b: a if a < b else b, sistema.temperaturas()[-12:])

        print(f"Temperatura máxima y mínima alcanzada en los últimos 60 segundos:\nTemperatura máxima: {t_max}ºC\nTemperatura máxima: {t_min}ºC")
        return t_max,t_min
    