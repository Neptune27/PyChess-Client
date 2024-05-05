import pygame
import pygame_gui
from pygame_gui import UIManager

pygame.init()

pygame.display.set_caption('Pygame Chat')
window_surface = pygame.display.set_mode((850, 700))
manager = UIManager((850, 700), '../theme.json')

background = pygame.Surface((850, 700))
background.fill(manager.ui_theme.get_colour('dark_bg'))

panel_background = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(50, 50, 750, 500),
    manager=manager,
    object_id="#scroll_panel_background"
)

scrollable_panel = pygame_gui.elements.UIScrollingContainer(
    relative_rect=pygame.Rect(25, 25, 740, 490),
    manager=manager,
    container=panel_background,
)

scrollable_panel.set_scrollable_area_dimensions((2000, 2000))
panel_list = []
for i in range(50):
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, i * 50), (700, 50)),
        manager=manager,
        container=scrollable_panel,

    )
    panel_list.append(panel)

clock = pygame.time.Clock()
is_running = True


while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            exit()

        manager.process_events(event)


    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()