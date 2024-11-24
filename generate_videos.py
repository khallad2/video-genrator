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
    for file in os.listdir(visuals_folder):
        if file.endswith(".jpg") and len(images) < max_images:
            images.append(os.path.join(visuals_folder, file))
        elif file.endswith(".mp4") and len(videos) < max_videos:
            videos.append(os.path.join(visuals_folder, file))
    return images, videos

def create_video(images, videos, voiceover_path, output_filename, background_music_path=None):
    """
    Create a video using images, videos, and a voiceover.
    """
    clips = []

    # Add images as clips with effects
    for image_path in images:
        image_clip = ImageClip(image_path, duration=5)
        image_clip = Resize(height=1080).apply(image_clip)  # Resize to fit the video dimensions
        image_clip = FadeIn(1).apply(image_clip)
        image_clip = FadeOut(1).apply(image_clip)
        clips.append(image_clip)

    # Add video clips with transitions
    for video_path in videos:
        try:
            video_clip = VideoFileClip(video_path)
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

    # Add Arabic subtitles
    subtitles = [
        ("الحرب في أوكرانيا اليوم", 0, 5),
        ("الحرب في الشرق الأوسط اليوم", 5, 10),
    ]
    for text, start, end in subtitles:
        subtitle_clip = TextClip(font='Arial', text=text, font_size=24, duration=end-start, color='white', size=(1920, 100), margin=(None, None), bg_color=None, stroke_color=None, stroke_width=0, method='caption', text_align='left', horizontal_align='center', vertical_align='center', interline=4, transparent=True)
        final_clip = CompositeVideoClip([final_clip, subtitle_clip])

    # Add the voiceover
    if os.path.exists(voiceover_path):
        voiceover = AudioFileClip(voiceover_path)
        if final_clip.audio is not None:
            final_audio = CompositeAudioClip([final_clip.audio, voiceover])
        else:
            final_audio = voiceover
        final_clip = final_clip.with_audio(final_audio)

    # Add background music if provided
    if background_music_path and os.path.exists(background_music_path):
        background_music = AudioFileClip(background_music_path)  # Lower volume for background music
        background_music.max_volume('0.03')
        if final_clip.audio is not None:
            final_audio = CompositeAudioClip([final_clip.audio, background_music])
        else:
            final_audio = background_music
        final_clip = final_clip.with_audio(final_audio)

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

    logging.info("Loading visuals.")
    images, videos = load_visuals(visuals_folder)
    logging.info(f"Loaded {len(images)} images and {len(videos)} videos.")

    logging.info("Creating the video.")
    create_video(images, videos, voiceover_path, output_filename, background_music_path)
    logging.info("Video creation completed.")

# Run the script
if __name__ == "__main__":
    main()
