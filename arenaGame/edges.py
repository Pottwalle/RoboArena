import pygame

TRANSITIONS = {
    "dirt": [("water", "water_dirt"), ("lava", "lava_dirt")],
    "jungle": [("dirt", "dirt_jungle")],
}

class Tile_Mask():
    def __init__(self, top, bottom, left, right, tile_type):
        '''stores the direction tile typed of the given tile
        Args:
            top, bottom, left, right, tile_type: tile types according to type_mapping in arena.py
        '''
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.tile_type = tile_type
        self.mask = self.generate_mask()
    
    def generate_mask(self) -> list:
        '''generates a list of tuples which hold the (edge_key, direction), the edge_key contains the <base tile type>_<neighbor tile type> and directions in the format n, e, s, w, nw, ne, sw, se'''
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
            add_edges(neighbor_type[0], neighbor_type[1])
        
        return overlays
