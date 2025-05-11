import base64
import re
import openai
import os
import tweepy


def get_latest_tweet():
    BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
    USER_NAME = "shimewtr"

    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    user_response = client.get_user(username=USER_NAME)
    user_id = user_response.data.id
    response = client.get_users_tweets(
        id=user_id,
        max_results=5,  # 5~100を指定する必要がある
        exclude=["retweets", "replies"],
    )
    tweet_text = re.sub(r'https?://\S+', '', response.data[0].text).replace('\n', ' ').replace('\r', '').strip()
    return tweet_text


def generate_image_with_emotion(tweet_text):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"Create a high-quality, polished 3D render of a stylized, 2-head-tall Pixar-style cartoon character based on the uploaded photo. The character should have big expressive eyes, rounded facial features, soft lighting, and a cute chibi-like proportion. Retain the person’s key traits such as hairstyle, skin tone, and clothing color (e.g., T-shirt and cap), but simplify them in an adorable Pixar/3D animation style. \
               Make the character appear as if speaking the phrase: {tweet_text} in a speech bubble. The speech bubble should use a Japanese font appropriate for the style (e.g., rounded, friendly typeface such as Noto Sans JP or similar). The background and the character’s facial expression should match the mood and context of the phrase."

    result = client.images.edit(
        model="gpt-image-1",
        image=[
            open("./icon/profile.png", "rb"),
        ],
        prompt=prompt,
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open("image.png", "wb") as f:
        f.write(image_bytes)


if __name__ == "__main__":
    generate_image_with_emotion(get_latest_tweet())
