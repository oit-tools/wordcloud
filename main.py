import MeCab
from wordcloud import WordCloud
import datetime
import re
import tweepy
import os
from dotenv import load_dotenv
import unicodedata


def get_tweet():
    tweet_list = list()
    token = None
    flag = False

    client = tweepy.Client(bearer_token=os.environ["BEARER_TOKEN"])
    while flag is False:
        tweets = client.get_list_tweets(
            id="1238737475306020865", pagination_token=token)

        for j in range(len(tweets[0])):
            data = (tweets[0][j].text)
            if "RT" in data:  # RTを除外
                continue
            data = re.sub(r"[\n\u3000]", "", data)  # 改行と全角スペースを除外
            data = re.sub(r"http\S+", "", data)  # URLを除外
            data = re.sub(r"@\S+", "", data)  # @を除外
            data = re.sub(r"#\S+", "", data)  # #を除外
            tweet_list.append(data)

        try:
            token = ((tweets[3])["next_token"])
        except KeyError:
            flag = True

    tweet = " ".join(tweet_list)

    return tweet


def get_word(text):
    mecab = MeCab.Tagger()
    parse = mecab.parse(text)

    # 形態素解析
    word_list = list()
    lines = parse.splitlines()
    for line in lines:
        items = re.split("[\t,]", line)
        # 名詞のみ保存
        if (len(items) >= 2 and items[1] != "名詞") or items[0] == "EOS":
            continue
        word_list.append(items[0])

    word = " ".join(word_list)

    return word


def main():
    load_dotenv()
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"
    DATE = datetime.datetime.now().strftime("%Y_%m_%d")

    data = get_tweet()
    text = unicodedata.normalize("NFKC", data)
    word = get_word(text)

    # Word Cloud
    wc = WordCloud(font_path=FONT_PATH, width=1000, height=800,
                   background_color="black").generate(word)
    wc.to_file("./img/" + DATE + ".png")


if __name__ == "__main__":
    main()
