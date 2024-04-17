import pygame_gui
import pygame

from components.base_ui import BaseUI
from services.setting import Setting


class BoardInfoMenu(BaseUI):
    def __init__(self, setting: Setting):
        super().__init__(setting)
        rect = pygame.Rect(-200, 0, 200, setting.HEIGHT)

        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect,
                                                 manager=self.manager,
                                                 anchors={
                                                     'right': 'right',
                                                     'top': 'top'
                                                 })

        self.pgn_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(-25, 0, 100, 25),
                                                     manager=self.manager,
                                                     container=self.panel,
                                                     text="PGN:"
                                                     )

        self.pgn_output = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(0, 0, 195, 500),
                                                        manager=self.manager,
                                                        container=self.panel,
                                                        html_text="",
                                                        anchors={
                                                            'top_target': self.pgn_label,
                                                            'centerx': "centerx"
                                                        }
                                                        )

        self.fen_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(-25, 0, 100, 25),
                                                     manager=self.manager,
                                                     container=self.panel,
                                                     text="FEN:",
                                                     anchors={
                                                         'top_target': self.pgn_output
                                                     })

        self.fen_output = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(0, 0, 195, 200),
                                                        manager=self.manager,
                                                        container=self.panel,
                                                        html_text="",
                                                        anchors={
                                                            'top_target': self.fen_label,
                                                            'centerx': "centerx"
                                                        })

    def set_fen_text(self, text):
        self.fen_output.set_text(text)

    def set_pgn_text(self, text):
        self.pgn_output.set_text(text)