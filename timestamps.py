import google.generativeai as genai
import pathlib
import dotenv
import os

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SONG = "15February.mp3"

model = genai.GenerativeModel("models/gemini-2.0-pro-exp-02-05")

prompt = "Generate transcript of lyrics with timestamps formatted as [mm:ss]. Do not include any other information in the response."

response = model.generate_content(
    [
        prompt,
        {"mime_type": "audio/mp3", "data": pathlib.Path(SONG).read_bytes()},
    ]
)

pathlib.Path("timestamps.txt").write_text(response.text)
