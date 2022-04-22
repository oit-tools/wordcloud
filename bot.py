import generate
import tweepy
from dotenv import load_dotenv
import os
import datetime


def post_tweet(count, date, api):
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
    # フォローされているアカウントを取得
    follower_list = api.get_follower_ids(count=1000)

    # フォローされているアカウントをフォロー
    for i in range(len(follower_list)):
        try:
            api.create_friendship(user_id=follower_list[i])
        except tweepy.errors.Forbidden:
            continue


def add_list():
    OITWORDCLOUD_ID = "1516397750317117441"
    OIT_LIST_ID = "1516921724033728512"
    client = tweepy.Client(bearer_token=os.environ["BT"], consumer_key=os.environ["CK"],
                           consumer_secret=os.environ["CS"], access_token=os.environ["AT"],
                           access_token_secret=os.environ["AS"])
    following_list = list()
    member_list = list()

    # フォローしているアカウントのIDを取得
    following = client.get_users_following(id=OITWORDCLOUD_ID)
    for i in range(len(following[0])):
        following_list.append(following[0][i].id)

    # リストのメンバーのIDを取得
    member = client.get_list_members(id=OIT_LIST_ID)
    for i in range(len(member[0])):
        member_list.append(member[0][i].id)

    # フォローしているアカウントがリストに含まれていない場合はリストに追加
    unlisted = list(set(following_list) - set(member_list))

    # リストに追加
    for i in range(len(unlisted)):
        client.add_list_member(id=OIT_LIST_ID, user_id=unlisted[i])


def main():
    # Word Cloudを生成
    count = generate.main()

    # APIキーの読み込み
    load_dotenv()
    auth = tweepy.OAuthHandler(os.environ["CK"], os.environ["CS"])
    auth.set_access_token(os.environ["AT"], os.environ["AS"])
    api = tweepy.API(auth)

    DATE = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=+9))).strftime("%Y_%m_%d_%H")

    post_tweet(count, DATE, api)
    # follow_back(api)
    # add_list()


if __name__ == "__main__":
    main()
