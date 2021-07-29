# importing pandas package
import pandas as pd
import os

# making data frame from csv file
data = pd.read_csv(os.path.join(os.getcwd(), 'Utility', 'employees.csv'))
# generating one row
rows = data.sample(frac=0.5)
data = data.drop(rows.index)
# display
print(len(data), len(rows))
