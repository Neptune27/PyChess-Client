import json
from collections import deque

import pygame
import pygame_gui.elements
from pygame.sprite import Group

from components.base_ui import BaseUI
from services.setting import Setting
from services.socket_service import SocketService


class RoomMenu(BaseUI):
    def __init__(self, setting: Setting, socket_service: SocketService):
        super().__init__(setting)
        self.to_main_menu_callback = None
        self.deque = deque()
        self.socket_service = socket_service
        rect = pygame.Rect(0, 0, setting.WIDTH, setting.HEIGHT)
        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect,
                                                 manager=self.manager,
                                                 anchors={
                                                     'left': 'left',
                                                     'top': 'top'
                                                 })
        self.refresh_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-225, 25, 200, 100),
                                                        text="Refresh",
                                                        manager=self.manager,
                                                        container=self.panel,
                                                        anchors={
                                                            'right': 'right'
                                                        })

        self.create_room = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(-450, 25, 200, 100),
                                                        text="Create Room",
                                                        manager=self.manager,
                                                        container=self.panel,
                                                        anchors={
                                                            'right': 'right'
                                                        })

        self.return_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(25, 25, 200, 100),
                                                       text="Return",
                                                       manager=self.manager,
                                                       container=self.panel,
                                                       anchors={
                                                           'left': 'left'
                                                       })

        self.room_scroll_view = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(0, 150, setting.WIDTH, setting.HEIGHT - 150),
            manager=self.manager,
            container=self.panel
        )
        self.room_group = []
        self.socket_service.on_receive(self.handle_receive)
        self.to_board_callback = None
        self.add_room([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        # self.clear_room()

    def handle_receive(self, msg: str):
        self.deque.append(msg)

    def handle_queue(self):
        if len(self.deque) == 0:
            return
        msg = self.deque.popleft()
        tokens = msg.split("|")
        if tokens[0] == "room_info":
            rooms = json.loads(tokens[1])
            self.clear_room()
            self.add_room(rooms)

    def clear_room(self):
        [r.kill() for r in self.room_group]
        self.room_group.clear()

    def get_rooms(self):
        self.socket_service.send("rooms")

    def add_room(self, rooms: list[list]):

        for i, room in enumerate(rooms):
            anchors = {
                'top_target': self.room_group[-1]
            } if len(self.room_group) > 0 else {
                'top': 'top'
            }
            offset = 25 if len(self.room_group) > 0 else 0
            rect = pygame.Rect(self.setting.WIDTH / 2 - 250, offset, 500, 100)
            ui_room = pygame_gui.elements.UIButton(relative_rect=rect,
                                                   manager=self.manager,
                                                   container=self.room_scroll_view,
                                                   text=f"Join room {i + 1}",
                                                   anchors=anchors
                                                   )

            self.room_group.append(ui_room)
        self.room_scroll_view.set_scrollable_area_dimensions((800, len(rooms) * 125))

    def process_events(self, event: pygame.event.Event):
        super().process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in self.room_group:
                pos = self.room_group.index(event.ui_element)
                self.logger.info(f"Click to room {pos + 1}")
                self.socket_service.send(f"join|{pos + 1}")
                self.handle_callback(self.to_board_callback)

                # Callback to join room
            if event.ui_element == self.refresh_btn:
                self.socket_service.send("rooms")
            if event.ui_element == self.return_btn:
                self.handle_callback(self.to_main_menu_callback)
            if event.ui_element == self.create_room:
                self.socket_service.send("join|999")
                self.handle_callback(self.to_board_callback)

    def update(self, delta_time):
        super().update(delta_time)
        self.handle_queue()
