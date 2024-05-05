from enum import Enum

import pygame
from pygame import SurfaceType, Surface

from components.board_info_menu import BoardInfoMenu
from components.chat_component import ChatGUI
from components.main_menu import MainMenu
from components.room_menu import RoomMenu
from services.base_service import BaseService
from services.board import Board
from components.game_over_dialog import GameOverDialog
from services.setting import Setting
from services.socket_service import SocketService
from services.stockfish_service import Stockfish


class EScene(Enum):
    MAIN_MENU = 0
    ONLINE_SELECTION = 1
    BOARD = 2


class Game(BaseService):
    screen: Surface | SurfaceType = None

    def __init__(self, setting: Setting,
                 board: Board, stockfish: Stockfish, socket_service: SocketService,
                 game_over_dialog: GameOverDialog, main_menu: MainMenu, room_menu: RoomMenu, board_info: BoardInfoMenu):
        BaseService.__init__(self)
        self.board_info = board_info
        self.room_menu = room_menu
        self.main_menu = main_menu

        self.game_over_dialog = game_over_dialog
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

        self.game_scenes = EScene.MAIN_MENU

        self.play_online = True
        self.board.play_online = self.play_online

        self.game_over_dialog.on_restart_clicked(self.board.reset_board)

        self.chat_gui = ChatGUI(setting, socket_service)

        self.setup_callback()

    def setup_callback(self):
        self.main_menu.vs_ai_callback = self.handle_callback_ai
        self.main_menu.vs_2p_callback = self.handle_callback_offline
        self.main_menu.vs_online_callback = self.handle_callback_online

        self.chat_gui.forfeit_offline_callback = self.handle_forfeit_offline
        self.chat_gui.undo_callback = self.handle_undo_offline

        self.room_menu.to_board_callback = self.to_board
        self.room_menu.to_main_menu_callback = self.to_main_menu

        self.game_over_dialog.return_callback = self.to_main_menu
        self.socket_service.on_receive(self.board.handle_socket_message)

        self.board.set_fen_callback = self.board_info.set_fen_text
        self.board.set_pgn_callback = self.board_info.set_pgn_text

    def to_board(self):
        self.game_scenes = EScene.BOARD

    def to_main_menu(self):
        self.game_scenes = EScene.MAIN_MENU
        self.socket_service.disconnect()

    def to_online(self):
        self.game_scenes = EScene.ONLINE_SELECTION
        self.socket_service.ready_msg = "rooms"
        self.socket_service.start()

    def handle_forfeit_offline(self):
        self.game_scenes = EScene.MAIN_MENU

    def handle_undo_offline(self):
        self.board.undo_turn_offline()

    def handle_callback_offline(self):
        self.logger.info('Clicked Offline')
        self.board.is_online = False
        self.board.is_ai = False
        self.board.reset_board()
        self.game_scenes = EScene.BOARD
        self.chat_gui.is_online = False

    def handle_callback_ai(self):
        self.logger.info('Clicked AI')
        self.board.is_online = False
        self.board.is_ai = True
        self.board.reset_board()
        self.game_scenes = EScene.BOARD
        self.chat_gui.is_online = False

    def handle_callback_online(self):
        self.socket_service.start()
        self.socket_service.send("rooms")

        self.logger.info('Clicked Online')
        self.game_scenes = EScene.ONLINE_SELECTION

        self.board.is_online = True
        self.board.is_ai = False
        self.board.reset_board()
        self.chat_gui.is_online = True
        self.board.start_online_game()
        self.play_online = True

    def start(self):
        pygame.init()
        self.run = True
        while self.run:
            time_delta = self.clock.tick(self.setting.FPS) / 1000.0

            # event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.logger.info('Game quit')
                    self.socket_service.disconnect()
                    exit()

                match self.game_scenes:
                    case EScene.BOARD:
                        self.handle_board_event(event)
                    case EScene.MAIN_MENU:
                        self.main_menu.process_events(event)
                    case EScene.ONLINE_SELECTION:
                        self.room_menu.process_events(event)

            match self.game_scenes:
                case EScene.BOARD:
                    self.handle_board(time_delta)
                case EScene.MAIN_MENU:
                    self.main_menu.update(time_delta)
                    self.main_menu.draw(self.screen)
                case EScene.ONLINE_SELECTION:
                    self.room_menu.update(time_delta)
                    self.room_menu.draw(self.screen)

            pygame.display.flip()

    def handle_board_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.board.handle_event(event)

        self.chat_gui.process_events(event)
        self.board_info.process_events(event)

        if self.board.board_state > 1:
            self.game_over_dialog.process_events(event)

    def handle_board(self, time_delta):
        self.board.draw()
        if self.board.board_state > 1:
            match self.board.board_state:
                case 2:
                    self.game_over_dialog.info_label.set_text("White win")
                case 3:
                    self.game_over_dialog.info_label.set_text("Black win")
                case 4:
                    self.game_over_dialog.info_label.set_text("Draw - Player Offered")
                case 5:
                    self.game_over_dialog.info_label.set_text("Draw - Stale Mate")
                case 6:
                    self.game_over_dialog.info_label.set_text("Draw - 50 Moves")
                case 7:
                    self.game_over_dialog.info_label.set_text("Draw - Three-fold Repetition")
                case 8:
                    self.game_over_dialog.info_label.set_text("Draw - Insufficient Pieces")

            self.game_over_dialog.update(time_delta)
            self.game_over_dialog.draw(self.screen)

        self.chat_gui.update(time_delta)
        self.chat_gui.draw(self.screen)

        self.board_info.update(time_delta)
        self.board_info.draw(self.screen)

