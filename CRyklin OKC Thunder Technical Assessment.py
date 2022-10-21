#!/usr/bin/env python
# coding: utf-8

# In[404]:


import sys
get_ipython().system('{sys.executable} -m pip install --upgrade pip')
get_ipython().system('{sys.executable} -m pip install numpy')
get_ipython().system('{sys.executable} -m pip install pandas')


# In[405]:


import pandas as pd
import numpy as np
raw_shots_df = pd.read_csv('/Users/coriryklin/Documents/NBA data/shots_data.csv')
raw_shots_df.head()


# In[406]:


shots_df = raw_shots_df.copy()
shots_df['shot_distance'] = shots_df['x']**2 + shots_df['y']**2
shots_df['shot_distance'] = round(np.sqrt(shots_df['shot_distance']), 2)

def shot_determination(row):
    if row['shot_distance'] > 23.75 and row['y'] > 7.8:
        shot_type = 'NC3'
    elif abs(row['x']) > 22 and row['y'] <= 7.8:
        shot_type = 'C3'
    else:
        shot_type = '2PT'
    return shot_type

shots_df['shot_type'] = shots_df.apply(shot_determination, axis=1)
shots_df.drop(['x', 'y', 'shot_distance'], axis=1, inplace=True)

shots_df.head()


# In[407]:


test_df = shots_df.groupby(by=['team', 'shot_type']).agg(['sum', 'count'])
test_df.reset_index(inplace=True)
test_df.columns = ['team', 'shot_type', 'FGM', 'FGA']


# In[408]:


def EFG_percentage(row):
    if row['shot_type'] == '2PT':
        return round(row['FGM'] / row['FGA'],3)
    else:
        return round((row['FGM'] + 0.5*(row['FGM'])) / row['FGA'],3)

EFG_df['EFG%'] = test_df.apply(EFG_percentage, axis=1)

EFG_df.head(10)


# In[410]:


df_2PT = EFG_df[EFG_df['shot_type'] == '2PT'].drop('shot_type', axis=1).rename(columns={'FGM':'2PTM','FGA':'2PTA','EFG%':'2PT eFG%'})
df_C3 = EFG_df[EFG_df['shot_type'] == 'C3'].drop('shot_type', axis=1).rename(columns={'FGM':'C3M','FGA':'C3A','EFG%':'C3 eFG%'})
df_NC3 = EFG_df[EFG_df['shot_type'] == 'NC3'].drop('shot_type', axis=1).rename(columns={'FGM':'NC3M','FGA':'NC3A','EFG%':'NC3 eFG%'})
team_df = df_2PT.merge(df_C3, on='team').merge(df_NC3, on='team')

team_df['FGA'] = team_df['2PTA'] + team_df['C3A'] + team_df['NC3A']
team_df['FGM'] = team_df['2PTM'] + team_df['C3M'] + team_df['NC3M']

team_df['2PTA_shot_distribution'] = round(team_df['2PTA'] / team_df['FGA'],3)
team_df['C3A_shot_distribution'] = round(team_df['C3A'] / team_df['FGA'],3)
team_df['NC3A_shot_distribution'] = round(team_df['NC3A'] / team_df['FGA'],3)

team_df['EFG%'] = round((team_df['FGM'] + (0.5*(team_df['C3M']+team_df['NC3M']))) / team_df['FGA'],3)


team_df.head()


# In[ ]:




