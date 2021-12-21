import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

##############################################################
##  horario     --> 1: Trabajo      0: fuera de horario
##  ubicacion   --> 1: Presencial   0: Remoto
##  duracion    --> 1: Larga        0: Corta
##  asistencia  --> 1: Obligatoria  1: Opcional
##############################################################

def planifica(horario, ubicacion, duracion, asistencia):
    if horario: 
        # En horas de Oficina
        return (ubicacion and asistencia)
    else:
        # Fuera de horario
        return (not ubicacion and not duracion)

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
    duracion = 'larga' if sample['duracion'] else 'corta'
    asistencia = 'obligatoria' if sample['asistencia'] else 'opcional'
    print("{}: {} sesion de tipo {}, de duracion {} con asistencia {}"
                .format(occurences, horario, ubicacion, duracion, asistencia))