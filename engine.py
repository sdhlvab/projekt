import pygame

from audio import Sound

class Engine:
    def __init__(self, hud, points_per_kill=100):
        self.hud = hud
        self.points_per_kill = points_per_kill
        self.sfx = Sound()

    def handle_hits(self, projectiles: pygame.sprite.Group, enemies: pygame.sprite.Group):
        # wykryj trafienia pocisk→wróg i usuń obie grupy
        hits = pygame.sprite.groupcollide(
            projectiles, enemies,
            True,  # usuń pocisk
            False  # nie usuwaj wroga od razu – pozwól take_damage(…) zadziałać
        )
        for proj, hit_list in hits.items():
            for enemy in hit_list:
                # dajemy trochę damage
                enemy.take_damage(proj.damage)
                # jeśli wróg faktycznie umarł, nalicz punkty
                if not enemy.alive():
                    self.sfx.play("kill")
                    self.hud.add_points(self.points_per_kill)

    def handle_player_collisions(self, player, enemies: pygame.sprite.Group):
        if pygame.sprite.spritecollideany(player, enemies):
            player.take_damage(1)