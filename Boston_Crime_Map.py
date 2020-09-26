#!/usr/bin/env python
# coding: utf-8

# # Boston City Crime Map GeoVisualization using Folium 

# In[15]:


import pandas as pd 
import folium
import math
from folium.plugins import MarkerCluster,HeatMap
import plotly.graph_objects as go 
import plotly.express as px
import datetime
from plotly.subplots import make_subplots


# # Importing Data for Boston City

# In[16]:


df = pd.read_csv("crime.csv",encoding='windows-1252')
df.head(3) # reading first 3 rows of the table


# # Generating the Boston Map

# In[18]:


boston = (42.358443,-71.05977)
m = folium.Map(location = boston, tile = 'Stamen terrain',zoom_start = 13)


# # Marking the Crime Scenes

# In[19]:


mc = MarkerCluster()
for idx,row in df.iterrows():
    if not math.isnan(row['Long']) and not math.isnan(row['Lat']):
        mc.add_child(folium.Marker([row['Lat'], row['Long']]))
m.add_child(mc)
m


# # Viewing the Districts that have the Highest Crime Rates

# In[22]:


crime = df.groupby(['DISTRICT','STREET','REPORTING_AREA','Lat','Long']).sum().reset_index()


# In[24]:


crime.update(crime['DISTRICT'].map('District:{}'.format))
crime.update(crime['REPORTING_AREA'].map('Reports:{}'.format))


# In[25]:


m2 = folium.Map(location = boston, tiles = 'stamentoner',zoom_start = 13)
HeatMap(data = crime[['Lat','Long']], radius = 15).add_to(m2)
# marking crime scenes
def plotDot(point):
    folium.CircleMarker(location = [point.Lat, point.Long],
                       radius = 5,
                       weight = 2,
                       popup = [point.DISTRICT,point.REPORTING_AREA],
                       fill_color='#000000').add_to(m2)
crime.apply(plotDot,axis = 1)
m2.fit_bounds(m2.get_bounds())
m2


# # Analysing Crimes that Requires Medical Assistance

# In[26]:


med = df.loc[df.OFFENSE_CODE_GROUP == 'Medical Assistance'][['Lat','Long']]
med.Lat.fillna(0,inplace = True)
med.Long.fillna(0,inplace = True)
m6 = folium.Map(location = boston,tiles = 'openstreetmap',zoom_start = 12)
HeatMap(data = med, radius = 16).add_to(m6)
m6


# In[28]:


import seaborn as sns
sns.catplot(y = 'OFFENSE_CODE_GROUP',
           kind = 'count',
           height = 8,
           aspect = 1.5,
           order = df.OFFENSE_CODE_GROUP.value_counts().index,
           data = df)


# In[ ]:




