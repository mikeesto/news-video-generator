import requests
from dotenv import load_dotenv
import os
import json
import fal_client
import base64

load_dotenv()

# Delete all images in the images folder

# for file in os.listdir("images"):
#     if file != ".gitkeep":
#         os.remove(os.path.join("images", file))


# Fetch top 5 news headlines

NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?sources=abc-news-au&apiKey={os.getenv('NEWS_API_KEY')}&pageSize=5"

response = requests.get(NEWS_API_URL)
news_headlines = [article["title"] for article in response.json()["articles"]]

# For each headline, generate a description of an image

headers_openrouter = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
}

descriptions = []

for headline in news_headlines:
    data = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "Generate an image description from the news headline. Here is an example: 'A quaint cobblestone street in a historic European town, with flowers blooming on balconies, captured in golden hour lighting'. Reply with the prompt only. Do not include anything else in reply.",
            },
            {"role": "user", "content": f"HEADLINE: {headline}"},
        ],
        "temperature": 0.5,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers_openrouter,
        data=json.dumps(data),
    )

    result = response.json()
    descriptions.append(result["choices"][0]["message"]["content"])

# print(descriptions)

# For each description, generate an image using fal.ai. Save it to the images folder and map it to the headline

for i, description in enumerate(descriptions):
    result = fal_client.subscribe(
        "fal-ai/fast-turbo-diffusion",
        arguments={"prompt": description, "image_size": "square_hd"},
    )

    image_data = result["images"][0]["url"].split(",")[1]

    image_binary = base64.b64decode(image_data)

    filename = f"image_{i}.jpg"
    with open(os.path.join("images", filename), "wb") as file:
        file.write(image_binary)

    print(f"Saved {filename}")


# Generate lyrics for headlines

data = {
    "model": "meta-llama/llama-3-8b-instruct:free",
    "messages": [
        {
            "role": "system",
            "content": """Generate lyrics for a pop song from the array of news headlines. There should be one verse, chorus and bridge only. Reply with the following structure only. Do not include anything else in reply.:
            [Verse]
            Evan’s free, the swap is done
            Headlines flash, a victory won
            While on Wall Street fortunes fall
            Tech giants stumble, hear the call
            [Chorus]
            It’s a day of highs and lows
            Freedom rings as markets slow
            From Moscow to the trading floor
            The world spins on forevermore
            [Bridge]
            Fed debates September’s fate
            Harris’ past fuels the debate
            Middle East in turmoil still
            Leaders fall, but hope fulfills
            """,
        },
        {"role": "user", "content": str(news_headlines)},
    ],
    "temperature": 0.5,
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers_openrouter,
    data=json.dumps(data),
)

result = response.json()

lyrics = result["choices"][0]["message"]["content"]

print(lyrics)


# Simple website where I upload the video and it stores it in cloudflare
