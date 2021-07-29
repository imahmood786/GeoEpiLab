import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Utility.functions as fun
import matplotlib
import plotly.express as px
import os


def random_selection(n, age_from=0, age_to=100, gender='*', race = '*', consume = True):
    global pop
    sub_pop = pop[(pop['age'] >= age_from) & (pop['age'] <= age_to)]
    result = []
    if len(sub_pop) > n:
        if gender != '*':
            sub_pop = sub_pop[(sub_pop['gender'] == gender)]

        if race != '*':
            sub_pop = sub_pop[(sub_pop['race'] == race)]

        if len(sub_pop)< n :
            samples = []
        else:
            samples = sub_pop.sample(n=n)

        if consume==True:
            pop = pop.drop(samples.index)
            for index, row in samples.iterrows():
                print(row['age'], row['gender'], row['race'])
                result.append(row['uid'])

    return result


def generate_household(hh_df):
    global pop
    hh_df['occupants'] = np.empty((len(hh_df), 0)).tolist()
    for index, row in hh_df.iterrows():

        size = row['size']
        if size=='1':
            #assign 1 adult occupant to the house
            selection = random_selection(1, 18, 100, '*', '*')
            if len(selection) > 0:
                hh_df.at[index, 'occupants'] = selection
            else:
                continue

        elif size=='2':
            #assign 2 adult occupants to the house
            selection = random_selection(2, 18, 100, '*', '*')
            if len(selection) > 1:
                hh_df.at[index, 'occupants'] = selection
            else:
                continue

        elif size == '3':
            # assign 2 adults & 1 kid occupants to the house
            temp = []
            temp.append(random_selection(1, 25, 60, 'Male', '*')[0])
            temp.append(random_selection(1, 25, 60, 'Female', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            hh_df.at[index, 'occupants'] = temp

        elif size == '4':
            # assign 2 adults & 2 kid occupants to the house
            temp = []
            temp.append(random_selection(1, 25, 60, 'Male', '*')[0])
            temp.append(random_selection(1, 25, 60, 'Female', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            hh_df.at[index, 'occupants'] = temp

        elif size == '5':
            # assign 2 adults & 3 kid occupants to the house
            temp = []
            temp.append(random_selection(1, 25, 60, 'Male', '*')[0])
            temp.append(random_selection(1, 25, 60, 'Female', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            temp.append(random_selection(1, 0, 18, '*', '*')[0])
            hh_df.at[index, 'occupants'] = temp

        elif size == '6':
            # assign 6 random occupants
            hh_df.at[index, 'occupants']= random_selection(6, 0, 100, '*', '*')

        elif size == '7':
            # assign 7 random occupants
            hh_df.at[index, 'occupants'] = random_selection(7, 0, 100, '*', '*')

        print('--------------', len(pop), '-----------------')
    return hh_df



pop = pd.read_csv(os.path.join(os.getcwd(), 'SynPop', 'hillsborough_pop.csv'))
pop = pop.head(10000)
houses = 600

#https://data.census.gov/cedsci/table?q=hillsborough%20household%20size%20percent&tid=ACSST1Y2019.S2501
household_data =    [['1', 28.87],
                    ['2', 33.63],
                    ['3', 16.6],
                    ['4', 12.7],
                    ['5', 5.29],
                    ['6', 1.85],
                    ['7', 1.06]]

hh_groups = [ x[0] for x in household_data]
hh_probs = [ x[1] for x in household_data]
hh_probs = np.array(hh_probs)/100
households = np.random.choice(hh_groups, size=houses, replace=True, p=hh_probs)
len(households)
hid = list(range(0,houses,1))
houses = np.stack((hid, households), axis=1)

hh_df = pd.DataFrame(houses, columns=['hid', 'size'])
fig = px.histogram(households)
fig.show()
df = generate_household(hh_df)


