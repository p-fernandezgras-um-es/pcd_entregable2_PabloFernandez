from abc import ABC, abstractmethod
import numpy as np
from functools import reduce
from enum import IntEnum

## R1: Singleton
class Sistema:
    _unicaInstancia = None

    def __init__(self):
        self.datos=[]
         
         

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
    
    def realizar_operacion(self,operaciones:Operaciones):
        if self._paso_actual==(operaciones.pasos and self._paso_actual):
            self._operar(operaciones)
        
        if (operaciones.terminado() or self._proxima_operacion==None):
            return
        else:
            self._proxima_operacion.realizar_operacion(operaciones)

    @abstractmethod 
    def _operar(self,operacion:Operaciones):
        raise NotImplementedError
    
class Calcular_estadisticos(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Calcular_estadisticos
        self._proxima_operacion = None
    
    def _operar(self, operacion: Operaciones):
        print("Calculando estadisticos")

class Supera_umbral(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Supera_umbral
        self._proxima_operacion = None
    
    def _operar(self, operacion: Operaciones):
        print("Supera umbral")

class Aumento_brusco(Manejador):
    def __init__(self) -> None:
        self._paso_actual = Paso.Aumento_brusco
        self._proxima_operacion = None
    
    def _operar(self, operacion: Operaciones):
        print("Aumento brusco")
        