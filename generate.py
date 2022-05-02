import MeCab
from wordcloud import WordCloud
import datetime
import re
import tweepy
import os
from dotenv import load_dotenv
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tweets():
    word_list = list()
    token = None
    count = 0
    client = tweepy.Client(bearer_token=os.environ["BT"])
    # TWITTER_LIST_ID = "1238737475306020865" # oit(たぶん枚方のみ)
    OITWC_LIST_ID = "1516921724033728512"  # OIT
    GET_TWEET_LIMIT = 150  # 取得するツイートの上限

    while True:
        tweets = client.get_list_tweets(
            id=OITWC_LIST_ID, pagination_token=token)

        for i in range(len(tweets[0])):
            text = (tweets[0][i].text)
            text = unicodedata.normalize("NFKC", text)  # 正規化
            if "RT" in text:  # リツイートを除外
                continue
            # 改行、全角スペース、URL、メンション、ハッシュタグを除外
            text = re.sub(r"\n|\u3000|http\S+|@\S+|#\S+", "", text)

            # 形態素解析
            text_list = word_analysis(text)

            # 単語の重複排除
            text_list = list(set(text_list))

            # リストを1つの文字列に変換
            word = " ".join(text_list)

            # もし単語が空ならば次のツイートへ
            if word == "":
                continue

            # リストに追加
            word_list.append(word)

            # ツイート取得数が上限に達したらループを抜ける
            count += 1
            if count >= GET_TWEET_LIMIT:
                break

        # ツイート取得数が上限に達していない場合は次のページを取得
        try:
            token = ((tweets[3])["next_token"])
        except KeyError:
            break

    return word_list, count


# 形態素解析
def word_analysis(text):
    parse = MeCab.Tagger().parse(text)
    lines = parse.splitlines()
    word_list = list()
    HINSHI = ["名詞", "形容詞", "形容動詞"]

    for line in lines:
        item = re.split("[\t,]", line)
        # 名詞のみ保存
        if (len(item) >= 2 and item[1] not in HINSHI) or item[0] == "EOS":
            continue
        word_list.append(item[0])

    return word_list


# TF-IDFの計算
def tfidf(word_list):
    vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u"(?u)\\b\\w+\\b")
    vec = vectorizer.fit_transform(word_list)
    vec_list = list()

    for i in range(len(vec.toarray())):
        vec_sum = sum(vec.toarray()[i])
        vec_list.append(vec_sum)

    word = dict(zip(vectorizer.get_feature_names_out(), vec_list))

    return word


# WordCloudの生成
def wordcloud(word):
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"
    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")
    NG = ["人", "こと", "時間", "やつ", "日", "時", "分", "ない", "気", "今"]
    wc = WordCloud(font_path=FONT_PATH, background_color="black",
                   prefer_horizontal=0.85, colormap="Set3",
                   collocations=False, height=1080, width=1920,
                   stopwords=set(NG)).generate_from_frequencies(word)
    wc.to_file("./img/" + DATE + ".png")


def main():
    # 環境変数の読み込み
    load_dotenv()

    word_list, count = get_tweets()
    word = tfidf(word_list)
    wordcloud(word)

    return count


if __name__ == "__main__":
    main()
