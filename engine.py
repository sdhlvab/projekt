import pygame

from ui import Scoreboard, HealthBar, GameOverScreen

class Engine:
    def __init__(self, hud, points_per_kill=100):
        self.hud = hud
        self.points_per_kill = points_per_kill

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
                    self.hud.add_points(self.points_per_kill)

    def handle_player_collisions(self, player, enemies: pygame.sprite.Group):
        if pygame.sprite.spritecollideany(player, enemies):
            player.take_damage(1)

class GameEngine:
    def __init__(self, screen, game_logic):
        self.screen = screen
        self.game = game_logic  # instancja Twojej klasy Game (bez pętli!)
        self.clock = pygame.time.Clock()
        self.hud = Scoreboard()
        self.healthbar = HealthBar(self.game.player)
        self.score_mgr = Engine(self.hud)
        self.gameover = GameOverScreen(screen)
        self.state = "PLAY"

    def run(self):
        while self.state != "EXIT":
            dt = self.clock.tick(60) / 1000
            self._handle_events()
            if self.state == "PLAY":
                self._update(dt)
            self._draw()

        pygame.quit()

    def _handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.state = "EXIT"
            else:
                proj = self.game.player.handle_event(e)
                if proj:
                    self.game.projectiles.add(proj)

    def _update(self, dt):
        # logika ruchu
        self.game.player.update(dt, self.game.ground_rects)
        self.game.enemies.update(self.game.ground_rects)
        self.game.projectiles.update(self.game.enemies, self.game.ground_rects)

        # punkty i obrażenia
        self.score_mgr.handle_hits(self.game.projectiles, self.game.enemies)
        self.score_mgr.handle_player_collisions(self.game.player, self.game.enemies)

        # sprawdź koniec gry
        if self.game.player.hp <= 0:
            self.state = "GAMEOVER"

    def _draw(self):
        # świat
        self.game.draw_world()  # rysuje level, gracza, wrogów, pociski
        # HUD
        self.hud.draw(self.screen)
        self.healthbar.draw(self.screen)

        if self.state == "GAMEOVER":
            self.gameover.show()
            self.state = "EXIT"
        else:
            pygame.display.flip()