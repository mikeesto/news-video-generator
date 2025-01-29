from moviepy import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os
import re


def parse_lyrics_file(lyrics_file):
    """Parse the lyrics file and return a list of subtitle tuples (start_time, end_time, text)"""
    subtitles = []

    with open(lyrics_file, "r") as f:
        for line in f:
            # Skip empty lines
            if not line.strip():
                continue

            # Find all timestamp-text pairs in the line
            matches = re.findall(r"\[(\d{2}:\d{2}:\d{2})\](.*?)(?=\[|$)", line)

            for i in range(len(matches)):
                time_str, text = matches[i]

                # Convert timestamp to seconds
                h, m, s = map(int, time_str.split(":"))
                start_time = h * 3600 + m * 60 + s

                # If there's a next subtitle, use its timestamp as end time
                if i + 1 < len(matches):
                    next_time_str = matches[i + 1][0]
                    h, m, s = map(int, next_time_str.split(":"))
                    end_time = h * 3600 + m * 60 + s
                else:
                    # For the last subtitle in a line, show it for 4 seconds
                    end_time = start_time + 4

                subtitles.append((start_time, end_time, text.strip()))

    return subtitles


def create_subtitle_clips(subtitles, video_size):
    def make_textclip(text):
        return TextClip(
            text=text,
            font="Arial",
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=3,
            size=video_size,
            method="caption",
            vertical_align="bottom",
            margin=(0, -30, 0, 0),
        )

    # Format subtitles into the required structure
    subtitles_formatted = []
    for start_time, end_time, text in subtitles:
        subtitles_formatted.append(((start_time, end_time), text))

    return SubtitlesClip(subtitles_formatted, make_textclip=make_textclip)


def create_video_with_images_and_audio(
    image_folder="images",
    audio_file="audio.mp3",
    output_file="output.mp4",
    lyrics_file="lyrics.txt",
):
    # Get list of image files
    image_files = [
        f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))
    ]
    image_files.sort()  # Ensure consistent ordering

    # Create clips from images (10 seconds each)
    image_clips = []
    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        clip = ImageClip(img_path).with_duration(10)
        # Center the image vertically if needed
        clip = clip.with_position("center")
        image_clips.append(clip)

    # Concatenate all image clips
    video_clip = concatenate_videoclips(image_clips, method="compose")

    # Load and set the audio
    audio_clip = AudioFileClip(audio_file)

    # If the video is shorter than the audio, loop the video
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    if video_duration < audio_duration:
        # Calculate how many times we need to loop (round up)
        loops_needed = int(audio_duration / video_duration) + 1
        # Create a list of repeated clips
        repeated_clips = [video_clip] * loops_needed
        # Concatenate all repeated clips
        video_clip = concatenate_videoclips(repeated_clips, method="compose")
        # Trim to exact audio duration
        video_clip = video_clip.subclipped(0, audio_duration)

    # Parse and create subtitle clips
    if lyrics_file and os.path.exists(lyrics_file):
        subtitles = parse_lyrics_file(lyrics_file)
        subtitle_clips = create_subtitle_clips(subtitles, video_clip.size)

        # Combine video with subtitles
        video_clip = CompositeVideoClip([video_clip, subtitle_clips])

    # Combine video with audio
    final_clip = video_clip.with_audio(audio_clip)

    # Write the result
    final_clip.write_videofile(
        output_file,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="4000k",
    )

    # Clean up
    final_clip.close()
    audio_clip.close()


# Create the video with subtitles
create_video_with_images_and_audio(
    image_folder="images",
    audio_file="4December.mp3",
    output_file="video.mp4",
    lyrics_file="lyrics.txt",
)
