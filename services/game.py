import threading

import pygame
import pygame_gui
from pygame import SurfaceType, Surface

from components.chat_component import ChatGUI
from services.base_service import BaseService
from services.board import Board
from services.game_over_dialog import GameOverDialog
from services.setting import Setting
from services.socket_service import SocketService
from services.stockfish_service import Stockfish


class Game(BaseService):
    screen: Surface | SurfaceType = None

    def __init__(self, setting: Setting,
                 board: Board, stockfish: Stockfish, socket_service: SocketService):
        BaseService.__init__(self)
        pygame.init()
        pygame.font.init()
        self.socket_service = socket_service
        self.stockfish = stockfish
        self.setting = setting
        self.board = board
        self.run = False

        Game.screen = pygame.display.set_mode([setting.WIDTH, setting.HEIGHT])

        self.board.screen = Game.screen

        self.logger.info('Game started')

        self.clock = pygame.time.Clock()

        self.game_scenes = []

        self.play_online = True
        self.board.play_online = self.play_online

        self.game_over_dialogs = GameOverDialog(setting)
        self.game_over_dialogs.on_restart_clicked(self.board.reset_board)

        self.chat_gui = ChatGUI(setting, socket_service)

        if self.play_online:
            self.socket_service.ready_msg = "join|1"
            self.socket_service.on_receive(self.board.handle_socket_message)
            self.board.start_online_game()

    def start(self):
        pygame.init()
        self.run = True
        while self.run:
            time_delta = self.clock.tick(self.setting.FPS) / 1000.0
            self.board.draw()

            # event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.logger.info('Game quit')
                    self.kill_socket()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.logger.info(event)
                    self.board.handle_event(event)

                self.chat_gui.process_events(event)

                if self.board.board_state > 1:
                    self.game_over_dialogs.process_events(event)

            if self.board.board_state > 1:
                self.game_over_dialogs.update(time_delta)
                self.game_over_dialogs.draw(self.screen)

            self.chat_gui.update(time_delta)
            self.chat_gui.draw(self.screen)

            pygame.display.flip()

    def kill_socket(self):
        self.socket_service.running = False
