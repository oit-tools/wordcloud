# OIT Word Cloud

generate.pyでWord Cloudを生成し、bot.pyで自動投稿を行います。  
bot.pyを動作させるためにはTwitter API v1(Elevated Access)が必要です。  

**各自でBearer tokenを用意してください**  
[Twitter API v2の申請とBearer tokenの取得方法](https://wporz.com/twitterapi-apikey-accesstoken/)

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
py ./generate.py
```

generate.pyを動作させるとツイートを自動で取得し、形態素解析した後Word Cloudが./img内に画像として生成される。  

## Misc

Tweetの取得は
[Tweepy](https://github.com/tweepy/tweepy)
を使用し、取得先のリストは
[これ](https://twitter.com/i/lists/1238737475306020865)
を利用。  
形態素解析は
[MeCab](https://github.com/taku910/mecab)
と
[UniDic](https://clrd.ninjal.ac.jp/unidic/)
を使用。  
Word Cloud生成には
[Word Cloud](https://github.com/amueller/word_cloud)
を使用し、フォントには
[UDEV Gothic](https://github.com/yuru7/udev-gothic)
を使用。
