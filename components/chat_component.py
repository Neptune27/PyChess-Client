from collections import deque

import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryBox, UITextBox, UIButton

from services.base_service import BaseService
from services.setting import Setting
from services.socket_service import SocketService


class ChatGUI(BaseService):
    def __init__(self, setting: Setting, socket_service: SocketService):
        super().__init__()
        self.setting = setting
        self.manager = pygame_gui.UIManager((setting.WIDTH, setting.HEIGHT), 'theme.json')

        self.socket_service = socket_service
        self.socket_service.on_receive(self.handle_receive)
        self.deque = deque()

        rect = pygame.Rect((0, 0), (200, 800))
        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect, manager=self.manager,
                                                 anchors={
                                                     'left': 'left',
                                                     'top': 'top'
                                                 }
                                                 )

        self.text_entry_box = UITextEntryBox(
            relative_rect=pygame.Rect(0, -200, 200, 100),
            initial_text="",
            manager=self.manager,
            container=self.panel,
            anchors={
                'bottom': 'bottom'
            }
        )

        self.text_output_box = UITextBox(
            # relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
            relative_rect=pygame.Rect(0, 0, 200, 550),
            html_text="",
            container=self.panel,
            manager=self.manager
        )
        self.text_output_box.line_spacing = 0.1

        self.forfeit_button = UIButton(
            relative_rect=pygame.Rect(0, -100, 100, 70),
            text="Forfeit",
            container=self.panel,
            manager=self.manager,
            tool_tip_text="",
            object_id='#forfeit_button',
            anchors={
                'bottom': 'bottom'
            }

        )

        self.tie_button = UIButton(
            relative_rect=pygame.Rect(100, -100, 100, 70),
            text="Tie",
            container=self.panel,
            manager=self.manager,
            tool_tip_text="",
            object_id='#tie_button',
            anchors={
                'bottom': 'bottom'
            }
        )

    def handle_receive(self, msg: str):
        self.deque.append(msg)

    def handle_queue(self):
        if len(self.deque) == 0:
            return

        msg: str = self.deque.popleft()
        tokens = msg.split("|")
        match tokens[0]:
            case "chat":
                self.handle_chat(" ".join(tokens[1:]))

    def handle_chat(self, msg: str):
        self.text_output_box.append_html_text(f"Opponent: {msg}")

    def send_message(self, msg: str):
        self.socket_service.send(f"chat|{msg}")

    def send_command(self, message):
        if message == "/forfeit":
            self.text_output_box.append_html_text("--Forfeit Request--")
            self.send_message("/forfeit")

        else:
            self.text_output_box.append_html_text('<font color="blue">Command not found.</font>' + '<br><br>')

    def send_chat_message(self, message):
        self.text_output_box.append_html_text(f"You: {message}")
        # data = str(net.id) + ":" + self.text_entry_box.get_text()
        # reply = parse_data(net.send(data))
        self.send_message(message)
        # pygame.event.post(
        #     pygame.event.Event(pygame.KEYDOWN, unicode="U+232B", key=pygame.K_BACKSPACE, mod=pygame.KMOD_NONE))

    def send_chat(self):
        message = self.text_entry_box.get_text()
        if message == "\n":
            return
        if message[0] == '/':
            self.send_command(message)
        else:
            self.send_chat_message(message)

        self.text_entry_box.clear()

    def process_events(self, event: pygame.event.Event):
        self.manager.process_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.send_chat()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.forfeit_button:
                self.send_command("/forfeit")

    def update(self, delta_time):
        self.manager.update(delta_time)
        self.handle_queue()

    def draw(self, surface):
        self.manager.draw_ui(surface)
