class Camera:
    def __init__(self, level_width, level_height, screen_width, screen_height):
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0

    def apply(self, rect):
        """Przekształca rect z przestrzeni świata do przestrzeni ekranu"""
        return rect.move(-self.x, -self.y)

    def update(self, target_rect):
        # Środek ekranu na graczu
        self.x = target_rect.centerx - self.screen_width // 2
        self.y = target_rect.centery - self.screen_height // 2
        # Ograniczenia, by kamera nie wychodziła poza level
        self.x = max(0, min(self.x, self.level_width - self.screen_width))
        self.y = max(0, min(self.y, self.level_height - self.screen_height))
