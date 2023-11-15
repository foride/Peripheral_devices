import time
import serial
import threading


def read_from_port(port):
    while True:
        data = port.read_until('\r'.encode('utf-8'))
        try:
            data = data.decode('utf-8')-
            if data == '':
                continue
            print(data)
        except:
            continue


modem_port = serial.Serial("COM1", 9600, parity='N', stopbits=1, bytesize=8, xonxoff=True, timeout=5)
print('Port opened!\n')
t = threading.Thread(target=read_from_port, daemon=True, args=(modem_port,))
print('Made a listening thread!')
t.start()
while True:
    chose = input("Wpisz liczbe od 0 do 4\n"
                  "0 : Odbierz polaczenie\n"
                  "1 : Polaczenie z wpisanym numerem\n"
                  "2 : Wyslij komende AT\n"
                  "3 : Zakoncz polaczenie\n"
                  "4 : Zamknij port\n")

    if chose == "0":
        modem_port.write("ata\r".encode())
    elif chose == "1":
        number = input("Wpisz numer z ktorym chcesz sie polaczyc\n")
        message = number + '\r'
        print(f'Sending atd{number} ...')
        modem_port.write(message.encode())
    elif chose == "2":
        message = input("Wpisz komende AT\n")
        msg = message + '\r'
        print(f'Sending: {msg}')
        modem_port.write(msg.encode())
    elif chose == "3":
        print('Declining connection')
        modem_port.write("+++ath\r".encode())
    elif chose == "4":
        modem_port.close()
