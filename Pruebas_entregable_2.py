from entregable_2 import *

calcular_estadisticos=Calcular_estadisticos()
supera_umbral=Supera_umbral()
aumento_brusco=Aumento_brusco()

calcular_estadisticos.set_proxima_operacion(supera_umbral)
supera_umbral.set_proxima_operacion(aumento_brusco)


problema=Operaciones(Paso)

calcular_estadisticos.realizar_operacion(problema)