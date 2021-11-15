# Entity capsule


class EntityManager:
    def __init__(self, screen, *entities):
        self.screen = screen
        self.entities = list(entities)

    def update(self):
        for entity in self.entities:
            entity.update()

    def get_render_entities(self):
        return self.entities
