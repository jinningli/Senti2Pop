from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import codecs
import sys
import math
import json
import os
from process import *

def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)

class StdOutListener(StreamListener):

    def __init__(self, sp, thd=0, di=0, keyword=None):
        super(StreamListener, self).__init__()
        self.savepath = sp
        self.cnt = 0
        self.thread = thd
        self.dicind = di
        self.keyword = keyword

    def on_data(self, data):
        if not os.path.exists(self.savepath):
            with open(self.savepath,'a+') as file:
                file.write('[{}')
        with open(self.savepath,'a+') as file:
            file.write(',\n' + data + '\n')
            self.cnt += 1
        if self.cnt % 50 == 0:
            print("[" + str(self.thread) + ':' + str(self.dicind) + "]  " + self.savepath + ' :' + str(self.cnt))
        return True

    def on_error(self, status):
        if status == 420:
            #returning False in on_data disconnects the stream
            return False

class Spider():

    def get_trends(self):
        api = tweepy.API(self.authList[0])
        trends = api.trends_place(23424977)
        names = []
        trends = trends[0]['trends']
        for i in range(len(trends)):
            names.append(trends[i]['name'].replace('#', ''))
        return names

    def set_threads(self, dir, keywords, alloc=2):
        # each thread support 2
        # dir: save path
        # self.dic: list of keywords
        l = len(keywords)

        for i in range(self.thread_max):
            for j in range(alloc):
                if i * alloc + j >= l:
                    continue
                self.threads[i * alloc + j] = Stream(self.authList[i], StdOutListener(sp=os.path.join(dir, str(i) + '.json'), thd=i, di=i * alloc + j, keyword=keywords[i * alloc + j]))
                print('Thread: ' + str(i) + " listening " + str(keywords[i * alloc + j]))
                with codecs.open(os.path.join(dir, 'log.txt'), 'a+', 'utf-8') as file:
                    file.write(time.strftime("%Y-%m-%d_%H-00", time.localtime()))
                    file.write('Thread: ' + str(i) + " listening " + str(keywords[i * alloc + j]))
        self.thread_cnt = l

    def run(self):
        if self.mode == 'day':
            while True:
                self.check_time()
                makedir(os.path.join(self.save_path, self.day))
                makedir(os.path.join(self.save_path, self.day, self.hour))

                # preprocess
                for root, dirs, files in os.walk(self.save_path):
                    for file in files:
                        if file.find('.json') == -1:
                            continue
                        if file.find('_processed') != -1:
                            continue
                        processFile(os.path.join(root, file), os.path.join(root, file.replace('.json', '_processed.json')))
                        os.remove(os.path.join(root, file))

                self.set_threads(os.path.join(self.save_path, self.day, self.hour), keywords=self.keywords, alloc=1)
                self.auto_forcing()

    def check_time(self):
        nowday = time.strftime("%Y-%m-%d", time.localtime())
        nowhour = time.strftime("%H", time.localtime())
        if nowday != self.day:
            self.day = nowday
            self.hour = nowhour
            print('Time shifted to ' + self.day + '_' + self.hour)
            return 2
        elif nowhour != self.hour:
            self.day = nowday
            self.hour = nowhour
            print('Time shifted to ' + self.day + '_' + self.hour)
            return 1
        else:
            return 0

    def auto_forcing(self):
        while(True):
            self.start_threads()
            if self.check_time() > 0:
                self.stop_threads()
                return
            time.sleep(15)

    def start_threads(self):
        for i in range(self.thread_cnt):
            if self.threads[i] != None:
                if self.threads[i].running is False:
                    self.threads[i].filter(track=self.threads[i].listener.keyword, async=True)
                    sys.stdout.write(str(self.threads[i].listener.thread) + ':' + str(i) + ' ')
        print('forced')

    def stop_threads(self):
        for i in range(self.thread_max):
            if self.threads[i] is not None:
                self.threads[i].disconnect()

    def __del__(self):
        self.stop_threads()

    def __init__(self, keywords = None, save_path=None, mode = 'day'):
        self.access_token = [
            "953622906302480384-sAUAPtAr8u77Kk5fPLaH7zOhw5pEfxR",
            "953622906302480384-O77aB4kn0MwIeSNWFVT7KsSIAt2tszi",
            "953622906302480384-x8r809eneFNRdUqHbs09rOQnaYpE03u",
            "953945723581612032-gP41vh5NBiBxduake9LVEW9qkiCVsth",
            "953945723581612032-yhqxySgEpv2nG0rSzXqxX1HkxuqUqhZ",
            "953945723581612032-CriFc87cTYMOFdi3lmmimeTJTHT1Oj6",
            "953622906302480384-zCfBnoUFkTXdTgHBoh5zQmpXeensNZz",
            "953622906302480384-ip2KiT2nYS24vHmOnfQd5kMAF4YkDTL",
            "953622906302480384-mMTvSzhyuV5XBsaTlPaWDBpPZ06eMoV",
            "886769973506342912-V4WfF7eIFGlXY2rmNrEPDcE073C57Fa",
            "886769973506342912-2BFOCqjArj2864btgaKxTavxnybu4PL",
            "953945723581612032-dfg6WX1pm3crbkuWRvYKDe3uXbWOaFW",
            "953945723581612032-u2f6aHF3Rt4VpDNVUEqcQqR7E28Pad7",
            "953945723581612032-XoOi4g4HIuJTtVJdUXrpLfuRWfAQctg",
            "953622906302480384-aytCv5ZGgwGwqHKN3upusFcfxBiUKO9",
            "953622906302480384-App8bmqFc49Yx10JkrgO0Z3olOokg5x",
            "953622906302480384-EJclxN5RLmh5hxftrhHPmZcdm7yPUkx",
            "953622906302480384-dDe0WiLG77pNRnvuA4ylJ17q7FzJ0cY",
            "953622906302480384-pvtB9KYqq4Qx7mD5t794A2zXIsCRE8O",
            "953622906302480384-Me8j2pO0z8aJAySMQ7k1DnJeSe9lidV",
            "953945723581612032-skNPLKbnRjbc9p0vihRqJzdPr99mSs0",
            "953945723581612032-JoLQjDDXllaECt9ArcZRKBq5lYZNFNA",
            "953945723581612032-kfCJZdEizPW6b0UXU0BzYnDrCsZ1Syd"
        ]

        self.access_token_secret = [
            "8ggB9Ri6xHlWwBP5Ma8d6mEPsvpOwglkAIrHpXazPlrjl",
            "olOzLdIFAMEasMcNSz4sEYqmEhem7rCH7yrjgUpm9ZVXe",
            "ljSzsc3XYE18BTWLmLjQeoA1qd5Ruzdrnhq03qBPAIgbD",
            "JfWR0KefDyXnkpvhu3ygrrnLMlCf9olaeEiNoIFCBQJ8D",
            "gXrbkebTk9wuM0lfymLVbpwFmt8TQMKTDyE2602naCQOe",
            "r7aOx3xiURDng6ro9BJ97yEGmiGYITXu3VDsTbjDgwVSR",
            "C8DQnlXl7RqNZNJCyJANrPuB8ZeF56ha9EGdK6rusdEdF",
            "jcFAF4Q5KAkjzRJigAjgNWgEkY0rySNtiADUhP3ILbLqg",
            "gQJidn2jmWhxnhiXU1v3PT16vO6vLdGMGmZssHE1aZILG",
            "bVEoAyZEQ9X0sNjMzZz8dwwN5GHWZC0v4dEfguDuFoIKq",
            "xst8lcAAPi91LPV6AFfy5XAgjfc7hHJk2gkcM359MciWX",
            "3cs6Xiwiismf7R9OjTlaN1otoUIypYkhGakwUzxnMl3Jb",
            "BZYLnZauX437UWDihzmUkBpivFvFcGUUlBUI3no0wFr1w",
            "SqieNTMVLQfhHnlBBBFQBLvQw0A1UQWgX39zVR9XgwTgE",
            "jORm7SKnHg0Bvh4Egg0Y0o1DS44pHDUANsfWN3vJATbJs",
            "qbWbRQE8XPCerBsIC0Vd3hBe8lLWD7XpqWxJ7i4I91VoW",
            "8uqlwt0loBJjJnsA5tVB9uk0wYR9kkHovb8Mt2QcuGQ9A",
            "0dczCno10x9XwVweuzShuQw28oqLA8xRBajYUxvRmI44Y",
            "Xr5hBeRovHMLgCIMUc4VMLQL23Mls7b6YblayZA3FDhtp",
            "IOuKsaz2bLqc5luXiuQYw7ggQNAeYoPbjOD3bCjveDLkb",
            "fOSE8wiTM6HkjCGKqFxqa8dFxtmuygE2T1aECv6IeZv0l",
            "bGyHU1fBDrpVJ8WCSVjRIO0juOcXw8BYYAzU7oireXGo9",
            "D5DJ6Getac5PAAZoWYPAtGSTt624yqtr030avCcCQsVyG"
        ]

        self.consumer_key = [
            "E3k3t0zoyyS8YUjXe67jcAMU2",
            "QvEn8Laj4Z9NKfGXCdifYaHap",
            "gAjFUz9l5flrbFwypueCjYKbw",
            "m0AK2Iwv5yeHUicLO87WpdIon",
            "3kvixWNRgpqgQjCnZgg0mdnEI",
            "ywpQEIS7rjeLOH0cHJqd19CmE",
            "b6R0YZsW1ZN2ys3z3Y7jNPqGP",
            "s7NuDuF0tGFX6YHf9oMB5chYI",
            "8vzRwe5EwinGZarScrnbSNMGw",
            "NiUvgllYc4ryJSUc4D7ceHNXU",
            "DwcqAMS6y9ygilYATfCyaRyb1",
            "33vfV41uZQkMbqiu63pEMRzDw",
            "YzIc3gv1QWZp0Ic9087eodiQd",
            "TezYFghBlsLdnovO9Ml2sLnEH",
            "rE2CagyAnjEEDkfw2ll4DlfY7",
            "E1Beldk3n5PsXCQ0ozzqKdTEa",
            "HQFkCtsfvegxlwokZp70ga8IR",
            "eta58qYzFrGaaoOOotjr9Z4G1",
            "sEbESpqHCN54cIRJaVTZ33oLD",
            "OeJG3KAEQMJst1k4vpt3pm2tk",
            "hH09IBNzT6LxTMCHUM2QUv3nT",
            "FfXA3PJn9hbnl2JAsuIvHSO0m",
            "HDwTE5siuFh81bhhqhQDj5ekh"
        ]

        self.consumer_secret = [
            "EYYUkUbtEGBQXMGaZZ29oeyrXedRdk1H9JhiqSaPRaLQOVF1Gu",
            "E7PcqVghPd5uuZsTFpiiYfxQKDRSz4HrH4BqOK5Yn30stRJ8wH",
            "suN3Jm41VHR3y5dEoKwtfAxO5ARxC42Y7ubmMMglAeT9o2Fn2S",
            "w5T2NUWw2pxjawjXwIuLhBRk1XLcVtP76WTktTwyd0dxT44hIo",
            "gkRo1cDv3QpNXzrAYgKUGH09xjI0UqRkqqA1JuDyQygokbfwKT",
            "msb9YXJQ59bCiOA0oBrqeK6w86woE1X5Kfnz7Fp7TaWtkXegDi",
            "0W9D9naHKPtSnJuP1CRZoGMI1IheiFZTmcKBcESsI6ljB7i0zH",
            "OsTli5D2K6EYqUF2sxmNPVJu6YzFiSvYtlYtVBuKjYTHeHgRXZ",
            "gZ4BMCFNZoCfhTyrZN0LTWs5ABExNm4Of44fu7AWNlzPNilztr",
            "5CntXsBctuLDN8uulNyMnWpjarPigXqEJXx1VB7XyJFRBwzMOK",
            "U1c5pacCGr3vBbB3FxApwr8OHSyhe111eJlzOWXcX38qEf8glL",
            "JaH4Kqaf6Se6b7mmkQbUizXLqgwsLlvKeHTgxHZa5Bz2uKVZIW",
            "DVFAqvuAqwkfUWaNLfomuwblbzXou6P6qPHurYuHrzWLsnA98V",
            "ECNCvAYSZF3ODJBx7vv8QlhEXDOAxvZ0c2b836Ltdk436eaM9S",
            "re8RUgeNxTNhPJNNnrNesjm8iC2DtsVqQ5fkvNwFM9Y9ZlBdW2",
            "KAlCQCIsU6Qg3hcGUX4qjFGt9NFxqr4faUvYGx3ewKlN4nV9Ds",
            "7PR3mOUi0wb9BZC5pnHTO3CgOiyEQN96NYAOhwSxu42Zc10917",
            "1L9EWsOA1tFoPqCuuEfLKX2JW4cW0h75KMQGlVZeJZdTNUT8Hn",
            "gvktOYvw7wttNPzT4KmTtEyQXyAkWLHulqQu6FUkESum8ojv1m",
            "YymyY9aWHbKvLiXyybBMprfSJUjsbXKTORn3zIObw3ol3bM5NY",
            "G24f2JKSXaZLwIPWzTEHskwiHNjsjPrcEhC2taqE7jjsaOBe99",
            "Jp3plemsvkpInNtERGd81EQI0L05jIA7NmDjfBxc900FEjAKj1",
            "lYMOM5oncCDBg7IhQWKMDj5ctLMoSh0T4jGRN9DuAZkd922cG9"
        ]

        self.daytimes = ['00', '01', '02', '03', '04', '05', '06', '07']

        # append authList
        self.authList = []
        for i in range(len(self.access_token)):
            auth = OAuthHandler(self.consumer_key[i], self.consumer_secret[i])
            auth.set_access_token(self.access_token[i], self.access_token_secret[i])
            self.authList.append(auth)

        # max thread number decided by authList
        self.thread_max = len(self.authList)

        # the cnt of running thread
        self.thread_cnt = 0
        # store the threads
        self.threads = [None for k in range(self.thread_max + 1)]

        # keywords: [[a, b, c], [d, e, f]]
        self.keywords = keywords
        self.save_path = save_path
        makedir(save_path)
        self.mode = mode
        self.hour = time.strftime("%H", time.localtime())
        self.day = time.strftime("%Y-%m-%d", time.localtime())


def read_topic(path):
    res = []
    if not os.path.exists(path):
        return res
    with codecs.open(path, 'r+', 'utf-8') as file:
        for line in file:
            s = line
            if s == '':
                continue
            s = s.replace('\n', '').replace('\r\n', '').split('; ')
            print(s)
            print('\n\n')
            res.append(s)
    return res

spider = Spider(read_topic('daytopics.txt'), 'text', 'day')
spider.run()
