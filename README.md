# News video generator

This is an experiment in creating a music video for daily news headlines. The idea is to generate images and lyrics for today's top three news headlines, and then use a song generation model to create a song. The song is used as the background music for the video, and the images are used as the visuals.

## Example

<video controls src="https://github.com/mikeesto/news-video-generator/raw/refs/heads/master/example/example.mp4" title="Example video"></video>

## How to use

1. Run `script.py` to retrieve news headlines, generate images and lyrics.

2. Generate and download song manually by pasting lyrics into [Suno](https://suno.com/). Choose `pop` as the genre.

3. Run `timestamps.py` to generate timestamps for the video.

4. Run `video.py` to generate the video.

## Environment variables

- `NEWS_API_KEY`: API key for news API
- `OPENROUTER_API_KEY`: API key for open router
- `FAL_KEY`: API key for fal.ai
- `GEMINI_API_KEY`: API key for gemini

## Process

1. Retrieve news headlines from news API.

2. For each news headline, generate a prompt using an LLM for an associated image.

3. Generate images using FLUX.1 [schnell].

   - A video generation model could also be used here, for now flux is faster and cheaper.

4. Generate lyrics for headlines using an LLM.

5. Generate song using Suno.

   - Suno and Loudme seem to be the current best options for generating songs from lyrics.
   - Neither have an API, so the lyrics need to be pasted manually.
   - In the future, using an API here would be ideal.

6. Generate timestamps.

   - I have found Gemini models to be quite good at generating timestamps from audio. I tried Whisper too but Gemini seems to be better at identifying words commonly used in news headlines (e.g. brand names, locations, etc.)

7. Generate video - combine images, lyrics and timestamps.

## Inspiration

[Karpathy's tweet](https://x.com/karpathy/status/1819229916212474070)
