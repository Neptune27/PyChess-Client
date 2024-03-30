import logging.config
from dependency_injector import containers, providers

from components.main_menu import MainMenu
from components.room_menu import RoomMenu
from services.board import Board
from services.game import Game
from components.game_over_dialog import GameOverDialog
from services.setting import Setting
from services.socket_service import SocketService
from services.stockfish_service import StockfishService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini"
    )

    # Gateways
    setting = providers.Singleton(
        Setting,
        config_file=config.setting.location
    )

    # Singleton
    stockfish = providers.Singleton(
        StockfishService,
        setting=setting
    )

    socket_service = providers.Singleton(
        SocketService
    )

    # Services
    board = providers.Factory(Board, setting=setting, stockfish=stockfish, socket_service=socket_service)
    game_over_dialog = providers.Factory(GameOverDialog, setting=setting)
    main_menu = providers.Factory(MainMenu, setting=setting)
    room_menu = providers.Factory(RoomMenu, setting=setting, socket_service=socket_service)

    game = providers.Factory(Game, setting=setting, board=board, stockfish=stockfish, socket_service=socket_service,
                             main_menu=main_menu, game_over_dialog=game_over_dialog, room_menu=room_menu)
    




