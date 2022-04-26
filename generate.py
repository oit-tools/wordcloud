import MeCab
from wordcloud import WordCloud
import datetime
import re
import tweepy
import os
from dotenv import load_dotenv
import unicodedata


def get_tweets():
    word_list = list()
    token = None
    count = 0
    client = tweepy.Client(bearer_token=os.environ["BT"])
    NG = ["人", "こと", "時間", "やつ", "日", "時", "分", "ない", "気", "今","ー"]
    # TWITTER_LIST_ID = "1238737475306020865" # oit(たぶん枚方のみ)
    OITWC_LIST_ID = "1516921724033728512"  # OIT
    GET_TWEET_LIMIT = 100  # 取得するツイートの上限

    while True:
        tweets = client.get_list_tweets(
            id=OITWC_LIST_ID, pagination_token=token)

        for i in range(len(tweets[0])):
            text = (tweets[0][i].text)
            text = unicodedata.normalize("NFKC", text)  # 正規化
            if "RT" in text:  # リツイートを除外
                continue
            for ng in NG:
                text = re.sub(ng, "", text)  # NGワードを除外
            text = re.sub(r"[\n\u3000]", "", text)  # 改行と全角スペースを除外
            text = re.sub(r"http\S+", "", text)  # URLを除外
            text = re.sub(r"@\S+", "", text)  # @を除外
            text = re.sub(r"#\S+", "", text)  # #を除外
            count += 1  # ツイート数のカウント

            # 形態素解析
            text_list = word_analysis(text)

            # 単語の重複排除
            text_list = list(set(text_list))

            # リストに追加
            word_list.extend(text_list)

            # ツイート取得数が上限に達したらループを抜ける
            if count >= GET_TWEET_LIMIT:
                break

        # ツイート取得数が上限に達していない場合は次のページを取得
        try:
            token = ((tweets[3])["next_token"])
        except KeyError:
            break

    # リストを1つの文字列に変換
    word = " ".join(word_list)

    return word, count


# 形態素解析
def word_analysis(text):
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

    return word_list


def main():
    load_dotenv()
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"
    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")

    word, count = get_tweets()

    # Word Cloud
    wc = WordCloud(font_path=FONT_PATH, background_color="black",
                   prefer_horizontal=0.85, colormap="Set3",
                   collocations=False, height=1080, width=1920).generate(word)
    wc.to_file("./img/" + DATE + ".png")

    return count


if __name__ == "__main__":
    main()
