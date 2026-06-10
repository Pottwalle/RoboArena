from pathlib import Path

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# ui
UI_SCALE = int(1280 / 320)

# Tiles
TILE_SIZE = 32
EDGE_OVERLAYS = True

# base rescource path
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"