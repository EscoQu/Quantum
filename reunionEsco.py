#Programa para solución de un problema de satisfacción de restricciones
#En este caso, se trata de ver qué opciones son compatibles para las reuniones
#de trabajo, sabiendo que en horario de trabajo (horario=1)
# restricción 1) las reuniones deben ser presenciales (ubicación=1) y
# restricción 2) las reuniones deben ser de obligatioria presencia (asistencia=1),
#  además de que fuera de horario de trabajo (horario =0)
# restricción 3) las reuniones deben ser remotas (ubicación=0) y
# restricción 4) las reuniones deben ser cortas (duracion=1)

#Importamos de DWave, los muestreadores y encajadores en su topología
import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())
#Estos otros samplers también podríamos utilizarlos, para ver a qué máquina 
#cuántica acude nuestro envío y con qué topología de conexiones entre qubits:
# sampler = EmbeddingComposite(DWaveSampler(solver='DW_2000Q_6'))
# sampler = EmbeddingComposite(DWaveSampler(solver=dict(topology__type='pegasus')))

#las variables binarias que nos interesan para el problema
##############################################################
##  horario     --> 1: Trabajo      0: fuera de horario
##  ubicacion   --> 1: Presencial   0: Remoto
##  duracion    --> 1: Corta        0: Larga
##  asistencia  --> 1: Obligatoria  1: Opcional
##############################################################
#hacemos una función de python relativa a las restricciones de antes
def planifica(horario, ubicacion, duracion, asistencia):
    if horario: 
        # En horas de Oficina, si horario de trabajo es verdadero=1, ubicación y asistencia 
        #también tienen que ser verdadero
        return (ubicacion and asistencia)
    else:
        # Fuera de horario, si horario de trabajo es falso=0, entonces ubicación es falso (remoto)
        #y duración es falso (corto, ojo he cambiado del archivo de Git de PacoGalvez)
        return (not ubicacion and duracion)

#aquí, en lugar de buscar nosotros las funciones penalty cuadráticas, para la restricción,
#que valen 0 cuando las restricciones se cumplen y 1 cuando no lo valen ( por ejemplo
#si x=>y, resolviendo la ecuación en 4 coeficentes a, b, c, d son las incógnitas:
#f(x,y)=ax+by+cxy+d, en los 4 casos posibles, y haciendo f(1,0)=1 y el resto 0, nos saldría
#f(x,y)=x-xy, y eso lo haríamos con todas, pero DWave ya sabe hacerlo, con la función
#planifica que contiene las restricciones.
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(planifica, ['horario', 'ubicacion', 'duracion', 'asistencia'])

bqm = dwavebinarycsp.stitch(csp)
print(bqm.linear)
print(bqm.quadratic)

response = sampler.sample(bqm, num_reads = 5000)
min_energy = next(response.data(['energy']))[0]

print(response)

total = 0
for sample, energy, occurences in response.data(['sample', 'energy', 'num_occurrences']):
    total = total + occurences
    # if energy == min_energy:
    horario = 'Horario de trabajo' if sample['horario'] else 'Fuera de horario'
    ubicacion = 'presencial' if sample['ubicacion'] else 'remota'
    duracion = 'corta' if sample['duracion'] else 'larga'
    asistencia = 'obligatoria' if sample['asistencia'] else 'opcional'
    print("{}: {} sesion de tipo {}, de duracion {} con asistencia {}"
                .format(occurences, horario, ubicacion, duracion, asistencia))