import logging.config
from dependency_injector import containers, providers

from services.board import Board
from services.game import Game
from services.setting import Setting
from services.socket_service import SocketService
from services.stockfish_service import Stockfish, StockfishService


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

    # Singletion
    stockfish = providers.Singleton(
        StockfishService,
        setting=setting
    )

    socket_service = providers.Singleton(
        SocketService
    )

    # Services
    board = providers.Factory(Board, setting=setting, stockfish=stockfish, socket_service=socket_service)

    game = providers.Factory(Game, setting=setting, board=board, stockfish=stockfish, socket_service=socket_service)
    




