import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def read_short_video_data(filename):
    table = pd.read_excel(filename)
    table.loc[table.subject == 'male_A', 'subject'] = 'male'
    table.loc[table.subject == 'male_B', 'subject'] = 'male'
    table.loc[table.subject == 'female_A', 'subject'] = 'female'
    table.loc[table.subject == 'female_B', 'subject'] = 'female'
    return table.drop(columns=['tank_num', 'date'])

def do_test_boxplot(data, col):
    control = data.loc['control'][col]
    treatment = data.loc['treatment'][col]
    print(f'{col}: {stats.mannwhitneyu(control, treatment)}')

    fig, ax = plt.subplots()
    ax.boxplot([control, treatment], labels=['control', 'treatment'])
    ax.set(title=f'{heading}')
    fig.savefig(f'{heading}.pdf', format='pdf')

short_videos = 'data/output_data_long_videos_PAIR_ID_corrected.xlsx'

def main():
    data = read_short_video_data(short_videos)
    do_test_boxplot(data, 'app_i')

if __name__ == '__main__':
    main()

# table = read_output_data('output_data_long_videos_PAIR_ID_corrected.xlsx'); table.head()

# table.loc[(table.cond == 'control') & (table.subject == 'female') & (table.pair_id == 2) & (table.status == 'F')]

# grouped_sum = table.groupby(['phase', 'status', 'cond', 'pair_id', 'subject']).sum()
# delta = grouped_sum.loc['habituation'] - grouped_sum.loc['experiment']; delta.head()

# delta_fs = delta.loc['F']; delta_fs
# delta.to_csv('out.csv')

# delta.to_csv('output_long_videos.csv')
# for heading in ['app_neighbour', 'app_partner', 'freeze_neighbour', 'l_neighbour']:
#     do_test_boxplot(delta_fs, heading)

################################################################################

def read_long_video_data(filename):
    table = pd.read_excel(filename)
    # table.loc[table.subject == 'nm', 'subject'] = 'm'
    # table.loc[table.subject == 'nf', 'subject'] = 'm'
    # table.loc[(table.int_pos == 'A') | (table.int_pos == 'B'), 'int_pos'] = 'AB'
    # table.loc[(table.int_pos == 'C') | (table.int_pos == 'D'), 'int_pos'] = 'CD'
    return table.drop(columns=['date'])

# table = read_output_data('intruder_tests_corrected_pair_id.xlsx'); table.head()

# match A-D & C-B for control, and A-A, B-B, etc for treatment
# always habituation minus experiment
# table.loc[((table.subject == 'nm') | (table.subject == 'm')) & (table.pair_id == 1)]

# For the above `pair_id = 1 & male`; m: A-D = -4, B-C = 16; nm: D-A = 0; C-B = 9; *always* subtract hab - exp

# ctbl = table.drop(columns=['tank_num']);

# def get_matching_pos(str):
#     if str == 'A':
#         return ('D', 'AD')
#     if str == 'B':
#         return ('C', 'BC')
#     if str == 'C':
#         return ('B', 'BC')
#     if str == 'D':
#         return ('A', 'AD')
#     assert False, str

# res = pd.DataFrame([], columns=ctbl.columns).drop(columns='phase')
# i = 0
# for k,v in ctbl.groupby(['phase', 'int_pos', 'subject', 'pair_id']):
#     if k[0] == 'habituation':
#         assert len(v) == 1, v
#         matching_pos, pos = get_matching_pos(k[1])
#         subject = k[2]
#         pair_id = k[3]
#         cond = v.iloc(0)[0]['cond']
#         status = v.iloc(0)[0]['status']

#         if np.isnan(v.iloc(0)[0]['app_n']):
#             print(f'Skipping NaN data: {k}')
#             continue

#         if cond == 'control' or cond == 'treatment':
#             matched = ctbl.loc[(ctbl.phase == 'experiment')
#                            & (ctbl.subject == subject)
#                            & (ctbl.pair_id == pair_id)
#                            & (ctbl.int_pos == matching_pos)]
#         else:
#             assert False, k

#         assert len(matched) == 1, v
#         assert cond == matched.iloc(0)[0]['cond'], v
#         assert status == matched.iloc(0)[0]['status'], v
#         row = (v.iloc(0)[0]['app_int':] - matched.iloc(0)[0]['app_int':]).append(pd.Series({
#             'int_pos': pos,
#             'pair_id': pair_id,
#             'subject': subject,
#             'status': status,
#             'cond': cond
#         }))
#         row.name = i
#         # Only increment i when a row is actually appended, not once for each input row
#         i = i + 1
#         res = res.append(row)

# res.loc[((res.subject == 'nm') | (res.subject == 'm')) & (res.pair_id == 1)]

# def do_test_boxplot(data, col):
#     control = data[data.cond == 'control'][col]
#     treatment = data[data.cond == 'treatment'][col]
#     print(f'{col}: {stats.mannwhitneyu(control, treatment)}')

#     fig, ax = plt.subplots()
#     ax.boxplot([control, treatment], labels=['control', 'treatment'])
#     ax.set(title=f'{heading}')

# res.to_csv('output_short_videos.csv')
# for heading in res.columns[5:7]:
#     do_test_boxplot(res, heading)

# to_compare = res.loc[((res.subject == 'nm') | (res.subject == 'nf')) & (res.int_pos == 'BC') & (res.status == 'F')]
# to_compare_grpd = to_compare.groupby('cond')
# control_app_ints = to_compare_grpd.get_group('control').loc[:,'app_int']
# treatment_app_ints = to_compare_grpd.get_group('treatment').loc[:,'app_int']
# stats.mannwhitneyu(control_app_ints, treatment_app_ints)
