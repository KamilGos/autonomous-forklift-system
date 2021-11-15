import serial
import sys

class Communication:
    """Handling communication between PC and robot via bluetooth
    """
    def __init__(self):
        self.port = None
        self.baudrate = None
        self.Serial = None
        self.initializated = False

    def Initialize(self, PORT, BAUDRATE):
        """ Initialize serial communication between PC and robot
        """
        self.Serial = None
        self.port = PORT
        self.baudrate = BAUDRATE
        try:
            self.Serial = serial.Serial(self.port, self.baudrate)
        except:
            print("Can't open serial port: ", self.port)
            if type(self.Serial) is type(None):
                self.initializated = False
                return 0

        if (self.Serial.isOpen() == False):
            self.Serial.open()
            print("Serial open")
            self.initializated = True
        else:
            print("Serial is already open")
            self.initializated = True
        if (self.Serial.isOpen() == False):
            print("I cant open serial {}".format(PORT))
            self.initializated = False
            return 0

        print("Serial id: {}".format(self.Serial))

    def Show_Log(self, fcn_name, info):
        print("Error ({}): {}".fromat(fcn_name, info))


    def Make_Frame_To_Send(self, fcn, value):
        """ create specific frame which is prepare for communication witch robot.
        Args:
            fcn ([type]): function eg.turn left, turn right, go straight
            value ([type]): this is value which is connected witch function. eg. turn left 60 - it means that robot has to tourn 60 degrees in left
        Returns:
            [list]: frame to send to robot
        """
        if fcn == 1 or fcn == 2:
            if value < 0 or value > 360:
                print("Rotation value is not correct")
                return False
        value_frame = []
        tmp = int(value / 253)
        for i in range(0, tmp):
            value_frame.append(253)
        value_frame.append(value % 253)
        print(value_frame)
        new_frame = []
        new_frame.append(int(255))
        new_frame.append(int(fcn))
        for val in value_frame:
            new_frame.append(val)
        new_frame.append(254)
        return new_frame


    def Send_Rotate(self, angle, direction):
        """ send angle and direction of rotation to robot.
        Args:
            angle ([int]): angle to rotate
            direction ([int]): direction to rotate
        """
        if direction == 0:
            fcn = 1  # go right
            LOG = "GO RIGHT "
        else:
            fcn = 2  # go left
            LOG = 'GO LEFT '
        FRAME = self.Make_Frame_To_Send(fcn, angle)
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent:", LOG, str(angle), " deg ---")
        except AttributeError:
            self.Show_Log("send_rotation", "Serial turned off")
        except:
            self.Show_Log("send_rotation", sys.exc_info())


    def Send_Go_Straight(self, distance):
        """ send distance do go staright to robot.
        Args:
            value ([int]): distance
        """
        distance = int(distance * 2.1)
        if distance < 0:
            self.Show_Log("send_go_straight", "Value < 0")
            return

        FRAME = self.Make_Frame_To_Send(3, distance)  # 3-go straight
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            # print(FRAME.encode())
            print("--- Sent: GO STRAIGHT", str(distance), " ---")
        except AttributeError:
            self.Show_Log("send_go_straight", "Serial turned off")
        except:
            self.Show_Log("send_go_straight", sys.exc_info())


    def Send_Take_Pallet(self, level):
        """ send command to take pallet from Lvl level
        """
        if level < 0 or level > 3:
            self.Show_Log("send_take_pallet", "Wrong level (0 <= level <= 3")
        FRAME = self.Make_Frame_To_Send(4, level)  # 4-take pallet
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent: Take pallet from level ", str(level), " ---")
        except AttributeError:
            self.Show_Log("send_go_straight", "Serial turned off")
        except:
            self.Show_Log("send_take_pallet", sys.exc_info())


    def Send_Put_Pallet(self, level):
        """ send command to put pallet on Lvl level
        """
        if level < 0 or level > 3:
            self.Show_Log("send_put_pallet", "Wrong level (0 <= level <= 3")
        FRAME = self.Make_Frame_To_Send(5, level)  # 5-put pallet
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent: Put pallet on level ", str(level), "  ---")
        except AttributeError:
            self.Show_Log("send_go_straight", "Serial turned off")
        except:
            self.Show_Log("send_put_pallet", sys.exc_info())