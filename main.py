import pygame
from dependency_injector.wiring import inject, Provide

from containers import Container
from services.game import Game
from services.setting import Setting


@inject
def main(game: Game = Provide[Container.game],
         ):
    pygame.init()
    pygame.font.init()

    game.start()
    pass


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
    pass
