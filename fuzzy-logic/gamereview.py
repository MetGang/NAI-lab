#  Patryk Kośmider s16863
#  Krzysztof Marek s16663
#  
#  Recenzja gier komputerowych
#  https://github.com/scikit-fuzzy/scikit-fuzzy
# 
# Input:
#   Oprawa audiowizualna
#   Grywalność
#   Dopracowanie produktu
#   Stosunek ceny do rozmachu
# 
# Output:
#   Ocena generalna

import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control
import matplotlib.pyplot as plt

# argv
def terminate_on_argv():
    print('Bad input arguments!')
    sys.exit()

if len(sys.argv) != 5:
    terminate_on_argv()

argv = list(map(lambda x: sorted((0, int(x), 10))[1] if x.isnumeric() else terminate_on_argv(), sys.argv[1:]))

# Antecedents
audiovisuals = control.Antecedent(np.arange(0, 11, 1), 'Audiovisuals')
playability = control.Antecedent(np.arange(0, 11, 1), 'Playability')
refinement = control.Antecedent(np.arange(0, 11, 1), 'Refinement')
price_ratio = control.Antecedent(np.arange(0, 11, 1), 'Price ratio')

# Consequent
rating = control.Consequent(np.arange(0, 11, 1), 'Rating')

# Membership function population
audiovisuals.automf(5, names = [ 'Ugly', 'Bad', 'Average', 'Good', 'Outstanding' ])
playability.automf(5, names = [ 'Unplayable', 'Boring', 'Balanced', 'Enjoyable', 'Addictive' ])
refinement.automf(3, names = [ 'Buggy', 'Standard', 'Refined'])
price_ratio.automf(3, names = [ 'Expensive', 'Medium', 'Cheap' ])
rating.automf(7, names = [ 'Total crap', 'Could be better', 'Not bad, not good', 'Almost good', 'Good product', 'Highly enjoyable', 'Like a dream' ])

# Rules
rules = [
    control.Rule(audiovisuals['Ugly'] | playability['Unplayable'] | refinement['Buggy'] | price_ratio['Expensive'], rating['Total crap']),
    control.Rule(audiovisuals['Bad'] | playability['Boring'] | refinement['Standard'], rating['Could be better']),
    control.Rule(audiovisuals['Bad'] | playability['Balanced'] | refinement['Standard'], rating['Not bad, not good']),
    control.Rule(audiovisuals['Average'] | playability['Balanced'] | refinement['Standard'] | price_ratio['Medium'], rating['Almost good']),
    control.Rule(audiovisuals['Good'] | playability['Balanced'] | refinement['Standard'], rating['Good product']),
    control.Rule(audiovisuals['Good'] | playability['Enjoyable'] | refinement['Standard'], rating['Highly enjoyable']),
    control.Rule(audiovisuals['Outstanding'] | playability['Addictive'] | refinement['Refined'] | price_ratio['Cheap'], rating['Like a dream'])
]

# Simulation
rating_ctrl = control.ControlSystem(rules)
rating_sim = control.ControlSystemSimulation(rating_ctrl)

# Input
rating_sim.input['Audiovisuals'] = argv[0]
rating_sim.input['Playability'] = argv[1]
rating_sim.input['Refinement'] = argv[2]
rating_sim.input['Price ratio'] = argv[3]

# Computation
rating_sim.compute()

# Output
print(rating_sim.output['Rating'])

audiovisuals.view()
playability.view()
refinement.view()
price_ratio.view()
rating.view(sim = rating_sim)

plt.show()
