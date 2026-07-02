import os
import pygame
from settings import settings

def spiele_hintergrundmusik():
    # PulseAudio-Treiber für Linux erzwingen
    os.environ["SDL_AUDIODRIVER"] = "pulse"

    try:
        pygame.mixer.init()

        pygame.mixer.music.load(settings.BASE_DIR / "../Arena_musik_epic.mp3")
        pygame.mixer.music.play(-1)  # -1 Endlosschleife im Hintergrund
        pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
        print("Hintergrundmusik läuft...")
    except pygame.error as e:
        print(f"Audio-Fehler: {e}. Spiel läuft stumm weiter.")