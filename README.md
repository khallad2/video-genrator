# Video Generation Project

This project generates videos using images, video clips, and audio files, including voiceovers and background music. The final video incorporates effects like fades, subtitles, and transitions. Below you'll find a comprehensive guide on how to set up, run, and understand the functionalities of the project.

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Dependencies](#dependencies)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Logging](#logging)
8. [Troubleshooting](#troubleshooting)

## Overview

This project is designed to generate a video using different types of visual assets (images and videos), combined with audio assets (voiceovers and background music). The output video is created by adding effects like fading in/out, transitions, resizing, and subtitles.

Key features include:
- Load images and videos from a given folder.
- Add voiceover and background music to the final video.
- Apply transitions, fading, and resizing effects to video clips and images.
- Generate Arabic subtitles.
- Save the final video with a given filename.

## Project Structure

- **generate_videos.py**: Main script that loads visuals, processes them, and generates the video with audio and subtitles.
- **visuals/**: Directory where images and video files are stored.
- **war_news_voiceover_DATE.mp3**: Voiceover audio file expected to be available for each video creation with the specific date format.
- **background_music.mp3**: Background music file used in the video generation.
- **video_creation.log**: Log file for recording errors, status updates, and progress information.

## Dependencies

This project uses the following Python libraries:

- **moviepy**: For handling video and audio editing.
- **Pillow**: Used internally by MoviePy for text rendering.
- **logging**: To record the execution flow and error messages.

## Setup Instructions

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not available, manually install dependencies using:
   ```bash
   pip install moviepy Pillow
   ```

3. Ensure that the following files are available in the project directory:
   - A **visuals/** directory containing image (`.jpg`) and video (`.mp4`) files.
   - A **voiceover** audio file named with the format: `war_news_voiceover_YYYY-MM-DD.mp3`.
   - A **background_music.mp3** file for optional background music.

## Usage

1. Run the main video generation script:
   ```bash
   python generate_videos.py
   ```
   This will create a video with the filename `war_news_video_YYYY-MM-DD.mp4` where `YYYY-MM-DD` is the current date.

2. The final video will be saved in the current working directory.

## Configuration

The script uses a few configurable parameters that you can adjust as per your requirements:

- **Maximum Images/Videos**: Set the number of images and videos to use in the video generation.
  ```python
  load_visuals(visuals_folder, max_images=20, max_videos=10)
  ```
- **Output Video Resolution**: The images are resized to fit a resolution of height `1080px`. You can modify the `Resize` effect to match your desired resolution:
  ```python
  image_clip = Resize(height=1080).apply(image_clip)
  ```
- **Subtitle Configuration**: The subtitles are configured with the following details:
  - Font: Arial
  - Font size: 24
  - Color: White
  - Alignment: Center

  You can change these parameters in the `TextClip` instantiation:
  ```python
  subtitle_clip = TextClip(font='Arial', font_size=24, ...)
  ```

## Logging

The script uses the **logging** module to log messages to a file named `video_creation.log`. The log records important steps, errors, and exceptions that occur during the execution of the script.

Log messages include:
- The number of images and videos loaded.
- Any issues loading video files (e.g., corrupted files).
- Any errors during the concatenation or writing process.

## Troubleshooting

1. **Corrupted Video Files**:
   - If any of the video files are corrupted, they will be skipped, and an error message will be logged. Check the log file (`video_creation.log`) for details on which files caused the problem.

2. **Audio Issues**:
   - If there are issues with audio files, ensure that the voiceover and background music files exist in the correct paths and are in the proper format (`.mp3`).

3. **Font Issues for Subtitles**:
   - If the specified font is not found, you may encounter an error related to `PIL.ImageFont`. Ensure that the specified font (`Arial`) is available on your system. You can replace `'Arial'` with any other available font.

4. **Dependency Problems**:
   - If you encounter issues with installing MoviePy or Pillow, make sure to use compatible versions of Python (preferably 3.7 or above).

## Notes

- Make sure that `ffmpeg` is installed and available in your system path as **MoviePy** uses `ffmpeg` for video processing.
- It is recommended to keep the visuals folder organized with a manageable number of files to avoid long processing times.

## Future Enhancements

- Add command-line arguments to specify inputs like `visuals_folder`, `voiceover_path`, and `output_filename`.
- Introduce dynamic subtitle support to allow more flexibility in subtitle text and timing.
- Add error recovery for missing files to ensure smoother video generation without interruptions.

If you have any questions or need further assistance, feel free to open an issue in the repository.
