import google.generativeai as genai
import pathlib
import dotenv
import os

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "models/gemini-exp-1206"
)  # Use gemini-1.5-pro when it's working again

prompt = "Generate transcript of lyrics with timestamps formatted as [mm:ss]"

response = model.generate_content(
    [
        prompt,
        {"mime_type": "audio/mp3", "data": pathlib.Path("4December.mp3").read_bytes()},
    ]
)

pathlib.Path("lyrics.txt").write_text(response.text)
