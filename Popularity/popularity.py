import os
import json
import codecs
import os.path as path
import matplotlib.pyplot as plt
import numpy as np


def pop_calc(init_fname, data_path):
        ls = []
        for root, dirs, files in os.walk(data_path):
            for dir in dirs:
                if len(dir) > 2:
                    continue
                with codecs.open(os.path.join(root, dir, init_fname.replace('.json','.wordtr')), 'r+', 'utf-8') as input:
                    for line in input:
                        source = json.loads(line)
                        tot_pop = 0.0
                        tot_fre = 0.0
                        word_cnt = len(source)
                        if word_cnt == 0:
                            ls.append({'hour': None})
                            continue
                        for content in source:
                            tot_pop += content['pop']
                            tot_fre += content['fre']
                        ls.append({
                            'hour': dir,
                            'event_pop': tot_pop * tot_fre / (word_cnt * 1),
                            'event_pop2': tot_pop * tot_fre / (word_cnt * 0.2),
                            'event_pop5': tot_pop * tot_fre / (word_cnt * 0.5),
                            'event_pop8': tot_pop * tot_fre / (word_cnt * 0.8),
                        })
        # if not os.path.exists(os.path.join(os.getcwd(), 'popularity')):
        #     os.mkdir(os.path.join(os.getcwd(), 'popularity'))
        with codecs.open(os.path.join(data_path, init_fname.replace('.json','.pop')), 'w+', 'utf-8') as output:
            output.write(json.dumps(ls))
        print('Calculating Popularity Success!')

# pop_calc('data/fixed')

def show():
    for i in range(18):
        if i == 10 or i == 14 or i == 15:
            continue
        i = 5
        print(i)
        with codecs.open(path.join('popularity', str(i)+'.json')) as f:
            with codecs.open(path.join('emotionSeries', str(i) + '.json')) as fe:
                ls = json.loads(f.readline())
                s = []
                for content in ls:
                    s.append(content['event_pop'])
                    print(content['event_pop'])
                ss = np.array(s)
                ss = [(float(k)-min(ss))/(max(ss)-min(ss)) for k in ss]
                x = np.arange(23)
                plt.plot(x, ss)

                ls = json.loads(fe.readline())
                fess = np.array(ls)
                fess = [(float(k)-min(fess))/(max(fess)-min(fess)) for k in fess]
                print(len(ls))
                plt.plot(x, fess)

                plt.show()
        exit()

# show()