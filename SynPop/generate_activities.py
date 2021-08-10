import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Utility.functions as fun
import matplotlib
import plotly.express as px
import os
import plotly.figure_factory as ff
from datetime import datetime
from datetime import timedelta
import  plotly as py
import numpy as np
import os
import geopandas as gpd
import pandas as pd
import plotly.express as px
import  plotly as py
import os
from shapely.geometry import Point
import random


def get_activities(hour_of_the_day):
    global schedule
    next = hour_of_the_day + timedelta(hours=1)
    result = schedule[(schedule['START']>=hour_of_the_day) & (schedule['START']<=next)]
    return  list(result.index.values)

def get_duration(rand_activity_index):
    global schedule
    schedule_row = schedule.loc[rand_activity_index]
    return  schedule_row['DURATION']

def get_rand_activity_location(rand_activity_index):
    global LG,activities, schedule

    schedule_row = schedule.loc[rand_activity_index]
    activity_row = activities[activities.ACTIVITY == schedule_row['ACTIVITY']]
    activity_type = activity_row['Type'].values[0]
    activity_location = LG[LG['type'] == activity_type]
    return  activity_location

# load location graph
LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'VE', 'GIS','landuse.geojson'))
LG = LG.to_crs("EPSG:3857")

# load people
pop = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab','SynPop', 'hillsborough_pop33612.csv'))
# Load households
households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab','SynPop', 'hillsborough_hh33612.csv'))




activities = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'SynPop', 'data', 'activities.csv'))
places = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'SynPop', 'data', 'places.csv'))
schedule = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'GeoEpiLab', 'SynPop', 'data', 'schedule.csv'))
# schedule = schedule[schedule['AGE']==15]
schedule = schedule.drop(schedule[schedule['PLACE']>=115].index)
schedule['START'] = pd.to_datetime(schedule['START'])
schedule['STOP'] =  pd.to_datetime(schedule['STOP'])
schedule = pd.merge(schedule, activities, on="ACTIVITY") #Merge activity
schedule = pd.merge(schedule, places, on="PLACE") #Merge activity
schedule = schedule.drop(schedule[(schedule['PLACE']==101)].index)  # Remove activities at home
schedule = schedule.drop(schedule[(schedule['ACTIVITY']<50000)].index) # Remove activities at home
schedule = schedule.drop(schedule[(schedule['ACTIVITY']>=500000)].index) #remove unlocated activities
times = pd.date_range(schedule['START'].min(), periods=24, freq='1H').tolist()

#place to assign activities
ages = schedule['AGE'].drop_duplicates().tolist()
ages.sort()
alist = []
for age in ages:
    for time in times:
        activities_ofthe_hour = get_activities(time) #indexes to the rows of schedule table
        dic = {'age':age, 'time': time , 'activities' : activities_ofthe_hour}
        alist.append(dic)

activity_df = pd.DataFrame(alist) # these are list of activities per age per hour of the day

visits = []
for hindex, hrow in households.iterrows():
    house_location = Point(hrow['x'], hrow['y'])
    occupants = hrow['occupants']
    occupants = occupants.replace('[', '').replace(']', '')
    occupants = occupants.strip()
    occupants = occupants.replace(' ', '')
    occupants = occupants.split(',')
    occupants = np.array(occupants, dtype=np.int)
    persons = pop.loc[pop['uid'].isin(occupants)]
    print(hindex)
    for pindex, prow in persons.iterrows():
        #pick a random activity and assign at each hour of the day
        for time in times:
            act = activity_df[(activity_df.age==prow['age']) & (activity_df.time == time)]
            if act['activities'].tolist() == []:
                continue
            else:
                rand_activity = random.choice(act['activities'].tolist())[0]
                end_location = get_rand_activity_location(rand_activity) #pass row index to get the activity
                if not end_location.empty:
                    end_location = end_location.sample(n=1)
                    end_loc = end_location.iloc[0]['geometry'].centroid
                    duration = get_duration(rand_activity)
                    dic = {'uid':prow['uid'], 'age':prow['age'], 'time': time, 'SX':house_location.x, 'SY': house_location.y, 'EX':end_loc.x,'EY':end_loc.y, 'duration':duration}
                    print(str(dic))
                    visits.append(dic)
    print()

visits_df = pd.DataFrame(visits)
len(visits_df)
visits_df.to_csv(os.path.join(os.getcwd(), 'SynPop', 'hillsborough_mov33612.csv'), index=False)
#Plot activities
# tasks = []
# for index, row in schedule.iterrows():
#     dic = dict(Task="Task" + str(index), Start=str(row['START']), Finish=str(row['START'] + timedelta(minutes=row['DURATION'])), Resource=row['ACTIVITY_DESC'] + ' ' + row['PLACE_DESC'])
#     tasks.append(dic)
#
#
# df = pd.DataFrame(tasks)
# df = df.sort_values(by=['Start', 'Resource'])
# fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource", width=1500, height=1500)
# fig.update_yaxes(autorange="reversed")
# py.offline.plot(fig, filename= "Schedules.html")
# fig.show()
