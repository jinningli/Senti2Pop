import gensim
import json
import os
import codecs
from timeit import default_timer as timer

def collect_words(topic='0', path='data/fixed'):
    words = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == topic + '.json':
                words.extend(get_words_file(os.path.join(root, file)))
                print(str(len(words)))
    return words

def get_words_file(path):
    print('Collecting words from ' + path + '...')
    words = []
    with codecs.open(path, 'r+', 'utf-8') as f:
        for line in f:
            if line == '':
                continue
            ls = json.loads(line)
            for i in range(len(ls)):
                words.append(ls[i]['text'])
    return words

def word2vec(words, save_path):
    print('Trainning ' + save_path + '...')
    model = gensim.models.Word2Vec(words, size=100, min_count=5)
    model.save(save_path)


if __name__ == '__main__':
    data_path = 'data'
    # auto find named k.json file in data_path, output inside w2vmodel/k.w2v
    for i in range(18):
        if not os.path.exists('w2vmodel'):
            os.mkdir('w2vmodel')
        word2vec(collect_words(str(i), path='data/fixed'), os.path.join('w2vmodel', str(i) + '.w2v'))
