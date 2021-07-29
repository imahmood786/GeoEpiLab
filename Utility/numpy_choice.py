import numpy as np

prog_langs = ['python', 'c++', 'java', 'ruby']

# generating random samples
print(np.random.choice(prog_langs, size=8))

# generating random samples without replacement
print(np.random.choice(prog_langs, size=3, replace=False))

# generating random samples with probabilities
print(np.random.choice(prog_langs, size=10,
                       replace=True, p=[0.7, 0.1, 0.1,0.1]))