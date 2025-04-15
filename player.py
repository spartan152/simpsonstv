import os
import time
from subprocess import PIPE, Popen, STDOUT

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
log_file = '/home/pi/video_log.txt'  # Change this to your preferred log file path

videos = []

def log_video(video_name, reason):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # Get timestamp
    with open(log_file, 'a') as log:  # Append to log file
        log.write("[{}] {} - {}\n".format(timestamp, video_name, reason))

def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))

def playVideos():
    global videos
    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return
    videos.sort()
    for video in videos:
        start_time = time.time()  # Record start time
        try:
            playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
            playProcess.wait()
            end_time = time.time()  # Record end time
            play_duration = end_time - start_time  # Calculate duration
            if play_duration < 30:  # If video played for less than 30 seconds
                log_video(video, 'played for less than 30 seconds')
        except Exception as e:
            log_video(video, 'failed to play: {}'.format(str(e)))  # Log any error during play

while True:
    playVideos()
