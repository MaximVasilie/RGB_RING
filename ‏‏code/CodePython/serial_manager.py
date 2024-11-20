import time
import serial
import threading

PORT = 'COM5'
BAUDRATE = 9600
ERR_CONNECT = "Connection error, retry..."
OK_CONNECT = "Connections are successful"
TIME_RETRY = 5
COMMAND_SENT = "Command been sent: %s"
MSG_FROM_ARDUINO = "Messages from Arduino: %s"
SERIAL_TIMEOUT = 1
SERIAL_WAITING = 0
CONNECT_DELAY = 2
CONNECTED_STATE = True

class SerialManager:
    def __init__(self, port=PORT, baudrate=BAUDRATE):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False

    def connect(self):
        """
        this function establishes a connection to the serial device. Retries every TIME_RETRY seconds
        if the connection fails, until successful.
        :param: None
        :return: None
        :rtype: None
        Time: O(n), where n is the number of retry attempts until connection is established.
        """
        while not self.connected:
            #Loop will run until it connects
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=SERIAL_TIMEOUT) #trying to connect
                time.sleep(CONNECT_DELAY)   #wait after connecting
                self.connected = CONNECTED_STATE #int he connection
                print(OK_CONNECT)
            except serial.SerialException:
                #If not connect
                print(ERR_CONNECT)
                time.sleep(TIME_RETRY)

    def send_command(self, command):
        """
        Sends a command to the connected serial device.
        :param command: The command string to be sent to the device.
        :type command: str
        :return: None
        :rtype: None
        Time: O(k), where k is the length of the command string.
        """
        if self.ser:
            self.ser.write(command.encode())
            print(COMMAND_SENT % command)

    def read_from_serial(self):
        """
        Reads incoming messages from the connected serial device and prints them.
        Runs continuously as long as the connection is active.
        :param: None
        :return: None
        :rtype: None
        Time: O(n), where n is the number of messages read during the connection's lifetime.
        """
        while self.connected:
            if self.ser and self.ser.in_waiting > SERIAL_WAITING:
                message = self.ser.readline().decode('utf-8').strip()
                print(MSG_FROM_ARDUINO % message)
