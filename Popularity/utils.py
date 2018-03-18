import os
import codecs
import collections
import json
import math
def javascript_print_zipfchart(file_name, data_path, save_path):
    d = collections.OrderedDict()
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file == file_name:
                ls = json.load(codecs.open(os.path.join(root, file), "r+", "utf-8"))
                for cont in ls:
                    for word in cont['text']:
                        if word not in d:
                            d[word] = 1
                        else:
                            d[word] += 1
    d = sorted(d.items(), key=lambda d:d[1], reverse=True)
    res = []
    for i in range(len(d)):
        res.append(math.log(d[i][1], 10))
    with codecs.open(save_path, 'w+', 'utf-8') as f:
        f.write(str(res))

javascript_print_zipfchart(file_name='1_processed.json', data_path='../Datasets/Sources/testlong', save_path='js_zipf_1.txt')
