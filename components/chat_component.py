from collections import deque

import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryBox, UITextBox, UIButton

from components.base_ui import BaseUI
from services.base_service import BaseService
from services.setting import Setting
from services.socket_service import SocketService


class ChatGUI(BaseUI):
    def __init__(self, setting: Setting, socket_service: SocketService):
        super().__init__(setting)
        self.__is_online = True
        self.setting = setting
        self.forfeit_offline_callback = None
        self.undo_callback = None

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
            relative_rect=pygame.Rect(0, -225, 200, 100),
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

        self.forfeit_button = UIButton(
            relative_rect=pygame.Rect(0, -125, 100, 50),
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
            relative_rect=pygame.Rect(100, -125, 100, 50),
            text="Tie",
            container=self.panel,
            manager=self.manager,
            tool_tip_text="",
            object_id='#tie_button',
            anchors={
                'bottom': 'bottom'
            }
        )

        self.undo = UIButton(
            relative_rect=pygame.Rect(0, -75, 200, 50),
            text="Undo",
            container=self.panel,
            manager=self.manager,
            tool_tip_text="",
            object_id='#undo_button',
            anchors={
                'bottom': 'bottom'
            }
        )

    @property
    def is_online(self):
        return self.__is_online

    @is_online.setter
    def is_online(self, value):
        if not isinstance(value, bool):
            return

        self.__is_online = value
        if value:
            self.text_output_box.enable()
            self.text_entry_box.enable()
            self.forfeit_button.enable()
            self.tie_button.enable()
            self.undo.enable()
            self.forfeit_button.set_text("Forfeit")

        else:
            self.tie_button.disable()
            self.text_output_box.disable()
            self.text_entry_box.disable()
            self.forfeit_button.set_text("Return")

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
            case "command":
                match tokens[1]:
                    case "undo":
                        if tokens[2] == "r":
                            self.text_output_box.append_html_text("--Opponent made a undo request, will you accept "
                                                                  "it?--\r\n")
                        elif tokens[2] == "a":
                            self.text_output_box.append_html_text("--Undo Made--\r\n")
                        elif tokens[2] == "d":
                            self.text_output_box.append_html_text("--Undo Denied--\r\n")
                    case "tie":
                        if tokens[2] == "r":
                            self.text_output_box.append_html_text("--Opponent made a Tie request, will you accept "
                                                                  "it?--\r\n")
                        elif tokens[2] == "a":
                            self.text_output_box.append_html_text("--Tie Made--\r\n")
                        elif tokens[2] == "d":
                            self.text_output_box.append_html_text("--Tie Denied--\r\n")

    def handle_chat(self, msg: str):
        self.text_output_box.append_html_text(f"Opponent: {msg}")

    def send_message(self, msg: str):
        self.socket_service.send(f"chat|{msg}")

    def send_command_message(self, msg: str):
        self.socket_service.send(f"command|{msg}")

    def send_command(self, message):
        match message:
            case "/forfeit":
                self.send_command_message("/forfeit")
            case "/undo":
                self.text_output_box.append_html_text("--Undo Request--\r\n")
                self.send_command_message("/undo")
            case "/tie":
                self.text_output_box.append_html_text("--Tie Request--\r\n")
                self.send_command_message("/tie")
            case _:
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
        if len(message) == 0:
            return
        if message == "\n":
            return
        if message[0] == '/':
            self.send_command(message)
        else:
            self.send_chat_message(message)

        self.text_entry_box.clear()

    def process_events(self, event: pygame.event.Event):
        super().process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.send_chat()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            match event.ui_element:
                case self.forfeit_button:
                    self.handle_forfeit()
                case self.undo:
                    self.handle_undo()
                case self.tie_button:
                    self.send_command("/tie")

    def handle_undo(self):
        if self.is_online:
            self.send_command("/undo")
        else:
            self.handle_callback(self.undo_callback)

    def handle_forfeit(self):
        if self.is_online:
            self.send_command("/forfeit")
        else:
            self.handle_callback(self.forfeit_offline_callback)

    def update(self, delta_time):
        super().update(delta_time)
        self.handle_queue()

