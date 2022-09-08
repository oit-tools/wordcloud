import generate
import tweepy
from dotenv import load_dotenv
import os
import datetime


def post_tweet(count, path, api):
    # 画像のパスを取得
    img = f"./img/{path}.png"

    # # 年月日と時刻を取得
    # date = datetime.datetime.now(datetime.timezone(
    #     datetime.timedelta(hours=+9))).strftime("%Y年%m月%d日%H時")
    # # テキストを生成
    # text = date + "のWordCloudです\n" + str(count) + "件のツイートを解析しました"

    # ツイート
    api.update_status_with_media(filename=img)


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
    OITWC_ACCOUNT_ID = "1516397750317117441"
    OITWC_LIST_ID = "1516921724033728512"
    client = tweepy.Client(bearer_token=os.environ["BT"], consumer_key=os.environ["CK"],
                           consumer_secret=os.environ["CS"], access_token=os.environ["AT"],
                           access_token_secret=os.environ["AS"])
    following_list = list()
    member_list = list()

    # フォローしているアカウントのIDを取得
    following = client.get_users_following(id=OITWC_ACCOUNT_ID)
    for i in range(len(following[0])):
        following_list.append(following[0][i].id)

    # リストのメンバーのIDを取得
    member = client.get_list_members(id=OITWC_LIST_ID)
    for i in range(len(member[0])):
        member_list.append(member[0][i].id)

    # フォローしているアカウントがリストに含まれていない場合はリストに追加
    unlisted = list(set(following_list) - set(member_list))

    # リストに追加
    for i in range(len(unlisted)):
        client.add_list_member(id=OITWC_LIST_ID, user_id=unlisted[i])


def main():
    # Word Cloudを生成し、解析ツイート数を取得
    count, path = generate.main()

    # APIキーの読み込み
    load_dotenv()
    auth = tweepy.OAuthHandler(os.environ["CK"], os.environ["CS"])
    auth.set_access_token(os.environ["AT"], os.environ["AS"])
    api = tweepy.API(auth)

    post_tweet(count, path, api)
    # follow_back(api) # 現在不使用
    add_list()


if __name__ == "__main__":
    main()
