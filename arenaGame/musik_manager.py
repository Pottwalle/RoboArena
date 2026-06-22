import os
import pygame

def spiele_hintergrundmusik():
    # PulseAudio-Treiber für Linux erzwingen
    os.environ["SDL_AUDIODRIVER"] = "pulse"

    try:
        pygame.mixer.init()

        pygame.mixer.music.load("../Arena_musik_epic.mp3")
        pygame.mixer.music.play(-1)  # -1 Endlosschleife im Hintergrund
        print("Hintergrundmusik läuft...")
    except pygame.error as e:
        print(f"Audio-Fehler: {e}. Spiel läuft stumm weiter.")