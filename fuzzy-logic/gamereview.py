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
#   Stosunek ceny do zawartości
# 
# Output:
#   Ocena generalna

import sys
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control
#import matplotlib.pyplot as plt

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
rating.automf(6, names = [ 'Total crap', 'Could be better', 'Not bad, not good', 'Good product', 'Highly enjoyable', 'Like a dream' ])

# Rules
rules = [
    control.Rule(audiovisuals['Ugly'] | playability['Unplayable'] | refinement['Buggy'] | price_ratio['Expensive'], rating['Total crap']),
    control.Rule(audiovisuals['Bad'] | playability['Boring'], rating['Could be better']),
    control.Rule(audiovisuals['Average'] | refinement['Standard'], rating['Not bad, not good']),
    control.Rule(audiovisuals['Good'] | playability['Balanced'], rating['Good product']),
    control.Rule(playability['Enjoyable'] | price_ratio['Medium'], rating['Highly enjoyable']),
    control.Rule(audiovisuals['Outstanding'] | playability['Addictive'] | refinement['Refined'] | price_ratio['Cheap'], rating['Like a dream'])
]

# Simulation
rating_ctrl = control.ControlSystem(rules)
rating_sim = control.ControlSystemSimulation(rating_ctrl)

# Input
rating_sim.input['Audiovisuals'] = int(input('Podaj ocenę w skali 1-10 przyznaną za oprawę audiowizualną: '))
rating_sim.input['Playability'] = int(input('Podaj ocenę w skali 1-10 przyznaną za grywalność: '))
rating_sim.input['Refinement'] = int(input('Podaj ocenę w skali 1-10 przyznaną za dopracowanie produktu: '))
rating_sim.input['Price ratio'] = int(input('Podaj ocenę w skali 1-10 przyznaną za stosunek ceny do zawartości: '))

# Computation
rating_sim.compute()

# Output
print('\nOcena generalna za grę:% 0d'% (rating_sim.output['Rating']))

#audiovisuals.view()
#playability.view()
#refinement.view()
#price_ratio.view()
#rating.view(sim = rating_sim)

#plt.show()
