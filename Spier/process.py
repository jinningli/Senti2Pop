import json
import codecs
import os

import re
import nltk
from nltk import tokenize


def get_time(s):
    monthdic = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
               'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
               'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12',
               'Sept': '09'
               }
    y = s[len(s)-4:len(s)]
    m = monthdic[s[4: 7]]
    d = s[7:11].replace(' ', '')
    t = str(re.search(r'..:..:..', s).group(0)).replace(':', '')
    return y+m+d+t

def clean_text(s):
    s = ''.join(x for x in s if ord(x) < 256) # clean not English and emoji
    s += ' '
    s = re.sub(r'RT \@(\w*)\: ', '', s) # clean RT @...:
    s = re.sub(r'\@(\w*)[ \n\!\.\,\;]', '', s) # clean @...:
    s += ' '
    s = re.sub(r'https:\/\/([\w\.\/]*)[ \n\!\.\,\;]', '', s) # clean URL
    s = re.sub(r'http:\/\/([\w\.\/]*)[ \n\!\.\,\;]', '', s)  # clean URL
    s += ' '
    s = re.sub(r'\#(\w*)[ \,\.\!\;\n]', '', s)
    s = s.replace('\n', '')
    # print(s)
    return s

def find_emoji(s):
    s = ''.join(x for x in s if ord(x) > 8239)
    res = []
    for c in s:
        if not res.count(c):
            res.append(c)
    return res

def get_stopword_list(path = 'dic/stopwords.txt'):
    res = []
    with codecs.open(path, 'r', 'utf-8') as file:
        for line in file:
            if line != '':
                res.append(line.replace('\n', ''))
    return res

def parse_text(s, stem=False):
    word_list = tokenize.word_tokenize(s)
    word_list = [w.lower() for w in word_list]
    # english_stopwords = nltk.corpus.stopwords.words("english")
    english_stopwords = get_stopword_list()
    english_punctuations = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '...', '``',
                            '[', '{', ']', '}', ';', ':', '\'', '\"', ',', '<', '.', '>', '/', '?', '\\', '|', '`', '\'\'', '--', '__']
    res = []
    for w in word_list:
        if w not in english_stopwords and w not in english_punctuations:
            res.append(w)
    if stem:
        st = nltk.stem.porter.PorterStemmer()
        res = [st.stem(word) for word in res]

    # print(res)
    return res

def get_info(tw):
    res = {}
    res['time'] = int(get_time(tw['created_at'])) # obtain standardized time
    try:
        res['reply'] = int(tw['quoted_status']['reply_count']) # obtain reply count
        res['retweet'] = int(tw['quoted_status']['retweet_count']) # obtain retweet count
        res['favorite'] = int(tw['quoted_status']['favorite_count']) # obtain favorite count
    except:
        res['reply'] = int(tw['reply_count'])  # obtain reply count
        res['retweet'] = int(tw['retweet_count'])  # obtain retweet count
        res['favorite'] = int(tw['favorite_count'])  # obtain favorite count

    text = tw['text'] # obtain text
    try:
        text += ' ' + tw['retweeted_status']['extended_tweet']['full_text']
    except:
        pass
    # print(text)

    res['emoji'] = find_emoji(text) # find emoji list
    cleaned = clean_text(text).rstrip() # clean text
    # print(cleaned)
    wordlist = parse_text(cleaned) # Parse
    res['text'] = wordlist
    # print()
    if res['text'] == '' and len(res['emoji'])==0:
        return None
    return res


def load_raw_topic_list(path):
    print('Processing file: ' + path + '...')
    # nltk.download('stopwords')
    with open(path, 'a+') as file:
        file.write(']')
    tweets_data = [] # store the dic for each tweet
    data_list = json.load(open(path, 'r+'))
    cnt = 0
    for tweet in data_list:
        cnt += 1
        if cnt % 1000 == 0:
            print(str(cnt))
        try:
            if tweet['lang'] != 'en' and tweet['lang']!='en-gb':
                # print('Skip not English: ' + path + '[' + str(cnt) + ']')
                continue
        except:
            continue
        res = get_info(tweet)
        if res is not None:
            tweets_data.append(res)
    print('Process Finished! Total: ' + str(len(tweets_data)) + '/' + str(cnt))
    return tweets_data

def evaluate(js):
    print('Analysis:')
    ls = []
    for tw in js:
        ls += tw['text']
    from collections import Counter
    words_counter = Counter(ls)
    print(words_counter.most_common(20))

def processDir(d=''):
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.find('.json') == -1:
                continue
            if file == 'trends.txt' or file == '.DS_Store' or file == 'log.txt':
                continue
            processFile(os.path.join(root, file), os.path.join(root, file.replace('.json', '_.json')))

def processFile(inpath, outpath):
    raw_data = load_raw_topic_list(inpath)
    evaluate(raw_data)
    with codecs.open(outpath, 'w+', 'utf-8') as f:
        f.write(json.dumps(raw_data))

# for root, dirs, files in os.walk(os.getcwd()):
#     for dir in dirs:
#         if dir.find('2018') == -1:
#             continue
#         processDir(os.path.join(root, dir))

# processDir('text')
