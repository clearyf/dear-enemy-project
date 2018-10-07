
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


# In[3]:


def read_output_data(filename):
    table = pd.read_excel(filename)
    table.loc[table.subject == 'male_A', 'subject'] = 'male'
    table.loc[table.subject == 'male_B', 'subject'] = 'male'
    table.loc[table.subject == 'female_A', 'subject'] = 'female'
    table.loc[table.subject == 'female_B', 'subject'] = 'female'
    return table.drop(columns=['tank_num', 'date'])


# In[4]:


def do_test_boxplot(data, col):
    control = data.loc['control'][col]
    treatment = data.loc['treatment'][col]
    print(f'{col}: {stats.mannwhitneyu(control, treatment)}')

    fig, ax = plt.subplots()
    ax.boxplot([control, treatment], labels=['control', 'treatment'])
    ax.set(title=f'{heading}')
    fig.savefig(f'{heading}.pdf', format='pdf')


# In[5]:


table = read_output_data('data/output_data_long_videos_PAIR_ID_corrected.xlsx'); table.head()


# In[6]:


table.loc[(table.cond == 'control') & (table.subject == 'female') & (table.pair_id == 2) & (table.status == 'F')]


# In[7]:


def get_treatments_experiments(table):
    grouped = table.groupby(['status','cond','phase','subject','pair_id']).sum().loc['F']
    return (grouped.loc['treatment'], grouped.loc['control'])

treatments, controls = get_treatments_experiments(table)


# In[12]:


stats.mannwhitneyu(
    treatments.loc['habituation']['app_neighbour'], 
    treatments.loc['experiment']['app_neighbour'],
    alternative='two-sided')


# In[14]:


stats.mannwhitneyu(
    controls.loc['habituation']['app_neighbour'], 
    controls.loc['experiment']['app_neighbour'],
    alternative='two-sided')


# In[ ]:


grouped_sum = table.groupby(['phase', 'status', 'cond', 'pair_id', 'subject']).sum()
delta = grouped_sum.loc['habituation'] - grouped_sum.loc['experiment']; delta.head()


# In[ ]:


delta_fs = delta.loc['F']; delta_fs
delta.to_csv('out.csv')


# In[ ]:


delta.to_csv('output_long_videos.csv')
for heading in ['app_neighbour', 'app_partner', 'freeze_neighbour', 'l_neighbour']:
    do_test_boxplot(delta_fs, heading)

