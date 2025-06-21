import random
import pygame

from config import MUSIC, SFX

class Music:
    MUSIC_END_EVENT = pygame.USEREVENT + 1

    def __init__(self, music_on=True):
        pygame.mixer.music.set_volume(0.5)
        self.themes = MUSIC
        random.shuffle(self.themes)
        self.current_index = 0
        self.music_on = music_on
        if self.music_on:
            self.play()

        # Zarejestruj event po zakończeniu pliku
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def play(self, loops=-1):
        # odtwarza aktualny plik
        if not self.music_on or not self.themes:
            return
        pygame.mixer.music.load(MUSIC[self.current_index])
        pygame.mixer.music.play(loops)

    def stop(self):
        # zatrzymuje odtwarzanie muzyki
        pygame.mixer.music.stop()

    def next(self):
        # odtwarza kolejny plik
        if not self.themes:
            return
        self.current_index = (self.current_index + 1) % len(self.themes)
        self.play()

    def handle_event(self, event):
        # jeśli wystąpił nasz event - kolejny plik
        if event.type == self.MUSIC_END_EVENT:
            self.next()
        # klawisz M zmienia muzyke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next()

    def set_music_on(self, on: bool):
        # włącza lub wyłącza muzykę
        self.music_on = on
        if self.music_on:
            # jeśli nic nie gra, zacznij
            if not pygame.mixer.music.get_busy():
                self.play()
        else:
            self.stop()


class Sound:
    def __init__(self, sound_on=True):
        self.sounds = SFX
        self.sound_on = sound_on

    def play(self, name):
        # odtwarza dźwięk o nazwie podanej w argumencie, jeżeli dźwięki są włączone
        if self.sound_on and name in self.sounds:
            try:
                pygame.mixer.Sound(self.sounds[name]).play()
            except Exception as e:
                print("Błąd audio:", e)

    def set_sound_on(self, on: bool):
        # włącza lub wyłącza efekty dźwiękowe
        self.sound_on = on
        if not self.sound_on:
            pygame.mixer.stop()


