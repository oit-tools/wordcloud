import MeCab
from wordcloud import WordCloud
import uuid
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
    # TWITTER_LIST_ID = "1238737475306020865" # oit(たぶん枚方のみ)
    OITWC_LIST_ID = "1516921724033728512"  # OIT

    while True:
        tweets = client.get_list_tweets(
            id=OITWC_LIST_ID, pagination_token=token)

        for i in range(len(tweets[0])):
            # ツイートの文字列を取得
            text = (tweets[0][i].text)
            # 正規化
            text = unicodedata.normalize("NFKC", text)
            # リツイートを除外
            if "RT" in text:
                continue
            # 改行、全角スペース、URL、メンション、ハッシュタグを除外
            text = re.sub(r"\n|\u3000|http\S+|@\S+|#\S+", "", text)
            # 形態素解析
            text_list = word_analysis(text)
            # 単語の重複排除
            text_list = list(set(text_list))
            # 空の要素を削除
            if len(text_list) == 0:
                continue
            # リストに追加
            word_list.extend(text_list)
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
    # パーサーを作成
    parse = MeCab.Tagger().parse(text)
    # 改行で分割
    lines = parse.splitlines()
    word_list = list()
    # 残したい品詞を指定
    HINSHI = ["名詞", "形容詞", "形容動詞"]

    for line in lines:
        item = re.split("[\t,]", line)
        if (len(item) >= 2 and item[1] not in HINSHI) or item[0] == "EOS":
            continue
        word_list.append(item[0])

    return word_list


# Word Cloud
def wordcloud(word, path):
    # フォントを指定
    FONT_PATH = "./font/UDEVGothic-Bold.ttf"

    # NGワードを指定
    NG = ["人", "こと", "時間", "やつ", "日", "時", "分", "ない", "気", "今", "いい", "笑", "笑笑", "匿名", "募集", "みんな", "質問"]

    wc = WordCloud(font_path=FONT_PATH, background_color="black",
                   prefer_horizontal=0.85, colormap="Set3",
                   collocations=False, height=1080, width=1920,
                   stopwords=set(NG)).generate(word)
    wc.to_file("./img/" + path + ".png")


def main():
    # 環境変数の読み込み
    load_dotenv()

    path = str(uuid.uuid4())

    # ツイートの取得とWord Cloudの生成
    word, count = get_tweets()
    wordcloud(word, path)

    return count, path


if __name__ == "__main__":
    main()
