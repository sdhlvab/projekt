import pygame

from audio import Sound

class Engine:
    def __init__(self, hud, points_per_kill=100):
        self.hud = hud
        self.points_per_kill = points_per_kill
        self.sfx = Sound()

    def handle_hits(self, projectiles: pygame.sprite.Group, enemies: pygame.sprite.Group):
        # wykrycie trafienia pocisk-wróg i usunięcie obu grup
        hits = pygame.sprite.groupcollide(projectiles, enemies,True,False)
        for proj, hit_list in hits.items():
            for enemy in hit_list:
                # zadanie obrażeń przeciwnikowi
                enemy.take_damage(proj.damage)
                # jeśli wróg faktycznie umarł to nalicz punkty i odtywórz dźwięk
                if enemy.hp <= 0:
                    self.hud.add_points(self.points_per_kill)
                    self.sfx.play("kill")

    def handle_player_collisions(self, player, enemies: pygame.sprite.Group):
        # wykrycie kolizji gracz - przeciwnicy i zredukowanie ilości hp jeśli tak się stało
        if pygame.sprite.spritecollideany(player, enemies):
            player.take_damage(1)