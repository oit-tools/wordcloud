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
    client = tweepy.Client(bearer_token=os.environ["BT"])
    NG = ["人", "こと", "時間", "やつ"]

    while True:
        tweets = client.get_list_tweets(
            id="1238737475306020865", pagination_token=token)

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

    for line in lines:
        item = re.split("[\t,]", line)
        # 名詞のみ保存
        if (len(item) >= 2 and item[1] != "名詞") or item[0] == "EOS":
            continue
        word_list.append(item[0])

    word = " ".join(word_list)

    return word


def post_tweet(date, api, count):
    # 画像のパスを取得
    img = "./img/" + date + ".png"

    # 年月日のフォーマットを変更
    date = date.replace("_0", "_")
    date = date.split("_")
    date = date[0] + "年" + date[1] + "月" + date[2] + "日" + date[3] + "時"

    # ツイート
    text = date + "のWord Cloudです\n" + str(count) + "件のツイートを解析しました"
    api.update_status_with_media(text, filename=img)


def follow_back(api):
    # フォローしているユーザーを取得
    follower_list = api.get_follower_ids(count=1000)

    # フォローしているユーザーをフォロー
    for i in range(len(follower_list)):
        api.create_friendship(user_id=follower_list[i])


def main():
    load_dotenv()
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"
    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")
    # Twitter
    auth = tweepy.OAuthHandler(os.environ["CK"], os.environ["CS"])
    auth.set_access_token(os.environ["AT"], os.environ["ATS"])
    api = tweepy.API(auth)

    data, count = get_tweet()
    text = unicodedata.normalize("NFKC", data)
    word = get_word(text)

    # Word Cloud
    wc = WordCloud(font_path=FONT_PATH, background_color="black",
                   prefer_horizontal=0.7, scale=4, colormap="Set3").generate_from_text(word)
    wc.to_file("./img/" + DATE + ".png")

    # post_tweet(DATE, api, count)
    # follow_back(api)


if __name__ == "__main__":
    main()
