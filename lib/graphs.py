import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats


def read_file(filename='data/intruder_tests_corrected_pair_id.csv'):
    return pd.read_csv(filename)


def build_box_plot_data_points_treatment(tbl, phase):
    with_pairs = tbl.assign(pair=tbl.loc[:,'subject'].transform(get_pair))
    treatment_s = with_pairs.groupby(['phase','cond','status','int_pos','pair','pair_id']) \
                            .sum().loc[phase,'treatment','S'].loc[:,'app_int']
    treatment_f = with_pairs.groupby(['phase','cond','status','int_pos','pair','pair_id']) \
                            .sum().loc[phase,'treatment','F'].loc[:,'app_int']

    far_f_focal = (treatment_f.loc['A'].append(treatment_f.loc['D'])).loc['focal']
    near_f_focal = (treatment_f.loc['B'].append(treatment_f.loc['C'])).loc['focal']
    near_f_neigh = (treatment_f.loc['B'].append(treatment_f.loc['C'])).loc['neighbour']
    near_s_neigh = (treatment_s.loc['B'].append(treatment_s.loc['C'])).loc['neighbour']
    near_s_focal = (treatment_s.loc['B'].append(treatment_s.loc['C'])).loc['focal']
    far_s_focal = (treatment_s.loc['A'].append(treatment_s.loc['D'])).loc['focal']

    return {
        'far_f': far_f_focal,
        'near_f': near_f_focal,
        'near_f_all': near_f_focal + near_f_neigh,
        'near_s_all': near_s_focal + near_s_neigh,
        'near_s': near_s_focal,
        'far_s': far_s_focal,
    }


def build_box_plot_data_points_control(tbl, phase):
    with_pairs = tbl.assign(pair=tbl.loc[:,'subject'].transform(get_pair))
    control_s = with_pairs.groupby(['phase','cond','status','int_pos','pair','pair_id']) \
                            .sum().loc[phase,'control','S'].loc[:,'app_int']
    control_f = with_pairs.groupby(['phase','cond','status','int_pos','pair','pair_id']) \
                            .sum().loc[phase,'control','F'].loc[:,'app_int']

    far_f_focal = (control_f.loc['A'].append(control_f.loc['D'])).loc['focal']
    near_f_focal = (control_f.loc['B'].append(control_f.loc['C'])).loc['focal']
    near_f_neigh = (control_f.loc['B'].append(control_f.loc['C'])).loc['neighbour']
    near_s_neigh = (control_s.loc['B'].append(control_s.loc['C'])).loc['neighbour']
    near_s_focal = (control_s.loc['B'].append(control_s.loc['C'])).loc['focal']
    far_s_focal = (control_s.loc['A'].append(control_s.loc['D'])).loc['focal']

    return {
        'far_f': far_f_focal,
        'near_f': near_f_focal,
        'near_f_all': near_f_focal + near_f_neigh,
        'near_s_all': near_s_focal + near_s_neigh,
        'near_s': near_s_focal,
        'far_s': far_s_focal,
    }


def group_tbl(tbl):
    with_pairs = tbl.assign(pair=orig.loc[:,'subject'].transform(get_pair))
    grpd = with_pairs.groupby(['phase','cond','int_pos','pair','status','pair_id','subject']).sum()

    ntbl = pd.DataFrame()
    for phase in ['habituation','experiment']:
        for cond in ['treatment','control']:
            for pos in ['A','B','C','D']:
                for subject in ['focal','neighbour']:
                    for status in ['F','S']:
                        ntbl.assign( grpd.loc[phase,cond,pos,subject,status].loc[:,'app_int'])
    return ntbl


def get_pair(gender):
    if gender == 'm' or gender == 'f':
        return 'focal'
    if gender == 'nm' or gender == 'nf':
        return 'neighbour'
    assert false, gender


def get_names():
    return [
        'habituation_control',
        'experiment_control',
        'habituation_treatment',
        'experiment_treatment'
    ]




def update_dict(d, key, value):
    d[key] = (int(value) + d.get(key, 0))


def read_data(filename='data/intruder_tests_corrected_pair_id.csv'):
    dicts = [dict() for _ in range(4)]
    with open(filename,'r') as f:
        import csv
        reader = csv.reader(f)
        for row in reader:
            # skip header
            if row[0] == 'tank_num':
                continue

            try:
                tank_num = row[0].strip()
                date = row[1].strip()
                position = row[2].strip()
                pair_id = int(row[3])
                status = row[4].strip()
                phase = row[5].strip()
                cond = row[6].strip()
                gender = row[7].strip()

                if tank_num == 'F6A' and date == '2017.04.28' and position == 'A':
                    # print(f'Skip: {row}')
                    continue

                pair = get_pair(gender)
                phase_cond = f'{phase}_{cond}'
                assert phase_cond in get_names(), phase_cond

                key = (tank_num, date, position, pair, pair_id)

                update_dict(dicts[get_names().index(phase_cond)], key, row[8])

            except ValueError as e:
                print(f'Skipping: {e}, {row}')
                pass
    return dicts


def generate_boxplot_data(dicts, i):
    a_focal = [v for k,v in dicts[i].items() if k[2] == 'A' and k[3] == 'focal']
    b_focal = [v for k,v in dicts[i].items() if k[2] == 'B' and k[3] == 'focal']
    c_focal = [v for k,v in dicts[i].items() if k[2] == 'C' and k[3] == 'focal']
    d_focal = [v for k,v in dicts[i].items() if k[2] == 'D' and k[3] == 'focal']
    b_neighbour = [v for k,v in dicts[i].items() if k[2] == 'B' and k[3] == 'neighbour']
    c_neighbour = [v for k,v in dicts[i].items() if k[2] == 'C' and k[3] == 'neighbour']
    b_all = [b_f + b_n for b_f, b_n in zip(b_focal, b_neighbour)]
    c_all = [c_f + c_n for c_f, c_n in zip(c_focal, c_neighbour)]
    return a_focal, b_focal, c_focal, d_focal, b_all, c_all


def do_plot(dicts, idxs):
    data_points = [list() for _ in range(6)]
    for i in idxs:
        results = generate_boxplot_data(dicts, i)
        for j, new_points in enumerate(results):
            data_points[j] += new_points

    print(f'lengths: {",".join([str(len(d)) for d in data_points])}')
    fig, ax = plt.subplots()
    ax.boxplot(
        data_points,
        labels=['A', 'B', 'B all', 'C all', 'C', 'D'],
        positions=[1, 3, 3.75, 5.25, 6, 8]
    )
    ax.set(ylabel='attacks per 2 min', title=f'{" + ".join([get_names()[i] for i in idxs])}')
    ax.set_ylim(0, 160)
