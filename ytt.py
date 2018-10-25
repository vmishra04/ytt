from __future__ import unicode_literals
import youtube_dl
import speech_recognition as sr
import csv
import os
from datetime import datetime


class ytt():
    def __init__(self):
        self.ids = []
        self.read_csv('news_politics.csv')
        if not os.path.exists('txts'):
            os.makedirs('txts')
        
    def read_csv(self, csvpath):
        with open(csvpath, 'r', newline='') as csvfile:
            csvreader = csv.DictReader(csvfile, dialect='excel')
            for row in csvreader:
                self.ids.append(row['id'])

    def get_audio(self, vid):
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '32',
            }],
            'outtmpl': '%(id)s.%(etx)s',
            'quiet': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v={}'.format(vid)])

    def get_text(self, vid):
        r = sr.Recognizer()
        audiofile = sr.AudioFile(vid + '.flac')
        with audiofile as source:
            audio = r.record(source)
        with open('txts/{}.txt'.format(vid), 'w') as txtfile:
            txtfile.write(r.recognize_sphinx(audio)) #recognize_google
            
    def start(self):
        i = 0
        for id in self.ids:
            i += 1
            if os.path.exists('txts/{}.txt'.format(id)):
                continue
            try:
                print('{}) {}\n{} - Downloading Audio ...'.format(str(i), str(id), datetime.now().strftime('%H:%M:%S')))
                self.get_audio(id)
                print('{} - Download Completed.\n{} - Processing Audio File ...'.format(datetime.now().strftime('%H:%M:%S'), datetime.now().strftime('%H:%M:%S')))
                self.get_text(id)
                print('{} - Processing Completed'.format(datetime.now().strftime('%H:%M:%S')))
                if os.path.exists('{}.flac'.format(id)):
                    os.remove('{}.flac'.format(id))
            except:
                print('Error!')

project = ytt()
project.start()
