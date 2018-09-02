import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats


def update_dict(d, key, row):
    empty = [0 for _ in row]
    d[key] = (int(row[0]) + d.get(key, 0))


def get_pair(gender):
    if gender == 'm' or gender == 'f':
        return 'focal'
    if gender == 'nm' or gender == 'nf':
        return 'neighbour'
    assert false, gender


def get_position(position):
    if position == 'A' or position == 'D':
        return 'AD'
    elif position == 'B' or position == 'C':
        return 'BC'
    assert False, position


class CrazyKey:
    def __init__(self, phase, position, cond, *args):
        self.phase = phase
        self.position = get_position(position)
        self.original_position = position
        self.cond = cond
        self.args = args

    def __eq__(self, other):
        return self.args == other.args and self.position == other.position

    def __hash__(self):
        return hash((self.args, self.position))

    def __str__(self):
        return f'{self.phase} & {self.original_position} & {self.cond} & {self.args}'


# in order to signal whether the subtraction has been done or not, the value is an int
# if the second value has been seen, and a string if it has.
def combine(crazy_dict, key, app):
    assert type(crazy_dict) is dict
    assert type(key) is CrazyKey
    assert type(app) is int

    try:
        (old_key, old_app) = crazy_dict[key]
        if old_key.phase == 'habituation' and key.phase == 'experiment':
            val = old_app - app
            # assert val >= 0, f'{k} -> {val}'
            return (old_key, f'{val}')

        if old_key.phase == 'experiment' and key.phase == 'habituation':
            val = app - old_app
            # assert val >= 0, f'{k} -> {val}'
            return (key, f'{val}')

        assert False, f'{old_key} f{key}'

    except KeyError:
        # Other entry not found yet, save app_i
        return (key, app)


def get_names():
    return [
        'habituation_control',
        'experiment_control',
        'habituation_treatment',
        'experiment_treatment'
    ]


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

                update_dict(dicts[get_names().index(phase_cond)], key, row[8:10])

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
    import matplotlib.pyplot as plt

    data_points = [list() for _ in range(6)]
    for i in idxs:
        results = generate_boxplot_data(dicts, i)
        for j, new_points in enumerate(results):
            data_points[j] += new_points

    print(f'{",".join([str(len(d)) for d in data_points])}')
    fig, ax = plt.subplots()
    ax.boxplot(
        data_points,
        labels=['A', 'B', 'B all', 'C all', 'C', 'D'],
        positions=[1, 3, 3.75, 5.25, 6, 8]
    )
    ax.set(ylabel='attacks per 2 min', title=f'{" + ".join([get_names()[i] for i in idxs])}')
    ax.set_ylim(0, 160)
