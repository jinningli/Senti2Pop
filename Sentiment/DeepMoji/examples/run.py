# -*- coding: utf-8 -*-

""" Use DeepMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the DeepMoji repo.

Writes the result to a csv file.
"""

from __future__ import print_function, division
import json
import numpy as np
import os
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.model_def import deepmoji_emojis
import codecs
import os.path as path

OUTPUT_PATH = 'test_sentences.csv'

emoji_list=[u'😂',u'😒',u'😩',u'😭',u'😍',u'😔', u'👌', u'😊',u'❤️',u'️😏',
            u'😁',u'🎶',u'😳',u'💯',u'😴',u'😌',u'☺',u'🙌',u'💕',u'😑',u'😅',u'🙏',
            u'😕',u'😘',u'♥',u'😐',u'💁',u'️😞',u'🙈',u'😫',u'✌',
            u'😎',u'😡',u'👍',u'😢',u'😪',u'😝',u'😤',u'✋',u'😷',u'👏',
            u'👀',u'🔫',u'😣',u'😈',u'😓',u'💔',u'♥',u'🎧',u'🙊',u'😉',u'💀',u'😖',
            u'😄',u'😜',u'😠',u'🙅',u'💪',u'👊',u'💜',u'💖',u'💙',u'😬',u'✨']

emoji2num={c:emoji_list.index(c) for c in emoji_list}

def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

def emoji_predict(sen_list, maxlen=30, step = 32, model_path='../model/deepmoji_weights.hdf5', vocab_path='../model/vocabulary.json'):
    model = deepmoji_emojis(maxlen, model_path)
    model.summary()

    with open(vocab_path, 'r') as f:
        vocabulary = json.load(f)
    st = SentenceTokenizer(vocabulary, maxlen, ignore_sentences_with_only_custom=True)
    records = []

    for i in range(0, len(sen_list), step):
        if i + step >= len(sen_list):
            tokenized, _, _ = st.tokenize_sentences(sen_list[i:len(sen_list)])
            content = sen_list[i:len(sen_list)]
            if len(tokenized) != len(content):
                print('Skip ' + str(i))
                continue
        else:
            tokenized, _, _ = st.tokenize_sentences(sen_list[i:i+step])
            content = sen_list[i:i+step]
            if len(tokenized) != len(content):
                print('Skip ' + str(i))
                continue
        prob = model.predict(tokenized)
        for j in range(len(content)):
            r = {}
            r['text'] = [content[j]]
            t_prob = prob[j]
            ind_top = top_elements(t_prob, 5)
            r['confidence'] = (str(sum(t_prob[ind_top])))
            r['top5emoji'] = [unicode(emoji_list[ind]) for ind in ind_top]
            r['top5prob'] = [str(t_prob[ind]) for ind in ind_top]
            r['prob'] = [str(num) for num in t_prob]
            records.append(r)
        if i % 1024 == 0:
            print('Processing: ' + str(i) + '/' + str(len(sen_list)))

    return records


def predict(data_path):
    for root, dirs, files in os.walk(data_path):
        for dir in dirs:
            for i in range(18):
                sens = []
                with codecs.open(path.join(root, dir, str(i) + '.json')) as f:
                    print('Processing: ' + path.join(root, dir, str(i) + '.json'))
                    s = f.readline()
                    ls = json.loads(s)
                    for content in ls:
                        words = content['text']
                        st = ''
                        for c in words:
                            st += ' ' + c
                        sens.append(unicode(st))
                rec = emoji_predict(sens)
                with codecs.open(path.join(root, dir, str(i) + '_emotion.json'), 'w+', 'utf-8') as f:
                    f.write(json.dumps(rec))

predict('../../data/fixed')