# OIT WordCloud

generate.pyでWordCloudを生成し、bot.pyで自動投稿を行います。  
以下の記事を参考にTwitter Developerアカウントの登録をしてください。  
[【2022年】TwitterAPI v2 の仕様まとめ・セットアップ方法](https://zenn.dev/mamushi/articles/twitter_api_v2_setup#2.-developer-%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E7%99%BB%E9%8C%B2%EF%BC%88essential%E5%88%A9%E7%94%A8%EF%BC%89=)

bot.pyを動作させるためにはTwitter API v1(Elevated Access)が必要です。  
[先程の記事](https://zenn.dev/mamushi/articles/twitter_api_v2_setup#3.-elevated-%E3%83%97%E3%83%A9%E3%83%B3%E3%81%B8%E3%81%AE%E3%82%A2%E3%83%83%E3%83%97%E3%82%B0%E3%83%AC%E3%83%BC%E3%83%89%E6%96%B9%E6%B3%95=)
を参考に申請してください。

## Usage

必要に応じてvenv作成

```bash
pip install -r requirements.txt
```

UniDicをダウンロードする

```bash
python -m unidic download
```

generate.pyと同じディレクトリに```.env```ファイルを作成  
```.env```ファイルに  

```text
BT=取得したBearer token
```

を記入し保存する。

```bash
python ./generate.py
```

generate.pyを動作させるとツイートを自動で取得し、形態素解析した後Word Cloudが./img内に画像として生成される。  

## Misc

Tweetの取得は
[Tweepy](https://github.com/tweepy/tweepy)
を使用し、取得先のリストは
[これ](https://twitter.com/i/lists/1516921724033728512)
を利用。  
形態素解析は
[MeCab](https://github.com/taku910/mecab)
と
[UniDic](https://clrd.ninjal.ac.jp/unidic/)
を使用。  
WordCloud生成には
[WordCloud](https://github.com/amueller/word_cloud)
を使用し、フォントには
[UDEV Gothic](https://github.com/yuru7/udev-gothic)
を使用。
