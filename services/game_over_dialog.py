import pygame_gui
import pygame

from services.base_service import BaseService
from services.setting import Setting


class GameOverDialog(BaseService):
    def __init__(self, setting: Setting):
        super().__init__()
        self.on_restart = None
        self.manager = pygame_gui.UIManager((setting.WIDTH, setting.HEIGHT), 'theme.json')

        rect = pygame.Rect((0, 0), (500, 200))
        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect, manager=self.manager,
                                                 anchors={
                                                     'center': 'center'
                                                 }
                                                 )

        restart_layout = pygame.Rect(0, -100, 100, 50)

        self.restart_btn = pygame_gui.elements.UIButton(relative_rect=restart_layout,
                                                        text='Restart',
                                                        manager=self.manager,
                                                        container=self.panel,
                                                        anchors={
                                                            'centerx': 'centerx',
                                                            'bottom': 'bottom'
                                                        }
                                                        )

        return_layout = pygame.Rect(-100, -100, 100, 50)

        self.return_btn = pygame_gui.elements.UIButton(relative_rect=return_layout,
                                                       text='Return',
                                                       manager=self.manager,
                                                       container=self.panel,
                                                       anchors={
                                                           'centerx': 'centerx',
                                                           'bottom': 'bottom'
                                                       }
                                                       )

        info_layout = pygame.Rect(0, 50, 100, 50)

        self.info_label = pygame_gui.elements.UILabel(relative_rect=info_layout,
                                                      text='Restart',
                                                      manager=self.manager,
                                                      container=self.panel,
                                                      anchors={
                                                          'centerx': 'centerx',
                                                      }
                                                      )

        # btn = pygame_gui.elements.UIButton(relative_rect=restart_layout,
        #                                    text='Restart',
        #                                    manager=self.manager,
        #                                    container=self.panel)
        # btn = pygame_gui.elements.UIButton(relative_rect=restart_layout,
        #                                    text='Restart',
        #                                    manager=self.manager,
        #                                    container=self.panel)

    def process_events(self, event):
        self.manager.process_events(event)
        if event.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if event.ui_element == self.restart_btn:
            self.logger.info("Restarting game")
            if self.on_restart is not None:
                self.on_restart()

    def on_restart_clicked(self, callback):
        self.on_restart = callback

    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self, surface):
        self.manager.draw_ui(surface)
