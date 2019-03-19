#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


# In[2]:


def read_output_data(filename):
    table = pd.read_excel(filename)
    table.loc[table.subject == 'male_A', 'subject'] = 'male'
    table.loc[table.subject == 'male_B', 'subject'] = 'male'
    table.loc[table.subject == 'female_A', 'subject'] = 'female'
    table.loc[table.subject == 'female_B', 'subject'] = 'female'
    return table.drop(columns=['tank_num', 'date'])


# In[42]:


table = read_output_data('data/output_data_long_videos_PAIR_ID_corrected.xlsx'); table.head()


# In[43]:


table.loc[(table.cond == 'control') & (table.subject == 'female') & (table.pair_id == 2) & (table.status == 'F')]


# In[44]:


def get_treatments_experiments(table):
    grouped = table.groupby(['status','cond','phase','subject','pair_id']).sum().loc['F']
    return (grouped.loc['treatment'], grouped.loc['control'])

treatments, controls = get_treatments_experiments(table)


# In[45]:


stats.mannwhitneyu(
    treatments.loc['habituation']['app_neighbour'], 
    treatments.loc['experiment']['app_neighbour'],
    alternative='two-sided')


# In[46]:


stats.mannwhitneyu(
    controls.loc['habituation']['app_neighbour'], 
    controls.loc['experiment']['app_neighbour'],
    alternative='two-sided')


# In[47]:


grouped_sum = table.groupby(['phase', 'status', 'cond', 'pair_id', 'subject']).sum()
delta = grouped_sum.loc['habituation'] - grouped_sum.loc['experiment']; delta.head()


# In[48]:


delta_fs = delta.loc['F']; delta_fs
delta.to_csv('output_long_videos_before_minus_after.csv')


# In[104]:


def do_test_boxplot(data, col):
    control = data.loc['control'][col]
    treatment = data.loc['treatment'][col]
    print(f'{col}: {stats.mannwhitneyu(control, treatment)}')

    fig, ax = plt.subplots()
    # only app_neighbour is correct here
    props = {'connectionstyle':'bar','arrowstyle':'-',                 'shrinkA':10,'shrinkB':10,'linewidth':2}
    sig_start = max(max(control), max(treatment))
    ax.annotate('', xy=(1,sig_start), xytext=(2,sig_start), arrowprops=props)
    ax.annotate('**', xy=(1.5,sig_start))
    ax.boxplot([control, treatment], labels=['control', 'treatment'])
    ax.set(ylabel='Approaches relative to baseline')
    
    
    fig.savefig(f'{heading}.pdf', format='pdf')


# In[105]:


for heading in ['app_neighbour', 'app_partner', 'freeze_neighbour', 'l_neighbour']:
    do_test_boxplot(delta_fs, heading)


# In[21]:


get_ipython().system('jupyter nbconvert --to script "Fishy stuff t-tests-long videos-Pandas.ipynb"')

