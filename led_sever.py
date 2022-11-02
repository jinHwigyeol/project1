#!/usr/bin/python3
import RPi.GPIO as GPIO
from ast import Pass
from bmp280 import BMP280
from smbus2 import SMBus
import time
from gpiozero import LED
import socket

bus = SMBus(1) # use i2c bus1
bmp280 = BMP280(i2c_dev=bus)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
p = GPIO.PWM(led_pin, 500)
p.start(0)

host = ''
port = 10001
buff_size = 128
conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
conn_sock.bind(server_address)
conn_sock.listen(1)
led = LED(4)
led.off()

while True:
    #print("waiting for a command...")
    data_sock, address = conn_sock.accept()
    command = data_sock.recv(buff_size)
    #print("recevied command: {}".format(command.decode()))
    cmd = command.decode()

    try:
        if cmd.upper() == 'MID':
            led.on()
            p.ChangeDutyCycle(50)
            reply = "LED turned MID"
            data_sock.sendall(reply.encode())
        elif cmd.upper() == 'OFF':
            led.off()
            p.ChangeDutyCycle(0)
            reply = "LED turned OFF"
            data_sock.sendall(reply.encode())
        elif cmd.upper()== 'MAX':
            led.on()
            p.ChangeDutyCycle(100)
            reply = "LED turned MAX"
            data_sock.sendall(reply.encode())
        elif cmd.upper()== 'TEM':
            temperature = bmp280.get_temperature()
            pressure = bmp280.get_pressure()
            print("Temperature = {:.2f}C".format(temperature))
            print("Pressure = {:.1f}hPa".format(pressure))
            print("=======================")
        else:
            reply = "command {} not supported".format(cmd)
            data_sock.sendall(reply.encode())
    except Exception as e:
        print("Exception: {}".format(str(e)))
    data_sock.close()

GPIO.cleanup()