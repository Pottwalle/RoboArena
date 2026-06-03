import pygame

TRANSITIONS = {
    "dirt": ["water", "lava"],
    "jungle": ["dirt"]
}

class Tile_Mask():
    def __init__(self, top, bottom, left, right, tile_type):
        '''
        stores the 
        Args:
            top, bottom, left, right, tile_type: tile types according to type_mapping in arena.py
        '''
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.tile_type = tile_type
    
    def generate_mask(self):
        overlays = []

        def add_edges(neighbor_type, overlay_key):
            edges = set()
            if self.top == neighbor_type: edges.add("n")
            if self.right == neighbor_type: edges.add("e")
            if self.bottom == neighbor_type: edges.add("s")
            if self.left == neighbor_type: edges.add("w")

            for direction in edges:
                overlays.append((overlay_key, direction))

            if "n" in edges and "w" in edges: overlays.append((overlay_key, "nw"))
            if "n" in edges and "e" in edges: overlays.append((overlay_key, "ne"))
            if "s" in edges and "w" in edges: overlays.append((overlay_key, "sw"))
            if "s" in edges and "e" in edges: overlays.append((overlay_key, "se"))
        
        for neighbor_type in TRANSITIONS.get(self.tile_type, []):
            add_edges(neighbor_type, neighbor_type)
        
        return overlays
