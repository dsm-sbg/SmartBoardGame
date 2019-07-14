import time
        gameDisplay.blit(pygame.image.load(players[2].path[0].replace('N', str(flag_ORDER))), tuple(players[2].pos))
import serial

Dice = 7

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

print(ser.portstr)

buff = [1, 1, 1]

def SendData(data):
    packet = [0x02]
    packet.append(data)
    packet.append(0x03)

    ser.write(packet)

    print("Sent 0x{} 0x{} 0x{}".format(0x02, data, 0x03))

##  while True:
##      SendData(0x50)
##      time.sleep(1)

def Pipe(data):
    print("Pushed Data to Pipe")

while True:
    buff = ser.read(3)

    if buff[0] == 0x02:
        print('buff[1]: ', buff[1])
        if buff[1] == 83:
            SendData(0x50)

        else:
            Dice = buff[1] - 48
            Pipe(Dice)
            SendData(0x4F)

        if buff[2] is not 0x03:
            print('buff[2]: ', buff[2])
    else:
        print('buff[0]: ', buff[0])

    time.sleep(0.01)
