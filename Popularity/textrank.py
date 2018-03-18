import os
import gensim
import json
import collections
import networkx
import codecs
import math

def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    # print sum1, sum2, denominator, float(numerator)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_rank(model_path, wiki_path, json_path, save_path):
    model = gensim.models.Word2Vec.load(model_path)
    wiki_model = gensim.models.Word2Vec.load(wiki_path)

    with codecs.open(json_path, 'r+', 'utf-8') as f:
        for line in f:
            source = json.loads(line)
    print('# of records:' + str(len(source)))

    dict_hour = collections.OrderedDict()

    Graph = networkx.Graph()

    for item in source:
        for word in item['text']:
            if word not in dict_hour:
                dict_hour[word] = 1
            else:
                dict_hour[word] += 1

    dict_hour = sorted(dict_hour.items(), key=lambda d:d[1], reverse=True)

    with codecs.open(json_path.replace('.json', '.fre'), 'w+', 'utf-8') as fre_files:
        res = []
        for i in range(len(dict_hour)):
            res.append({'word': dict_hour[i][0], 'fre': str(dict_hour[i][1])})
        fre_files.write(json.dumps(res))

    return


    dict_hour = [item for item in dict_hour if item[1] > 100]
    print('# of thresholded ' + str(len(dict_hour)))

    # add edges
    scale = len(dict_hour)
    for x in range(scale):
        for y in range(x, scale):
            if x == y:
                continue
            sim = 0.1 * get_cosine(collections.Counter(dict_hour[x][0]),
                                          collections.Counter(dict_hour[y][0]))
            if dict_hour[x][0] in model and dict_hour[y][0] in model:
                sim += 0.2 * model.similarity(dict_hour[x][0], dict_hour[y][0])
            if dict_hour[x][0] in wiki_model and dict_hour[y][0] in wiki_model:
                sim += 0.7 * wiki_model.similarity(dict_hour[x][0], dict_hour[y][0])
            if sim > 0:
                Graph.add_edge(x, y, weight=sim)

    print('# of nodes: ' + str(Graph.number_of_nodes()))
    print('# of edges: ' + str(Graph.number_of_edges()))
    print('pageranking...')
    pr = networkx.pagerank(Graph)
    result = [[dict_hour[j][0], dict_hour[j][1], pr[j], dict_hour[j][1] * pr[j]] for j in pr.keys()] # str, fre, pr, value
    with codecs.open(save_path, 'w+', 'utf-8') as fre_files:
        result = sorted(result, key=lambda d: d[3], reverse=True)
        res = []
        for i in range(len(result)):
            res.append({'keyword': result[i][0], 'fre': result[i][1], 'pr': result[i][2], 'pop': result[i][3]})
        fre_files.write(json.dumps(res))
    print(result)

# def textrank_dir(data_path=''):
#     for root, dirs, files in os.walk(data_path):
#         for dir in dirs:
#             if dir != '2018-01-26_20-00' and dir != '2018-01-26_21-00' and dir != '2018-01-26_22-00':
#                 continue
#             for i in range(18):
#                 try:
#                     print('Processing '+ os.path.join(root, dir, str(i)+'.json'))
#                     text_rank('w2vmodel/' + str(i) + '.w2v', 'w2vmodel/wiki/wiki.w2v', os.path.join(root, dir, str(i)+'.json'), os.path.join(root, dir, str(i)+'_hotword.json'))
#                 except:
#                     print('error')

# textrank_dir('data/fixed')

# text_rank('w2vmodel/0.w2v', 'w2vmodel/0.w2v', 'data/fixed/2018-01-26_00-00/6.json')



