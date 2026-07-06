class UIManager:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)
    
    def handle_event(self, event):
        for element in self.elements:
            element.handle_event(event)
    
    def update(self, dt):
        for element in self.elements:
            element.update(dt)
    
    def draw(self, surface):
        for element in self.elements:
            element.draw(surface)