from pytube import Playlist
from tqdm import tqdm
import os
import requests

# Function to download video with progress bar
def download_video_with_progress(stream, output_path, filename):
    response = requests.get(stream.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024

    tqdm_bar = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=filename, leave=True)
    with open(os.path.join(output_path, filename), 'wb') as file:
        for data in response.iter_content(chunk_size=chunk_size):
            tqdm_bar.update(len(data))
            file.write(data)
    tqdm_bar.close()

# Get playlist URL from user
playlist_url = input('Enter Playlist URL: ')

# Create a Playlist object
playlist = Playlist(playlist_url)

# Download videos with options
total_videos = len(playlist.videos)
downloaded = 0
for video in playlist.videos:
    print(f"Downloading: {video.title}")
    downloaded += 1

    # Get the highest resolution stream
    stream = video.streams.get_highest_resolution()

    # Sanitize filename
    sanitized_title = "".join([c for c in video.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    filename = f"{sanitized_title}.mp4"

    # Download the video with progress bar
    download_video_with_progress(stream, '.', filename)

    print(f"Downloaded {downloaded} out of {total_videos} videos.")

    # Ask user to continue
    choice = input("Do you want to exit after this video? (y/n): ")
    if choice.lower() == 'y':
        break

print("Download complete!" if downloaded == total_videos else f"Stopped downloading after {downloaded} videos.")
