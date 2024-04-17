import pygame
import pygame_gui

from components.base_ui import BaseUI
from services.base_service import BaseService
from services.setting import Setting


class MainMenu(BaseUI):
    def __init__(self, setting: Setting):
        super().__init__(setting)
        self.setting = setting
        self.manager = pygame_gui.UIManager((setting.WIDTH, setting.HEIGHT), 'theme.json')

        rect = pygame.Rect(0, 0, setting.WIDTH, setting.HEIGHT)
        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect, manager=self.manager,
                                                 anchors={
                                                     'left': 'left',
                                                     'top': 'top'
                                                 }
                                                 )

        self.vs_ai_callback = None
        self.vs_ai_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 100, 400, 100),
                                                         manager=self.manager,
                                                         container=self.panel,
                                                         text='Play VS AI',
                                                         anchors={
                                                             'centerx': 'centerx'
                                                         }
                                                         )

        self.vs_2p_callback = None
        self.vs_2p_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 250, 400, 100),
                                                         manager=self.manager,
                                                         container=self.panel,
                                                         text='2 Player Offline',
                                                         anchors={
                                                             'centerx': 'centerx'
                                                         }
                                                         )

        self.vs_online_callback = None
        self.vs_online_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 400, 400, 100),
                                                             manager=self.manager,
                                                             container=self.panel,
                                                             text='Online',
                                                             anchors={
                                                                 'centerx': 'centerx'
                                                             }
                                                             )

        self.puzzle_callback = None
        self.puzzle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 550, 400, 100),
                                                             manager=self.manager,
                                                             container=self.panel,
                                                             text='Random Puzzle',
                                                             anchors={
                                                                 'centerx': 'centerx'
                                                             }
                                                             )



    def process_events(self, event: pygame.event.Event):
        super().process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            match event.ui_element:
                case self.vs_ai_button:
                    self.handle_callback(self.vs_ai_callback)
                case self.vs_2p_button:
                    self.handle_callback(self.vs_2p_callback)
                case self.vs_online_button:
                    self.handle_callback(self.vs_online_callback)
                case self.puzzle_button:
                    self.handle_callback(self.puzzle_callback)
