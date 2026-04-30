import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        self.tracks  = []
        self.current = 0
        self.playing = False

        if os.path.exists(music_folder):
            for f in sorted(os.listdir(music_folder)):
                if f.endswith(('.mp3', '.wav')):
                    self.tracks.append(os.path.join(music_folder, f))

    def play(self):
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        if not self.tracks:
            return
        self.current = (self.current + 1) % len(self.tracks)
        self.play()

    def prev_track(self):
        if not self.tracks:
            return
        self.current = (self.current - 1) % len(self.tracks)
        self.play()

    def get_track_name(self):
        if not self.tracks:
            return "Нет треков"
        return os.path.basename(self.tracks[self.current])

    def get_status(self):
        return "▶ Playing" if self.playing else "■ Stopped"

    def get_track_number(self):
        if not self.tracks:
            return "0 / 0"
        return f"{self.current + 1} / {len(self.tracks)}"