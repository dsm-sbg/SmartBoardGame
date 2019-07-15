import sys
import time
import serial

Dice = 7
buff = [1, 1, 1]
endFlag = False

if len(sys.argv) < 2:
    print(sys.argv[0] +" [Turn]")
    sys.exit(-1)
turn = sys.argv[1]

f = open("result", 'w')

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
print(ser.portstr)

def SendData(data):
    packet = [0x02]
    packet.append(data)
    packet.append(0x03)

    ser.write(packet)

    print("Sent 0x{} 0x{} 0x{}".format(0x02, data, 0x03))

if __name__ == "__main__":
    while True:
        buff = ser.read(3)

        if buff[0] == 0x02:
            print('buff[1]: ', buff[1])
            if buff[1] == 83:
                if endFlag == True:
                    f.write(turn + '\n' + str(Dice))
                    sys.exit(0)
                SendData(0x50)

            elif 48 < buff[1] and buff[1] < 56:
                Dice = buff[1] - 48
                endFlag = True
                SendData(0x49)

            else:
                print("Error: buff[1] is ", buff[1])

            if buff[2] is not 0x03:
                print('buff[2]: ', buff[2])
        else:
            print('buff[0]: ', buff[0])

        time.sleep(0.3)
