import requests
import pytube
import sys
import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
from pytube import YouTube
from pydub import AudioSegment
import threading
import concurrent.futures
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value, Lock
import time



api_key = "AIzaSyBJAtfWhVU88jSXxXUw7zBKI0bTOVRjJ2U"
base_url = "https://www.googleapis.com/youtube/v3/search"

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
download_path = os.path.join(desktop, "102003366_Mashup")

if not os.path.exists(download_path):
    os.makedirs(download_path)

download_path_video = os.path.join(download_path,"Videos")
if not os.path.exists(download_path_video):
    os.makedirs(download_path_video)

download_path_audio = os.path.join(download_path, "Audio")
if not os.path.exists(download_path_audio):
    os.makedirs(download_path_audio)

download_path_audio_cut = os.path.join(download_path,"Audio Cut")
if not os.path.exists(download_path_audio_cut):
    os.makedirs(download_path_audio_cut)

singer_name = sys.argv[1]
no_songs = int(sys.argv[2])
dur = int(sys.argv[3])
output_file = sys.argv[4]

cut_audio_file_path = os.path.join(download_path, output_file)

def main():
    # Exception Handling
    if len(sys.argv) != 5:
        print("The number of arguments ar not equal to 4")
        exit(1)
    if not output_file.endswith(".mp3"):
        print("The output file is not in mp3 format")
        exit(1)
    if no_songs < 10:
        print("No. of songs are less than 10")
        exit(1)
    if dur < 20:
        print("The minimum duration of cut is 20")
        exit(1)


    params = {
        "part": "snippet",
        "q": singer_name,
        "type": "video",
        "maxResults": 50,  # maximum number of results per API request
        "key": api_key
    }

    # make the API request
    response = requests.get(base_url, params=params)
    data = response.json()
    video_urls = []

    try:
        data['items']
    except KeyError:
        print("Some error in API Key exists. That may occur unusally sometimes")
    
    if data["items"]:
        for item in data["items"]:
            url = "https://www.youtube.com/watch?v="
            id = item['id']['videoId']
            video_urls.append(url + str(id))
    else:
        print("No videos found for the specified query.")
        exit(1)

    count = Value('i',0)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for video_url in video_urls:
            futures = executor.submit(extract_videos(video_url,count))
            if count.value == no_songs:
                break

    extract_audio()
    cut_and_merge()

    print("Conversion ho gya Desktop pr bnegi file 102003366_Mashup ke naam se")

# This function extracts the top n videos of singer x from youtube
# if the video is a livestream it skips it and shows the error message  
def extract_videos(video_url,count):

        try:
            yt = pytube.YouTube(video_url)
            video_stream = yt.streams.filter(progressive=True,file_extension="mp4").first()  
        except pytube.exceptions.LiveStreamError:
            print(f"Skipping video {count.value+1} as it is a live stream: {video_url}")
            # print("Error:", e)
            return
        except pytube.exceptions.RecordingUnavailable:
            print(f"Skipping video {count.value+1} as it is a live stream: {video_url}")
            return

        try:
            video_stream = yt.streams.filter(progressive=True,file_extension="mp4").first()
        except KeyError:
            return


        # taking max length of song to be 10mins and min to be 1 min
        if int(yt.length) >= 600 or int(yt.length) <= 60:
            return

        with Lock():
            if count.value >= no_songs:
                print("All Required Videos are downloaded, so Stops Downloading Process!")
                return
            count.value = count.value+1
        
        video_title = yt.title
        video_title = video_title.replace("|", "").replace("/", "").replace("\"","")
        video_stream.download(download_path_video, video_title+".mp4")
        print(f"Downloaded video {count.value} of {no_songs}: {video_title}")
        
        return

def extract_audio():

    folder_path = download_path_video
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            video_file = os.path.join(folder_path, filename)
            video = VideoFileClip(video_file)
            audio = video.audio
            audio_file = os.path.join(download_path_audio, os.path.splitext(filename)[0] + ".mp3")
            audio.write_audiofile(audio_file, codec="mp3")

def cut_and_merge():        
    folder_path = download_path_audio

    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            audio_file = os.path.join(folder_path,filename)
            audio = AudioFileClip(audio_file)
            audio_file_path = os.path.join(download_path_audio_cut, os.path.splitext(filename)[0] + ".mp3")
            audio_cut = audio.subclip(0,dur)
            audio_cut.write_audiofile(audio_file_path)

    audio_lst = []
    for filename in os.listdir(download_path_audio_cut):
        audio_file = os.path.join(download_path_audio_cut,filename)
        audio = AudioFileClip(audio_file)
        audio_lst.append(audio)

    final_audio = concatenate_audioclips([x for x in audio_lst])
    final_audio.write_audiofile(cut_audio_file_path)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time : ",time.time() - start_time)