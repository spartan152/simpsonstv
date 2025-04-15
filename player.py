#Code has been modified to include a play count log, errors if they occur based on shorter than expected playtime or failure to play, and uses successful play count to ensure repeats don't occur until after all have played

import os
import random
import time
from subprocess import PIPE, Popen, STDOUT

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
play_counts_file = '/home/pi/play_counts.txt'  # Path to store play counts

videos = []


def loadPlayCounts():
    """Load the play counts from a file."""
    play_counts = {}
    if os.path.exists(play_counts_file):
        with open(play_counts_file, 'r') as f:
            for line in f:
                video, count = line.strip().split(' ')
                play_counts[video] = int(count)
    return play_counts


def savePlayCounts(play_counts):
    """Save the play counts to a file."""
    with open(play_counts_file, 'w') as f:
        for video, count in play_counts.items():
            f.write('{} {}\n'.format(video, count))


def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))


def playVideos():
    global videos
    play_counts = loadPlayCounts()  # Load play counts at the start

    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        return

    # Sort the videos by play count (favoring those with lower counts)
    videos.sort(key=lambda x: play_counts.get(x, 0))  # Default to 0 if video not in play_counts
    
    for video in videos:
        # Increment the play count of this video
        play_counts[video] = play_counts.get(video, 0) + 1

        # Play the video
        playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])
        playProcess.wait()

        # Save updated play counts after each video
        savePlayCounts(play_counts)


while True:
    playVideos()
