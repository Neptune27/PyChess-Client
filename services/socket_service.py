import threading
import time
import socket

from services.base_service import BaseService



class SocketService(BaseService):
    def __init__(self):
        BaseService.__init__(self)
        self._socket = None
        self.host = '26.247.59.68'
        self.port = 9999
        self.receive_handlers = []
        self.ready_msg = ""
        self.running = False

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
        self._socket.setblocking(False)

    def start(self):
        try:
            self.connect()
            self.running = True
            threading.Thread(target=self._fork_receive).start()
            threading.Thread(target=self._msg_on_ready).start()
        except ConnectionRefusedError:
            self.logger.info("Cannot connect to server")

    def disconnect(self):
        self.logger.info("Disconnecting from server %s:%d", self.host, self.port)
        self.running = False
        if self._socket is None:
            return
        self._socket.close()

    def _fork_receive(self):
        total_retry = 0
        while self.running:
            try:
                data = self._socket.recv(1024)
            except BlockingIOError:
                continue
            except OSError:
                total_retry += 1
                self.logger.error(f"Cannot connect to server, retrying... {total_retry}")
                if total_retry == 20:
                    self.disconnect()

                continue
            msgs = data.decode('utf-8')
            self.logger.info(f"Received: {msgs}")
            for msg in msgs.split("\\"):
                for receive_handler in self.receive_handlers:
                    receive_handler(msg)
        self.logger.info("Stopped")

    def send(self, message):
        try:
            self._socket.sendall(f"{message}\\".encode('utf-8'))
        except OSError:
            self.logger.info("Cannot send data to server, disconnecting...")
            self.disconnect()

    def on_receive(self, handler):
        self.receive_handlers.append(handler)

    def _msg_on_ready(self):
        retry = 0
        while self.running:
            try:
                self.send(self.ready_msg)
                return
            except BlockingIOError:
                retry += 1
                self.logger.info(f"Connecting, retry: {retry}")
                time.sleep(1)
            except OSError:
                retry += 1
                self.logger.info(f"Connecting, retry: {retry}")
                time.sleep(1)


def a(msg):
    print(msg)


if __name__ == '__main__':
    service = SocketService()
    service.on_receive(a)
    service.start()
    time.sleep(2)
    service.send("join 1")
    i = 0
    while True:
        time.sleep(0.5)
        service.send(f"i: {i}")
        i += 1
