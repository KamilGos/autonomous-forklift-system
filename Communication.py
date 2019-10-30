import serial
import sys
import time

class Communication:
    def __init__(self):
        print("Tworzę klasę Comminication")
        self.port = None
        self.baudrate = None
        self.Serial = None
        self.initializated = False

    def Initialize(self, PORT, BAUDRATE):
        print("+++ Inicjalizacja komunikacji")
        self.port = PORT
        self.baudrate = BAUDRATE
        try:
            self.Serial = serial.Serial(self.port, self.baudrate)
        except:
            print("Can't open serial port: ", self.port)
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
        print("!!! Błąd przesyłu danych. Funckja: ", fcn_name, " !!!")
        print("!!! Kod błędu: \n", info)

    # It create specific frame which is prepare for communication witch robot.
    # fcn   - function eg.turn left, turn right, go straight
    # value - this is value which is connected witch function. eg. turn left 60 - it means that robot has to tourn 60 degrees
    #        in left
    def Make_Frame_To_Send(self, fcn, value):
        if fcn == 1 or fcn == 2:
            if value < 0 or value > 360:
                print("Rotation value is not correct")
                return False
        value_frame = []
        tmp = int(value / 253)
        for i in range(0, tmp):
            value_frame.append('253')
        value_frame.append(str(value % 253))
        FRAME = '255' + str(fcn)
        for val in value_frame:
            FRAME = FRAME + val
        FRAME = FRAME + '254'
        return FRAME

    # Function send angle and direction of rotation to robot.
    def Send_Rotate(self, angle, direction):
        if direction == 0:
            fcn = 1  # go right
            LOG = "GO RIGHT "
        else:
            fcn = 2  # go left
            LOG = 'GO LEFT '
        FRAME = self.Make_Frame_To_Send(fcn, angle)
        try:
            self.Serial.write(FRAME.encode())
            print("--- Sent:", LOG, str(angle), " deg ---")
        except AttributeError:
            self.Show_Log("send_rotation", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_rotation", sys.exc_info())

    # Function send distance do go staright to robot.
    def Send_Go_Straight(self, value):
        if value < 0:
            self.Show_Log("send_go_straight", "Wartość < 0")
            return

        FRAME = self.Make_Frame_To_Send(3, value)  # 3-go straight
        try:
            self.Serial.write(FRAME.encode())
            print("--- Sent: GO STRAIGHT", str(value), " ---")
        except AttributeError:
            self.Show_Log("send_go_straight", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_go_straight", sys.exc_info())

    # Function send command to take pallet from Lvl level
    def Send_Take_Pallet(self, Lvl):
        if Lvl < 0 or Lvl > 3:
            self.Show_Log("send_take_pallet", "Wyrano nieprawidłowy poziom (0<=Poziom<=3")
            FRAME = self.Make_Frame_To_Send(4, Lvl)  # 4-take pallet
        try:
            self.Serial.write(FRAME.encode())
            print("--- Sent: Take pallet from level ", str(Lvl), " ---")
        except AttributeError:
            self.Show_Log("send_take_pallet", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_take_pallet", sys.exc_info())

    # Function send command to put pallet on Lvl level
    def Send_Put_Pallet(self, Lvl):
        if Lvl < 0 or Lvl > 3:
            self.Show_Log("send_put_pallet", "Wyrano nieprawidłowy poziom (0<=Poziom<=3")
            FRAME = self.Make_Frame_To_Send(4, Lvl)  # 4-take pallet
        try:
            self.Serial.write(FRAME.encode())
            print("--- Sent: Put pallet on level ", str(Lvl), "  ---")
        except AttributeError:
            self.Show_Log("send_put_pallet", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_put_pallet", sys.exc_info())

    def Read_Data_From_Robot(self):
        read_data = None
        self.Serial.flushInput()
        while read_data == None:
            data = self.Serial.readline()
            read_data = data.decode()
            time.sleep(0.1)
        if read_data[0] == str(1):
            return True
        else:
            return False


if __name__=="__main__":
    Comm = Communication()
    Comm.Initialize("COM14", 9600)
    Comm.Send_Go_Straight(100)
    Comm.Send_Rotate(30,1)