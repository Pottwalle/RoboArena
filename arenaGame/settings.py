from pathlib import Path
import json
import pygame

class GameSettings:
    def __init__(self):   
        # Screen
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 60
        self.SHOW_FPS = True

        # ui
        self.UI_SCALE = int(self.SCREEN_WIDTH / 320)

        # Tiles
        self.TILE_SIZE = 32
        self.EDGE_OVERLAYS = True

        # Inventory
        self.ITEM_SIZE = 16

        # Music
        self.MUSIC_VOLUME = 1.0
        self.MUSIC = "on"

        # base rescource path
        self.BASE_DIR = Path(__file__).parent
        self.ASSET_DIR = self.BASE_DIR / "assets"
        self.CONFIG_FILE = self.BASE_DIR / "settings.json"
        self.load()
    
    def load(self):

        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.__dict__.update(data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Error loading settings, continung with defaults: {e}")
    
    def save(self):
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump({
                    "SCREEN_WIDTH": self.SCREEN_WIDTH,
                    "SCREEN_HEIGHT": self.SCREEN_HEIGHT,
                    "FPS": self.FPS,
                    "SHOW_FPS": self.SHOW_FPS,
                    "UI_SCALE": self.UI_SCALE,
                    "TILE_SIZE": self.TILE_SIZE,
                    "EDGE_OVERLAYS": self.EDGE_OVERLAYS,
                    "ITEM_SIZE": self.ITEM_SIZE,
                    "MUSIC_VOLUME": self.MUSIC_VOLUME,
                    "MUSIC": self.MUSIC
                }, f, indent=4)
        except Exception as e:
            print(f"Error at saving settings: {e}")
    
    def set_music_volume(self, volume: str):
        '''changes the ingame Music

        changes the global settings.MUSIC_VOLUME setting'''
        float_volume = max(0.0, min(1.0, float(volume) / 100))
        pygame.mixer.music.set_volume(float_volume)
        self.MUSIC_VOLUME = float_volume
        self.save()
    
    def set_music(self, value: str):
        '''pauses / unpauses the music
        
        changes the global acessibla settings.MUSIC setting
        
        Args:
            value: "on" or "off" un / pauses the music'''
        self.MUSIC = value
        if value == "on":
            pygame.mixer.music.unpause()
        elif value == "off":
            pygame.mixer.music.pause()
        self.save()
    
    def set_show_fps(self, value: str):
        self.SHOW_FPS = (value == "on")
        self.save()

# global settings instance
settings = GameSettings()