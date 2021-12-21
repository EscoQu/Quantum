import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

# Definimos el Sampler
sampler = EmbeddingComposite(DWaveSampler())

# El método scheduling, comprueba las restricciones
def scheduling(time, location, length, mandatory):
    if time:
        # Horas de oficina
        return (location and mandatory and length)
    else:
        # En casa
        return ((not location and not length))

# Se definen las restricciones
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

# Se pasan las restricciones mediante el método scheduling
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory'])

#  Se carga el csp como un bqm ???
bqm = dwavebinarycsp.stitch(csp)
print(bqm.linear)
print(bqm.quadratic)

# Se pasa el modelo al sampler y lanzamos contra la QPU, recogemos el resultado en response.
response = sampler.sample(bqm, num_reads = 5000)

# Se leen los estamos de mínima energía
min_energy = next(response.data(['energy']))[0]


# Imprimir el muestreo
print(response)

# Ponemos la variable total = 0 e iteramos sobre los valores obtenidos de la QPU
total = 0

# Ahora se lee el resultado (muestreo) y se cogen lo estados de mínima energía
for sample, energy, occurrences in response.data(['sample', 'energy', 'num_occurrences']):
    total = total + occurrences
    if energy == min_energy:
        time = 'horas de oficina' if sample['time'] else 'las tardes' 
        location = 'presencial' if sample['location'] else 'remota' 
        length = 'de larga duración' if sample['length'] else 'de corta duración'
        mandatory = 'obligatoria' if sample['mandatory'] else 'opcional'
        print("{}: Durante {}, puedes planificar una reunión {}, {} con asistencia {}" .format(occurrences, time , location, length, mandatory))

#for sample, energy, occurences in response.data(['sample', 'energy', 'num_occurrences']):
#    total = total + occurences
#    if energy == min_energy:
#        time = 'business hours' if sample['time'] else 'evenings'
#        location = 'office' if sample['location'] else 'home'
#        length = 'short' if sample['length'] else 'long'
#        mandatory = 'mandatory' if sample['mandatory'] else 'optional'
#        print("{}: During {} at {}, you can schedule a {} meeting that is {}"
#                .format(occurences, time, location, length, mandatory))   