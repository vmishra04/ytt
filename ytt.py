from __future__ import unicode_literals
import youtube_dl
import speech_recognition as sr
import csv
import os

class ytt():
    def __init__(self):
        self.ids = []
        self.read_csv('news_politics.csv')
        
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
        with open('txt/{}.txt'.format(vid), 'w') as txtfile:
            txtfile.write(r.recognize_sphinx(audio)) #recognize_google
            
    def start(self):
        i = 0
        for id in self.ids:
            i += 1
            if os.path.exists('txt/{}.txt'.format(id)):
                continue
            try:
                print('{}) {}\nDownloading Audio ...'.format(str(i), str(id)))
                self.get_audio(id)
                print('Download Completed.\nProcessing Audio File ...')
                self.get_text(id)
                print('Processing Completed')
                if os.path.exists('{}.flac'.format(id)):
                    os.remove('{}.flac'.format(id))
            except:
                print('Error!')

project = ytt()
project.start()
