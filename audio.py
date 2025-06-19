import random
import pygame

from config import MUSIC, SFX

class Music:
    """
    Odpowiada za odtwarzanie tła muzycznego (theme1.mp3, theme2.mp3, ...).
    Automatycznie przechodzi do kolejnego pliku, gdy bieżący się zakończy.
    """
    MUSIC_END_EVENT = pygame.USEREVENT + 1

    def __init__(self, music_on=True):
        """
        music_on: czy muzyka ma być włączona
        """
        self.themes = MUSIC
        random.shuffle(self.themes)
        self.current_index = 0
        self.music_on = music_on

        # Zarejestruj event po zakończeniu pliku
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def play(self):
        """Rozpoczyna odtwarzanie aktualnego pliku muzycznego."""
        if not self.music_on or not self.themes:
            return
        pygame.mixer.music.load(MUSIC[self.current_index])
        pygame.mixer.music.play()

    def stop(self):
        """Zatrzymuje odtwarzanie muzyki."""
        pygame.mixer.music.stop()

    def next(self):
        """Przechodzi do kolejnego pliku i zaczyna je odtwarzać."""
        if not self.themes:
            return
        self.current_index = (self.current_index + 1) % len(self.themes)
        self.play()

    def handle_event(self, event):
        """
        Należy wywołać w pętli obsługi eventów.
        Jeśli event.type == MUSIC_END_EVENT, zaczyna kolejny utwór.
        """
        if event.type == self.MUSIC_END_EVENT:
            self.next()
        # klawisz M zmienia muzyke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.next()

    def set_music_on(self, on: bool):
        """Włącza lub wyłącza muzykę."""
        self.music_on = on
        if self.music_on:
            # jeśli nic nie gra, zacznij
            if not pygame.mixer.music.get_busy():
                self.play()
        else:
            self.stop()


class Sound:
    """
    Odpowiedzialna za efekty dźwiękowe.
    Przechowuje słownik {klucz: pygame.mixer.Sound}.
    """
    def __init__(self, sound_on=True):
        """
        sound_files: dict mapping klucz→ścieżka do pliku dźwiękowego
        sound_on: czy efekty dźwiękowe są włączone
        """
        self.sounds = SFX
        self.sound_on = sound_on

    def play(self, name):
        """Odtwarza dźwięk o podanym kluczu (jeśli jest włączony)."""
        if self.sound_on and name in self.sounds:
            try:
                pygame.mixer.Sound(self.sounds[name]).play()
            except Exception as e:
                print("Błąd audio:", e)

    def set_sound_on(self, on: bool):
        """Włącza lub wyłącza efekty dźwiękowe."""
        self.sound_on = on


