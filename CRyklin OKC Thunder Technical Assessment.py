#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install --upgrade pip')
get_ipython().system('{sys.executable} -m pip install numpy')
get_ipython().system('{sys.executable} -m pip install pandas')


# In[258]:


import pandas as pd
import numpy as np
shots_df = pd.read_csv('/Users/coriryklin/Documents/NBA data/shots_data.csv')

shots_df.head()


# In[259]:


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

shots_df.head()


# In[260]:


#shot distribution calculations
#-----------------------------------

shots_type_count = shots_df.groupby(by=['team', 'shot_type'])['shot_type'].count()
shots_FGA = shots_df.groupby(by=['team'])['team'].count()

# shots_type_count.head()

TeamA_FGA_pct = (shots_type_count['Team A']) / shots_FGA['Team A']
TeamB_FGA_pct = (shots_type_count['Team B']) / shots_FGA['Team B']

print('Team A shot distribution:', TeamA_FGA_pct)
print('Team B shot distribution:', TeamB_FGA_pct)

#EFG% calculation
#------------------------------------

shots_made = shots_df.groupby(by=['team','shot_type'])['fgmade'].sum()

TeamA_FGM = shots_made['Team A'].sum()
TeamA_3PM = TeamA_FGM - shots_made['Team A']['2PT']
TeamB_FGM = shots_made['Team B'].sum()
TeamB_3PM = TeamB_FGM - shots_made['Team B']['2PT']


TeamA_EFG = (TeamA_FGM + (0.5*TeamA_3PM))/shots_FGA['Team A']
TeamB_EFG = (TeamB_FGM + (0.5*TeamB_3PM))/shots_FGA['Team B']

print('Team A EFG%:', TeamA_EFG)
print('Team B EFG%:', TeamB_EFG)

# shots_made.head(10)


# In[ ]:





# In[ ]:




