import serial
import sys
import time

class Communication:
    def __init__(self):
        print("Tworzę klasę Communication")
        self.port = None
        self.baudrate = None
        self.Serial = None
        self.initializated = False

    def Initialize(self, PORT, BAUDRATE):
        self.Serial = None
        print("+++ Inicjalizacja komunikacji")
        self.port = PORT
        self.baudrate = BAUDRATE
        try:
            self.Serial = serial.Serial(self.port, self.baudrate)
        except:
            print("Can't open serial port: ", self.port)
            if type(self.Serial) is type(None):
                print("nonetype")
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
            value_frame.append(253)
        value_frame.append(value % 253)
        print(value_frame)
        tmpFRAME = []
        tmpFRAME.append(int(255))
        tmpFRAME.append(int(fcn))
        for val in value_frame:
            tmpFRAME.append(val)
        tmpFRAME.append(254)
        return tmpFRAME


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
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent:", LOG, str(angle), " deg ---")
        except AttributeError:
            self.Show_Log("send_rotation", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_rotation", sys.exc_info())

    # Function send distance do go staright to robot.
    def Send_Go_Straight(self, value):
        value = int(value * 2.1)
        if value < 0:
            self.Show_Log("send_go_straight", "Wartość < 0")
            return

        FRAME = self.Make_Frame_To_Send(3, value)  # 3-go straight
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            # print(FRAME.encode())
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
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent: Take pallet from level ", str(Lvl), " ---")
        except AttributeError:
            self.Show_Log("send_take_pallet", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_take_pallet", sys.exc_info())

    # Function send command to put pallet on Lvl level
    def Send_Put_Pallet(self, Lvl):
        if Lvl < 0 or Lvl > 3:
            self.Show_Log("send_put_pallet", "Wyrano nieprawidłowy poziom (0<=Poziom<=3")
        FRAME = self.Make_Frame_To_Send(5, Lvl)  # 5-put pallet
        try:
            print(serial.to_bytes(FRAME))
            self.Serial.write(serial.to_bytes(FRAME))
            print("--- Sent: Put pallet on level ", str(Lvl), "  ---")
        except AttributeError:
            self.Show_Log("send_put_pallet", "Wyłączono opcję SERIAL lub podano nieprawidłową klasę")
        except:
            self.Show_Log("send_put_pallet", sys.exc_info())

    def Read_Data_From_Robot(self):
        # tmp = None
        # while tmp != 'd':
        #     tmp = input("Press the button: ")
        # return True
        data = None

        while data == None:
            print("Nonee")
            self.Serial.flushInput()
            data = self.Serial.readline()
            print(type(data))
            time.sleep(0.2)
            print(data)
            if int(data[0]) == 1:
                print("True")
                return True
            else:
                print("False")
                return False

if __name__=="__main__":

    Comm = Communication()
    print(Comm.Make_Frame_To_Send(1,100))
    Comm.Initialize("COM14", 9600)
    # while True:
    #     Comm.Read_Data_From_Robot()
    inputt = None
    while inputt!="q":
        inputt = input("Press: ")
        # Comm.Read_Data_From_Robot()
        # Comm.Serial.write(b'\xff\x01d\xfe')
        # Comm.Send_Go_Straight(174)
        # Comm.Send_Rotate(1,0)
        # Comm.Send_Take_Pallet(3)
        # Comm.Send_Put_Pallet(1)
        # inputt = input("Press: ")
        # Comm.Send_Take_Pallet(3)
        # Comm.Read_Data_From_Robot()

    # ack = True
    # while True: #ack != False:
    #     Comm.Send_Rotate(1, 2)
    #     ack=Comm.Read_Data_From_Robot()
    #     Comm.Send_Go_Straight(1)
    #     ack = Comm.Read_Data_From_Robot()
    #     Comm.Send_Rotate(1, 1)