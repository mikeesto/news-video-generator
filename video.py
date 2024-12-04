from moviepy import *
import os


def create_video_with_images_and_audio(
    image_folder="images", audio_file="audio.mp3", output_file="output.mp4"
):
    # Get list of image files
    image_files = [
        f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))
    ]
    image_files.sort()  # Ensure consistent ordering

    # Create clips from images (5 seconds each)
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


create_video_with_images_and_audio(
    image_folder="images",
    audio_file="4December.mp3",
    output_file="video.mp4",
)
