import pygame

class NickInputUI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.nick = ""
        self.active = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        prompt = self.font.render("Podaj nick (Enter = zatwierdź):", True, (0,255,0))
        nicktxt = self.font.render(self.nick + "|", True, (0,255,0))
        self.screen.blit(prompt, (100, 200))
        self.screen.blit(nicktxt, (100, 250))
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.nick = self.nick[:-1]
            elif len(self.nick) < 12 and event.unicode.isprintable():
                self.nick += event.unicode
