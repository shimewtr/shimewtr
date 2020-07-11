# -*- coding: utf-8 -*-
import emoji
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from janome.tokenizer import Tokenizer
from PIL import Image
from requests_oauthlib import OAuth1Session
from wordcloud import WordCloud

CK = os.environ['API_KEY']
CS = os.environ['API_SECRET_KEY']
AT = os.environ['ACCESS_TOKEN']
ATS = os.environ['ACCESS_TOKEN_SECRET']
FONT_PATH = os.environ['FONT_PATH']
SCREEN_NAME = os.environ['GITHUB_ACTOR']


def generate_exclude_list():
    exclude_list = []
    f = open(os.path.join(
        os.path.dirname(__file__), "exclude_words.txt"), "r")
    for line in f:
        exclude_list.append(line.rstrip("\n"))
    f.close()
    return exclude_list


def generate_word_cloud(words):
    text = ' '.join(words)
    fpath = FONT_PATH

    x, y = np.ogrid[:450, :900]
    mask = ((x - 225) ** 2 / 5 ** 2) + ((y - 450) ** 2 / 10 ** 2) > 40 ** 2
    mask = 255 * mask.astype(int)

    wordcloud = WordCloud(background_color="white",
                          colormap="Greys",
                          font_path=fpath,
                          mask=mask
                          ).generate(text)
    wordcloud.to_file(os.path.join(
        os.path.dirname(__file__), "word_cloud.png"))


def get_tweets():
    twitter = OAuth1Session(CK, CS, AT, ATS)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 200,
        'exclude_replies': True,
        'include_rts': False,
        'screen_name': SCREEN_NAME,
    }
    req = twitter.get(url, params=params)

    if req.status_code == 200:
        tweets = []
        res = json.loads(req.text)
        for line in res:
            tweets.append(remove_emoji(line['text']))
    else:
        print("Failed Status Code: %d" % req.status_code)
        sys.exit()
    return tweets


def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)


def word_count(texts, exclude_list):
    t = Tokenizer()
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                if token.base_form not in exclude_list:
                    words.append(token.base_form)
    return words


def main():
    tweets = get_tweets()
    exclude_list = generate_exclude_list()
    words = word_count(tweets, exclude_list)
    generate_word_cloud(words)


if __name__ == '__main__':
    main()
