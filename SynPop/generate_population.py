import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Utility.functions as fun
import matplotlib
import plotly.express as px
import os

# Hillsborough Age Distr [https://censusreporter.org/profiles/05000US12057-hillsborough-county-fl/]
# 0-9	11.80%
# 10-19	12.80%
# 20-29	14%
# 30-39	14.50%
# 40-49	13.70%
# 50-59	12.70%
# 60-69	10.50%
# 70-79	6.60%
# 80+	3.20%

# gender_data =   [['Male', 48.9],
#                 ['Female', 51.1]]


# Hillsborough Race Distr
# White	47.30%
# Black	15.90%
# Native	0.1%†
# Asian	4%
# Islander	0.1%†
# Other	0.5%†
# Two+	2.5%†
# Hispanic	29.70%


# total_population = 1471968
total_population = 44601 #33612 population [https://www.zip-codes.com/county/fl-hillsborough.asp]
# total_population = 1000

age_data =  [['0-9', 11.80],
            ['10-19', 12.80],
            ['20-29', 14],
            ['30-39', 14.50],
            ['40-49', 13.70],
            ['50-59', 12.70],
            ['60-69', 10.50],
            ['70-79', 6.60],
            ['80-100', 3.40]]

gender_data =   [['Male', 48.9],
                ['Female', 51.1]]

race_data = [['White', 47.30],
            ['Black', 15.90],
            ['Native', 0.1],
            ['Asian', 4],
            ['Islander', 0.1],
            ['Other', 0.5],
            ['Two', 2.4],
            ['Hispanic', 29.70]]

pop_id = list(range(1,total_population,1))
pop_df = pd.DataFrame(pop_id, columns=['uid'])

age_groups = [ x[0] for x in age_data]
age_probs = [ x[1] for x in age_data]
age_probs = np.array(age_probs)/100

# get random ages based on prob. distribution
ages = np.random.choice(age_groups, size=len(pop_df), replace=True, p=age_probs)
for i, val in enumerate(ages):
    from_age, to_age = val.split('-')
    # print(from_age, to_age)
    ages[i] = np.random.randint(from_age, to_age, 1, int)[0]

pop_df = pop_df.sample(frac=1) #shuffle dataframe to randomize before the selection
pop_df['age'] = ages


gender_groups = [ x[0] for x in gender_data]
gender_probs = [ x[1] for x in gender_data]
gender_probs = np.array(gender_probs)/100

# get random gender based on prob. distribution
genders = np.random.choice(gender_groups, size=len(pop_df), replace=True, p=gender_probs)
pop_df = pop_df.sample(frac=1) #shuffle dataframe to randomize before the selection
pop_df['gender'] = genders


#Add races
race_groups = [ x[0] for x in race_data]
race_probs = [ x[1] for x in race_data]
race_probs = np.array(race_probs)/100

pop_df.reset_index()
# get random gender based on prob. distribution
races = np.random.choice(race_groups, size=len(pop_df), replace=True, p=race_probs)
pop_df = pop_df.sample(frac=1) #shuffle dataframe to randomize before the selection
pop_df['race'] = races

pop_df.reset_index(drop=True, inplace=True)
pop_df = pop_df.sort_values(by='uid')

pop_df.to_csv(os.path.join(os.getcwd(), 'SynPop','hillsborough_pop33612.csv'), index=False)
fig = px.histogram(pop_df, x="age")
fig.show()

fig = px.histogram(pop_df, x="gender")
fig.show()

fig = px.histogram(pop_df, x="race")
fig.show()


