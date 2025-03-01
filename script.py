import requests
from dotenv import load_dotenv
import os
import json
import fal_client
import pathlib

load_dotenv()

OPENROUTER_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
}


def delete_images():
    for file in os.listdir("images"):
        if file != ".gitkeep":
            os.remove(os.path.join("images", file))


def fetch_news_headlines():
    # Fetch top 3 news headlines
    NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?sources=abc-news-au&apiKey={os.getenv('NEWS_API_KEY')}&pageSize=3"

    response = requests.get(NEWS_API_URL)
    news_headlines = [article["title"] for article in response.json()["articles"]]
    print("Retrieved news headlines")
    return news_headlines


def generate_image_descriptions(news_headlines):
    descriptions = []

    for headline in news_headlines:
        data = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Generate a text to image prompt from the news headline. Here is an example: 'A quaint cobblestone street in a historic European town, with flowers blooming on balconies, captured in golden hour lighting'. Reply with the prompt only. Detail is essential. Include descriptions of color, mood, background, and subject matter. Do not include anything else in reply.",
                },
                {"role": "user", "content": f"HEADLINE: {headline}"},
            ],
            "temperature": 0.5,
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=OPENROUTER_HEADERS,
            data=json.dumps(data),
        )

        result = response.json()
        descriptions.append(result["choices"][0]["message"]["content"])

    print("Generated image descriptions")
    return descriptions


def generate_images(image_descriptions):
    for i, description in enumerate(image_descriptions):
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={"prompt": description, "image_size": "square_hd"},
        )

        image_url = result["images"][0]["url"]
        image_response = requests.get(image_url)

        filename = f"image_{i}.jpg"
        with open(os.path.join("images", filename), "wb") as file:
            file.write(image_response.content)

        print(f"Saved {filename}")


def generate_lyrics(news_headlines):
    data = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [
            {
                "role": "system",
                "content": """Generate lyrics for a pop song from the array of news headlines. The song should be informative, the listener should understand today's news headlines. There should be one verse, chorus and bridge only. Reply with the following structure only. Do not include anything else in reply.
                [Verse]
                Verse lyrics here
                [Chorus]
                Chorus lyrics here
                [Bridge]
                Bridge lyrics here
                """,
            },
            {"role": "user", "content": str(news_headlines)},
        ],
        "temperature": 0.5,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=OPENROUTER_HEADERS,
        data=json.dumps(data),
    )

    result = response.json()
    lyrics = result["choices"][0]["message"]["content"]

    # Remove leading whitespace from each line
    lyrics_cleaned = "\n".join(line.lstrip() for line in lyrics.splitlines())

    pathlib.Path("lyrics.txt").write_text(lyrics_cleaned)
    print("Generated lyrics")


# Workflow
delete_images()
news_headlines = fetch_news_headlines()
image_descriptions = generate_image_descriptions(news_headlines)
generate_images(image_descriptions)
generate_lyrics(news_headlines)
