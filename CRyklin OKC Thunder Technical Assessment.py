#!/usr/bin/env python
# coding: utf-8

# In[394]:


import sys
get_ipython().system('{sys.executable} -m pip install --upgrade pip')
get_ipython().system('{sys.executable} -m pip install numpy')
get_ipython().system('{sys.executable} -m pip install pandas')


# In[395]:


import pandas as pd
import numpy as np
raw_shots_df = pd.read_csv('/Users/coriryklin/Documents/NBA data/shots_data.csv')
raw_shots_df.head()


# In[396]:


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


# In[397]:


test_df = shots_df.groupby(by=['team', 'shot_type']).agg(['sum', 'count'])
test_df.reset_index(inplace=True)
test_df.columns = ['team', 'shot_type', 'FGM', 'FGA']

df_2PT = test_df[test_df['shot_type'] == '2PT'].drop('shot_type', axis=1).rename(columns={'FGM':'2PTM','FGA':'2PTA'})
df_C3 = test_df[test_df['shot_type'] == 'C3'].drop('shot_type', axis=1).rename(columns={'FGM':'C3M','FGA':'C3A'})
df_NC3 = test_df[test_df['shot_type'] == 'NC3'].drop('shot_type', axis=1).rename(columns={'FGM':'NC3M','FGA':'NC3A'})
test_df = df_2PT.merge(df_C3, on='team').merge(df_NC3, on='team')

test_df['FGA'] = test_df['2PTA'] + test_df['C3A'] + test_df['NC3A']
test_df['FGM'] = test_df['2PTM'] + test_df['C3M'] + test_df['NC3M']

test_df['2PTA_shot_distribution'] = round(test_df['2PTA'] / test_df['FGA'],3)
test_df['C3A_shot_distribution'] = round(test_df['C3A'] / test_df['FGA'],3)
test_df['NC3A_shot_distribution'] = round(test_df['NC3A'] / test_df['FGA'],3)

test_df['EFG%'] = round((test_df['FGM'] + (0.5*(test_df['C3M']+test_df['NC3M']))) / test_df['FGA'],3)


test_df.head()


# In[ ]:




