import MeCab
from wordcloud import WordCloud
import datetime
import re
import tweepy
import os
from dotenv import load_dotenv
import unicodedata


def get_list_tweet():
    tweet_list = list()
    token = None
    client = tweepy.Client(bearer_token=os.environ["BT"])
    NG = ["人", "こと", "時間", "やつ", "日", "時", "分", "ない"]
    TWITTER_LIST_ID = "1238737475306020865"

    while True:
        tweets = client.get_list_tweets(
            id=TWITTER_LIST_ID, pagination_token=token)

        for i in range(len(tweets[0])):
            data = (tweets[0][i].text)
            if "RT" in data:  # RTを除外
                continue
            for ng in NG:
                data = re.sub(ng, "", data)  # NGワードを除外
            data = re.sub(r"[\n\u3000]", "", data)  # 改行と全角スペースを除外
            data = re.sub(r"http\S+", "", data)  # URLを除外
            data = re.sub(r"@\S+", "", data)  # @を除外
            data = re.sub(r"#\S+", "", data)  # #を除外
            tweet_list.append(data)

            if len(tweet_list) >= 100:
                break

        try:
            token = ((tweets[3])["next_token"])
        except KeyError:
            break

    tweet = " ".join(tweet_list)
    count = len(tweet_list)

    return tweet, count


# 形態素解析
def get_word(text):
    parse = MeCab.Tagger().parse(text)
    lines = parse.splitlines()
    word_list = list()
    HINSHI = ["名詞", "形容動詞", "形容詞"]

    for line in lines:
        item = re.split("[\t,]", line)
        # 名詞のみ保存
        if (len(item) >= 2 and item[1] not in HINSHI) or item[0] == "EOS":
            continue
        word_list.append(item[0])

    word = " ".join(word_list)

    return word


def main():
    load_dotenv()
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"
    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")

    tweet, count = get_list_tweet()
    text = unicodedata.normalize("NFKC", tweet)
    word = get_word(text)

    # Word Cloud
    wc = WordCloud(font_path=FONT_PATH, background_color="black",
                   prefer_horizontal=0.85, scale=4, colormap="Set3",
                   collocations=False).generate(word)
    wc.to_file("./img/" + DATE + ".png")

    return count


if __name__ == "__main__":
    main()
