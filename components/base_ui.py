import pygame
import pygame_gui

from services.base_service import BaseService
from services.setting import Setting


class BaseUI(BaseService):
    def __init__(self, setting: Setting):
        super().__init__()
        self.setting = setting
        self.manager = pygame_gui.UIManager((setting.WIDTH, setting.HEIGHT), 'theme.json')

    @staticmethod
    def handle_callback(callback, *args):
        if callback is None:
            return

        callback(*args)

    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self, surface):
        self.manager.draw_ui(surface)

    def process_events(self, event: pygame.event.Event):
        self.manager.process_events(event)

