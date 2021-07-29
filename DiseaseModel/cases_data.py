import pandas as pd
import numpy as np
import plotly.express as px
import  plotly as py
import os

df = pd.read_csv('COVID_Cases2021-07-16 public.csv')
df =  df.dropna(subset=['Date'])
# count = 0
# for index, row in df.iterrows():
#     dt = row['Date']
#     if not dt or pd.isnull(dt):
#         count+=1
# print(count)

df['Date'] = pd.to_datetime(df['Date'],format='%m/%d/%Y').dt.date
# print(df.dtypes)
dfg = pd.DataFrame(columns=['Date', 'Cases'])
groups = df.groupby('Date')
for name, group in groups:
    dict = {'Date': name, 'Cases': group.size}
    dfg = dfg.append(dict, ignore_index = True)

fig = px.line(dfg, x='Date', y="Cases")
py.offline.plot(fig, filename= "cases_data.html")
fig.show()