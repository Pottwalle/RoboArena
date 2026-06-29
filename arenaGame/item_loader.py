from item import Item, Consumable
from settings import settings
import json
import pygame

def load_items():
    try:
        with open(settings.ASSET_DIR / "data/items.json", 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der Items: {e}")
        return {}
    
    item_spritesheet = pygame.image.load(settings.ASSET_DIR / "items/items.png")
    
    item_database = {}
    for key, info in data.items():
        try:
            coords = info["sprite"]
            icon = item_spritesheet.subsurface((coords["x"], coords["y"], settings.ITEM_SIZE, settings.ITEM_SIZE)).convert_alpha()

            if info["type"] == "consumable":
                item = Consumable(
                    info["name"],
                    icon,
                    info["description"],
                    info["stats"].get("heal_amount", 0)
                )
            else:
                item = Item(
                    info["name"],
                    icon,
                    info["description"]
                )
            item_database[key] = item
        except KeyError as e:
            print(f"Fehlender Key bei Item {key}: {e}")
        except pygame.error as e:
            print(f"Fehler beim Spriteladen für {key}: {e}")
    
    return item_database