import os
import moviepy as mp
from datetime import date
import logging
import random
from moviepy import concatenate_videoclips, CompositeVideoClip, AudioFileClip, CompositeAudioClip, ImageClip, VideoFileClip
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from moviepy.video.fx.Resize import Resize
from moviepy.video.fx.CrossFadeIn import CrossFadeIn
from moviepy.video.fx.CrossFadeOut import CrossFadeOut
from moviepy.video.VideoClip import TextClip

# Set up logging to a file
logging.basicConfig(filename='video_creation.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_visuals(visuals_folder, max_images=20, max_videos=10):
    """
    Load images and videos from the visuals folder.
    """
    images = []
    videos = []
    used_files = set()
    for file in os.listdir(visuals_folder):
        if file.endswith(".jpg") and len(images) < max_images and file not in used_files:
            try:
                images.append(os.path.join(visuals_folder, file))
                used_files.add(file)
            except Exception as e:
                logging.error(f"Error loading image {file}: {e}")
        elif file.endswith(".mp4") and len(videos) < max_videos and file not in used_files:
            try:
                videos.append(os.path.join(visuals_folder, file))
                used_files.add(file)
            except Exception as e:
                logging.error(f"Error loading video {file}: {e}")
    return images, videos

def load_subtitles(subtitles_file):
    """
    Load subtitles from the Arabic script file.
    """
    subtitles = []
    try:
        with open(subtitles_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            start_time = 0
            duration = 10  # Each subtitle lasts 10 seconds
            for line in lines:
                text = line.strip()
                if text:
                    subtitles.append((text, start_time, start_time + duration))
                    start_time += duration
    except FileNotFoundError:
        logging.error(f"Subtitles file '{subtitles_file}' not found.")
    except Exception as e:
        logging.error(f"Error reading subtitles file: {e}")
    return subtitles

def create_video(images, videos, voiceover_path, output_filename, background_music_path=None, subtitles_file=None):
    """
    Create a video using images, videos, and a voiceover.
    """
    clips = []

    # Add images as clips with effects, ensuring each scene is at least 10 seconds
    for image_path in images:
        try:
            image_clip = ImageClip(image_path, duration=10)
            image_clip = Resize(height=1080).apply(image_clip)  # Resize to fit the video dimensions
            image_clip = FadeIn(1).apply(image_clip)
            image_clip = FadeOut(1).apply(image_clip)
            clips.append(image_clip)
        except Exception as e:
            logging.error(f"Error processing image {image_path}: {e}")

    # Add video clips with transitions, ensuring each scene is at least 10 seconds
    for video_path in videos:
        try:
            video_clip = VideoFileClip(video_path,  duration=5)
            video_clip = video_clip.subclip(0, min(10, video_clip.duration))  # Trim videos to 10 seconds max
            video_clip = CrossFadeIn(1).apply(video_clip)
            video_clip = CrossFadeOut(1).apply(video_clip)
            clips.append(video_clip)
        except Exception as e:
            logging.error(f"Error loading video {video_path}: {e}")
            continue

    # Concatenate all visual clips
    if clips:
        try:
            final_clip = concatenate_videoclips([clip for clip in clips if hasattr(clip, 'duration') and clip.duration > 0], method="compose")
        except Exception as e:
            logging.error(f"Error concatenating clips: {e}")
            return
    else:
        logging.error("No valid clips were loaded, video creation aborted.")
        return

    # # Load and add Arabic subtitles
    # if subtitles_file:
    #     subtitles = load_subtitles(subtitles_file)
    #     for text, start, end in subtitles:
    #         try:
    #             subtitle_clip = TextClip(font='Arial', text=text, font_size=24, duration=end-start, color='white', size=(1920, 100), margin=(None, None), bg_color=None, stroke_color=None, stroke_width=0, method='caption', text_align='left', horizontal_align='center', vertical_align='center', interline=4, transparent=True)
    #             # subtitle_clip = subtitle_clip.duration(end - start).start(start)
    #             final_clip = CompositeVideoClip([final_clip, subtitle_clip])
    #         except Exception as e:
    #             logging.error(f"Error creating subtitle clip: {e}")

    # Add the voiceover before background music
    if os.path.exists(voiceover_path):
        try:
            voiceover = AudioFileClip(
                voiceover_path)  # .set_start(final_clip.audio.duration if final_clip.audio else 0)
            # final_clip = final_clip.set_duration(voiceover.duration)  # Adjust the video duration to match the voiceover
            final_audio = CompositeAudioClip([final_clip.audio, voiceover]) if final_clip.audio else voiceover
            final_clip = final_clip.with_audio(final_audio)  # .set_audio(final_audio)
        except Exception as e:
            logging.error(f"Error loading voiceover {voiceover_path}: {e}")

        # Add background music if provided, and ensure it plays before the voiceover
    if background_music_path and os.path.exists(background_music_path):
        try:
            background_music = AudioFileClip(
                background_music_path)  # .fx(mp.audio.fx.all.volumex, 0.03)  # Lower volume for background music
            # background_music = background_music.set_duration(final_clip.duration)
            final_audio = CompositeAudioClip([background_music])
            final_clip = final_clip.with_audio(final_audio)
        except Exception as e:
            logging.error(f"Error loading background music {background_music_path}: {e}")

    # Write the output video file
    try:
        final_clip.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    except Exception as e:
        logging.error(f"Error writing video file {output_filename}: {e}")

# Main script
def main():
    visuals_folder = "visuals"
    voiceover_path = f"war_news_voiceover_{date.today().strftime('%Y-%m-%d')}.mp3"
    output_filename = f"war_news_video_{date.today().strftime('%Y-%m-%d')}.mp4"
    background_music_path = "background_music.mp3"  # Path to your background music
    subtitles_file = f"war_news_script_arabic_{date.today().strftime('%Y-%m-%d')}.txt"

    logging.info("Loading visuals.")
    images, videos = load_visuals(visuals_folder)
    logging.info(f"Loaded {len(images)} images and {len(videos)} videos.")

    logging.info("Creating the video.")
    create_video(images, videos, voiceover_path, output_filename, background_music_path, subtitles_file)
    logging.info("Video creation completed.")

# Run the script
if __name__ == "__main__":
    main()
