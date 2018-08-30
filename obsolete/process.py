#!/usr/bin/python3

import attr
import sys

def replace_obs_id(str):
    if 'neighbour' in str:
        return str.replace('neighbour', 'treatment control')
    elif 'stranger' in str:
        return str.replace('stranger', 'treatment experiment')
    return str + " FIXME"

@attr.s
class Event:
    behaviour = attr.ib()
    modifier = attr.ib()

@attr.s
class CombiningData:
    obs_id = attr.ib()
    subject = attr.ib()

@attr.s
class BehaviourModifier:
    app_int = attr.ib(default=0)
    app_n = attr.ib(default=0)
    app_p = attr.ib(default=0)
    fsp_int = attr.ib(default=0)
    fsp_n = attr.ib(default=0)
    fsp_p = attr.ib(default=0)
    sb_int = attr.ib(default=0)
    sb_n = attr.ib(default=0)
    sb_p = attr.ib(default=0)
    mwr_p = attr.ib(default=0)
    l_int = attr.ib(default=None)
    l_n = attr.ib(default=None)

read_first_line = False

subject_to_record = dict()

# key is a CombiningData, value is BehaviourModifier
output_table = dict()
line_num = 1
last_obs_id = 'bogus'
last_subject = 'bogus'
num_no_modifiers = 0
# stores the start time for each observation.
vstarts = dict()

for line in sys.stdin:
    # Skip first line
    if not read_first_line:
        read_first_line = True
        continue

    line_num = line_num + 1
    cols = line.strip().split('\t')
    obs_id = replace_obs_id(cols[0])
    subject = cols[5]
    behaviour = cols[6]
    modifier = cols[7]
    timestamp = float(cols[9])

    # some basic sanity checking of the input
    if subject == 'No focal subject' and behaviour != 'vstart':
        print('Missing subject: {} @ {}, line num {}'.format(obs_id, timestamp, line_num))
    if not modifier:
        if behaviour == 'mwr':
            modifier = 'partner'
        elif behaviour != 'vstart':
            print('No modifier: {} @ {}, line num {}'.format(obs_id, timestamp, line_num))
    if subject in subject_to_record:
        subject_to_record[subject].append(Event(behaviour, modifier))
    else:
        subject_to_record[subject] = [Event(behaviour, modifier)]

    # Actual useful output, not just checking everything.
    combo = CombiningData(obs_id, subject)
    try:
        # get any preexisting data for this combo
        data = output_table[combo]
    except KeyError:
        data = BehaviourModifier()
        
    if behaviour == 'app':
        if modifier == 'intruder':
            data.app_int = data.app_int + 1
        elif modifier == 'neighbour':
            data.app_n = data.app_n + 1
        elif modifier == 'partner':
            data.app_p = data.app_p + 1
        else:
            print('app missing modifier on line {}, obs id = "{}", time = {}'
                  .format(line_num, obs_id, timestamp))
    elif behaviour == 'fsp':
        if modifier == 'intruder':
            data.fsp_int = data.fsp_int + 1
        elif modifier == 'neighbour':
            data.fsp_n = data.fsp_n + 1
        elif modifier == 'partner':
            data.fsp_p = data.fsp_p + 1
        else:
            print('fsp missing modifier on line {}, obs id = "{}", time = {}'
                  .format(line_num, obs_id, timestamp))
    elif behaviour == 'sb':
        if modifier == 'intruder':
            data.sb_int = data.sb_int + 1
        elif modifier == 'neighbour':
            data.sb_n = data.sb_n + 1
        elif modifier == 'partner':
            data.sb_p = data.sb_p + 1
        else:
            print('sb missing modifier on line {}, obs id = "{}", time = {}'
                  .format(line_num, obs_id, timestamp))
    elif behaviour == 'mwr':
        if modifier == 'partner':
            data.mwr_p == data.mwr_p + 1
        else:
            print('mwr missing modifier on line {}, obs id = "{}", time = {}'
                  .format(line_num, obs_id, timestamp))
    elif behaviour == 'vstart':
        vstarts[obs_id] = timestamp
    else:
        print('Missing behaviour on line {}'.format(line_num))
    
    try:
        if modifier == 'intruder' and (data.l_int is None or data.l_int > timestamp):
            data.l_int = timestamp - vstarts[obs_id]
    except KeyError:
        print('No vstart for line {}, observation id = {}'.format(line_num, obs_id))

    try:
        if modifier == 'neighbour' and (data.l_n is None or data.l_n > timestamp):
            data.l_n = timestamp - vstarts[obs_id]
    except KeyError:
        print('No vstart for line {}, observation id = {}'.format(line_num, obs_id))

    if behaviour != 'vstart':
        output_table[combo] = data

# After reading all input print number of events and some details
print('Read {} lines'.format(line_num))
# for subject, events in subject_to_record.items():
    # counting_set = set(events)
    # for i in counting_set:
        # print('Subject: {} Counted {} of {}'.format(subject, events.count(i), i))
        
with open('output_data.csv','w') as f:
    f.write('id, int_pos, cond, subject, app_int, app_n, app_p, fsp_int, fsp_n, fsp_p, sb_int, sb_n, sb_p, mwr_p, l_int, l_n\n')
    
    for k, v in output_table.items():
        # print('{} = {}'.format(k, v))
        
        # if the latency is None, that means that the fish did not react 
        # and set a maximum latency.
        if v.l_int is None:
            v.l_int = 5 * 60
        if v.l_n is None:
            v.l_n = 5 * 60
        
        f.write('{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(
            *k.obs_id.split(' '), k.subject, v.app_int, v.app_n, v.app_p, v.fsp_int, v.fsp_n, v.fsp_p, v.sb_int, v.sb_n, v.sb_p, v.mwr_p, v.l_int, v.l_n))
