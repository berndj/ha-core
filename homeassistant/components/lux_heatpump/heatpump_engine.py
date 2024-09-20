"""Heatpump engine module."""

import socket
import time


class heatpump_engine:
    """Engine talking to the heatpump over ser2net."""

    def __init__(self, sock=None):
        """Init heatpump connection."""
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.heating_circuit_flow_temp = 0.0
        self.heating_circuit_return_flow_temp_actual = 0.0
        self.heating_circuit_return_flow_temp_setpoint = 0.0
        self.domestic_hot_water_temp_setpoint = 0.0
        self.domestic_hot_water_temp_actual = 0.0
        self.outdoor_temp = 0.0
        self.polls = 0
        self.polls_skipped = 0
        self.epoch_time = int(time.time())
        self.host = None
        self.port = None

    def is_socket_closed(self, sock: socket.socket) -> bool:
        """Check socket closed state."""
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        return False

    def check_socket(self):
        """Check and repair socket."""

        if self.is_socket_closed(self.sock):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

    def connect(self, host, port):
        """Connect to ser2net socket."""
        self.host = host
        self.port = port
        try:
            self.sock.connect((host, port))
        except ConnectionError:
            # print("Connection Failed")
            return

    def readlines(self):
        """Read answer from ser2net/heatpump."""
        self.sock.settimeout(0.1)
        while True:
            try:
                data = self.sock.recv(1024)
            except TimeoutError:
                break
            except ConnectionAbortedError:
                self.reinit()
                break
            lines = data.split(b"\r\n")
            for line in lines:
                self.extract_temp(line)

    def trigger_stats(self):
        """Trigger response from heatpump."""
        buf = "1800\n\r"
        try:
            self.sock.send(buf.encode(encoding="utf-8"))
        except ConnectionAbortedError:
            self.reinit()

    def extract_temp(self, line):
        """Extract temperature values from response."""

        ser_str = line.decode("utf-8")
        tokens = ser_str.split(";")
        try:
            cat1 = int(tokens[0])
            if len(tokens) > 1:
                cat2 = int(tokens[1])
        except ValueError:
            return

        if cat1 == 1100 and cat2 == 12:
            tokens.pop(0)
            tokens.pop(0)
            #            for token in tokens:
            #                print(token)
            try:
                self.heating_circuit_flow_temp = float(tokens[0]) / 10
                self.heating_circuit_return_flow_temp_actual = float(tokens[1]) / 10
                self.heating_circuit_return_flow_temp_setpoint = float(tokens[2]) / 10
                self.outdoor_temp = float(tokens[4]) / 10
                self.domestic_hot_water_temp_actual = float(tokens[5]) / 10
                self.domestic_hot_water_temp_setpoint = float(tokens[6]) / 10
            except ValueError:
                return

    def poll_for_stats(self):
        """Poll sensor data."""

        new_time = int(time.time())
        if new_time - self.epoch_time > 10 or self.polls == 0:
            self.check_socket()
            self.trigger_stats()
            self.readlines()
            self.epoch_time = new_time
            self.polls += 1
        else:
            self.polls_skipped += 1
