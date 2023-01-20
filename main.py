import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from button import Button
from settingsQT import Setting_W
from PyQt5.QtWidgets import QApplication


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class Menu:
    def __init__(self):
        pg.init()
        self.SCREEN = pg.display.set_mode((1920, 1080))
        pg.display.set_caption("Menu")
        self.BG = pg.image.load("assets/Background.png")

    @staticmethod
    def get_font(size):
        return pg.font.Font("assets/font.ttf", size)

    def play(self):
        while True:
            game = Game()
            game.run()

    def options(self):
        app = QApplication(sys.argv)
        ex = Setting_W()
        ex.show()
        sys.exit(app.exec())

    def main_menu(self):
        while True:
            self.SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pg.mouse.get_pos()

            MENU_TEXT = self.get_font(200).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(990, 150))

            PLAY_BUTTON = Button(image=pg.image.load("assets/Play Rect.png"), pos=(990, 350),
                                 text_input="PLAY", font=self.get_font(150), base_color="#d7fcd4",
                                 hovering_color="White")
            OPTIONS_BUTTON = Button(image=pg.image.load("assets/Options Rect.png"), pos=(990, 550),
                                    text_input="OPTIONS", font=self.get_font(150), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pg.image.load("assets/Quit Rect.png"), pos=(990, 750),
                                 text_input="QUIT", font=self.get_font(150), base_color="#d7fcd4",
                                 hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pg.quit()
                        sys.exit()

            pg.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.main_menu()
