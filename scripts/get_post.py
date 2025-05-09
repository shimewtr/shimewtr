import tweepy
import os  # osモジュールをインポート

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

if not BEARER_TOKEN:
    print("エラー: 環境変数 X_BEARER_TOKEN が設定されていません。")
    exit()

client = tweepy.Client(bearer_token=BEARER_TOKEN)

username = "shimewtr"

try:
    # ユーザーIDを取得
    user_response = client.get_user(username=username)
    if user_response.data:
        user_id = user_response.data.id

        # ユーザーのタイムラインからツイートを取得 (リツイートとリプライを除外)
        response = client.get_users_tweets(
            id=user_id,
            max_results=1,  # 念のため少し多めに取得してフィルタリング
            exclude=["retweets", "replies"]
        )

        if response.data:
            latest_tweet = response.data[0]
            print(f"ユーザー名: @{username}")
            print(f"最新のツイート: {latest_tweet.text}")
            print(f"ツイートID: {latest_tweet.id}")
            print(f"作成日時: {latest_tweet.created_at}")
        else:
            print(f"@{username} のツイートが見つかりませんでした（リツイート・リプライを除く）。")
    else:
        print(f"ユーザー @{username} が見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
