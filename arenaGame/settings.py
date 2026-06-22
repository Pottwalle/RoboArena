from pathlib import Path

class GameSettings:
    # Screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    
    # ui
    UI_SCALE = int(SCREEN_WIDTH / 320)
    
    # Tiles
    TILE_SIZE = 32
    EDGE_OVERLAYS = True
    
    # base rescource path
    BASE_DIR = Path(__file__).parent
    ASSET_DIR = BASE_DIR / "assets"

# global settings instance
settings = GameSettings()