import pygame

class ScoreManager:
    def __init__(self, hud, points_per_kill=100):
        self.hud = hud
        self.points_per_kill = points_per_kill

    def handle_hits(self, projectiles: pygame.sprite.Group, enemies: pygame.sprite.Group):
        """
        Sprawdza kolizje pocisków z wrogami,
        usuwa trafione obiekty i przekazuje liczbę punktów HUD-owi.
        """
        hits = pygame.sprite.groupcollide(
            projectiles, enemies,
            True,   # usuwaj pocisk
            True    # usuwaj wroga
        )
        if not hits:
            return
        # policz ile wrogów zginęło
        killed = sum(len(v) for v in hits.values())
        # nalicz punkty
        self.hud.add_points(self.points_per_kill * killed)
