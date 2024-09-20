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

    def connect(self, host, port):
        """Connect to ser2net socket."""
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
                #                print("======\nEOF\n=")
                break
            lines = data.split(b"\r\n")
            for line in lines:
                self.extract_temp(line)

    def trigger_stats(self):
        """Trigger response from heatpump."""
        buf = "1800\n\r"
        self.sock.send(buf.encode(encoding="utf-8"))

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
