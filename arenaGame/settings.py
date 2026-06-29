from pathlib import Path
import json

class GameSettings:
    def __init__(self):   
        # Screen
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 60

        # ui
        self.UI_SCALE = int(self.SCREEN_WIDTH / 320)

        # Tiles
        self.TILE_SIZE = 32
        self.EDGE_OVERLAYS = True

        # Inventory
        self.ITEM_SIZE = 16

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
                    "UI_SCALE": self.UI_SCALE,
                    "TILE_SIZE": self.TILE_SIZE,
                    "EDGE_OVERLAYS": self.EDGE_OVERLAYS,
                    "ITEM_SIZE": self.ITEM_SIZE
                }, f, indent=4)
        except Exception as e:
            print(f"Error at saving settings: {e}")

# global settings instance
settings = GameSettings()