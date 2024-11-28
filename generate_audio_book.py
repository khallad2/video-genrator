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
    Load subtitles from the English script file.
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

def create_video(image_path, voiceover_path, output_filename, background_music_path=None, subtitles_file=None):
    """
    Create a video using a single image and a voiceover.
    """
    try:
        # Load the image
        image_clip = ImageClip(image_path, duration=1000)
        image_clip = Resize(height=1080).apply(image_clip)  # Resize to fit the video dimensions
        image_clip = FadeIn(1).apply(image_clip)
        image_clip = FadeOut(1).apply(image_clip)
        final_clip = image_clip
    except Exception as e:
        logging.error(f"Error processing image {image_path}: {e}")
        return

    # Load and add Arabic subtitles
    if subtitles_file:
        subtitles = load_subtitles(subtitles_file)
        for text, start, end in subtitles:
            try:
                subtitle_clip = TextClip(font='Arial', text=text, font_size=24, duration=end-start, start= start, color='white', size=(1920, 100), margin=(None, None), bg_color=None, stroke_color=None, stroke_width=0, method='caption', text_align='left', horizontal_align='center', vertical_align='center', interline=4, transparent=True)
                # subtitle_clip = subtitle_clip.start(start)
                final_clip = CompositeVideoClip([final_clip, subtitle_clip])
            except Exception as e:
                logging.error(f"Error creating subtitle clip: {e}")

    # Add background music if provided, and ensure it plays before the voiceover
    if background_music_path and os.path.exists(background_music_path):
        try:
            background_music = AudioFileClip(background_music_path, duration=final_clip.duration).max_volume(0.03)  # Lower volume for background music
            # background_music = background_music.duration(final_clip.duration)
            final_audio = CompositeAudioClip([background_music])
            final_clip = final_clip.with_audio(final_audio)
        except Exception as e:
            logging.error(f"Error loading background music {background_music_path}: {e}")

    # Add the voiceover and adjust the length of the video to match the voiceover
    if os.path.exists(voiceover_path):
        try:
            voiceover = AudioFileClip(voiceover_path)
            final_clip = CompositeVideoClip([final_clip])  # Use the CompositeVideoClip to adjust duration if needed
            final_clip.duration = voiceover.duration  # Adjust video duration to match voiceover duration
            final_audio = CompositeAudioClip([voiceover])
            final_clip = final_clip.with_audio(final_audio)
        except Exception as e:
            logging.error(f"Error loading voiceover {voiceover_path}: {e}")

    # Write the output video file
    try:
        final_clip.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    except Exception as e:
        logging.error(f"Error writing video file {output_filename}: {e}")

# Main script
def main():
    visuals_folder = "visuals"
    english_voiceover_path = f"book_summary_english_voiceover_{date.today().strftime('%Y-%m-%d')}.mp3"
    arabic_voiceover_path = f"book_summary_arabic_voiceover_{date.today().strftime('%Y-%m-%d')}.mp3"
    german_voiceover_path = f"book_summary_german_voiceover_{date.today().strftime('%Y-%m-%d')}.mp3"
    arabic_output_filename = f"arabic_book_summary_video_{date.today().strftime('%Y-%m-%d')}.mp4"
    german_output_filename = f"german_book_summary_video_{date.today().strftime('%Y-%m-%d')}.mp4"
    background_music_path = "background_music.mp3"  # Path to your background music
    subtitles_file = f"book_summary_script_{date.today().strftime('%Y-%m-%d')}.txt"

    logging.info("Loading visuals.")
    images, videos = load_visuals(visuals_folder)
    logging.info(f"Loaded {len(images)} images.")

    if not images:
        logging.error("No images found, video creation aborted.")
        return

    # logging.info("Creating the video.")
    # create_video(images[0], voiceover_path, output_filename, background_music_path, subtitles_file)
    # logging.info("Video creation completed.")

    # logging.info("Creating English video.")
    # create_video(images, english_voiceover_path, output_filename, background_music_path, subtitles_file)
    # logging.info("Arabic Video creation completed.")

    logging.info("Creating the German video.")
    create_video(images[0], german_voiceover_path, german_output_filename, background_music_path, subtitles_file)
    logging.info("German Video creation completed.")

    logging.info("Creating the Arabic video.")
    create_video(images[0], arabic_voiceover_path, arabic_output_filename, background_music_path, subtitles_file)
    logging.info("Arabic Video creation completed.")

# Run the script
if __name__ == "__main__":
    main()
