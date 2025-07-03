class Camera:
    def __init__(self, level_width, level_height, screen_width, screen_height):
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0

    def apply(self, rect):
        # przekształca rect z przestrzeni świata do przestrzeni ekranu
        return rect.move(-self.x, -self.y)

    def update(self, target_rect):
        # centrowanie wokół gracza
        raw_x = target_rect.centerx - self.screen_width // 2
        raw_y = target_rect.centery - self.screen_height // 2

        # oś X – standardowy clamp
        self.x = max(0, min(raw_x, self.level_width - self.screen_width))

        # oś Y – tylko scroll na długich mapach
        if self.level_height <= self.screen_height:
            self.y = 0
        else:
            min_y = -self.screen_height // 2
            max_y = self.level_height - self.screen_height
            self.y = max(min_y, min(raw_y, max_y))


    def apply_point(self, point):
        px, py = point
        return px - self.x, py - self.y
