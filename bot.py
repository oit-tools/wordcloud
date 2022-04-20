import generate
import tweepy
from dotenv import load_dotenv
import os
import datetime


def post_tweet(date, api):
    # 画像のパスを取得
    img = "./img/" + date + ".png"

    # 年月日のフォーマットを変更
    date = date.replace("_0", "_")
    date = date.split("_")
    date = date[0] + "年" + date[1] + "月" + date[2] + "日" + date[3] + "時"

    # ツイート
    text = date + "のWord Cloudです"
    api.update_status_with_media(text, filename=img)


def follow_back(api):
    # フォローされているアカウントを取得
    follower_list = api.get_follower_ids(count=1000)

    # フォローされているアカウントをフォロー
    for i in range(len(follower_list)):
        api.create_friendship(user_id=follower_list[i])


def main():
    # Word Cloudを生成
    generate.main()

    # APIキーの読み込み
    load_dotenv()
    auth = tweepy.OAuthHandler(os.environ["CK"], os.environ["CS"])
    auth.set_access_token(os.environ["AT"], os.environ["AS"])
    api = tweepy.API(auth)

    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")

    post_tweet(DATE, api)
    follow_back(api)


if __name__ == "__main__":
    main()
