import os
import os.path as path

import codecs

from Popularity.word2vecTraining import collect_words, get_words_file, word2vec
from Popularity.textrank import get_cosine, text_rank
from Popularity.popularity import pop_calc

class TRTF():
    def __init__(self, data_root, file_name):
        self.droot = data_root
        self.fname = file_name

    def train_w2v(self):
        # word2vec model will be saved in Popularity/w2vmodel
        word2vec(collect_words(self.fname, path=self.droot), os.path.join('w2vmodel', self.fname.replace('.json','.w2v')))

    def textRank(self):
        for root, dirs ,files in os.walk(self.droot):
            for file in files:
                if file == self.fname:
                    print('Text Ranking ' + path.join(root, file) + ' ...')
                    text_rank(model_path=path.join('w2vmodel', file.replace('.json','.w2v')),
                              wiki_path=path.join('w2vmodel','wiki', 'wiki.w2v'),
                              json_path=path.join(root, file),
                              save_path=path.join(root, file.replace('.json', '.wordtr')))

    def get_pop(self):
        pop_calc(init_fname=self.fname, data_path=self.droot)

    def run(self):
        print('Training Word2vec Model ...')
        self.train_w2v()
        print('Text Rank Processing ...')
        self.textRank()
        # print('Calculating Population ...')
        # self.get_pop()


trtf_test = TRTF(data_root='../Datasets/Sources/testlong', file_name='0_processed.json')
trtf_test.run()
