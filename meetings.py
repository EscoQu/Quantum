import dwavebinarycsp
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

def scheduling(time, location, length, mandatory):
    if time:
        # Horas de oficina
        return (location and mandatory)
    else:
        # En casa
        return ((not location) and mandatory)

csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
csp.add_constraint(scheduling, ['time', 'location', 'length', 'mandatory'])

bqm = dwavebinarycsp.stitch(csp)
print(bqm.linear)
print(bqm.quadratic)

response = sampler.sample(bqm, num_reads = 5000)
min_energy = next(response.data(['energy'])) [0]

print(response)

total = 0

for sample, energy, occurrences in response.data({'sample', 'energy', 'num_occurrences'}):
    total = total + 1
    if energy == min_energy:
        time = 'business hours' if sample['time'] else 'evenings' 
        location = 'office' if sample['location'] else 'home' 
        length = 'short' if sample['length'] else 'long'
        mandatory = 'mandatory' if sample['mandatory'] else 'optimal'
        print("{}: during {} at {}, you can schedule a {} meeting that is {}" .format(occurrences, time , location, length, mandatory))
    