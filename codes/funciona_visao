import serial
import time

# Configurações da porta serial
port = '/dev/ttyTHS0'  # Ajuste conforme necessário
baudrate = 115200

# Inicializa a conexão serial
ser = serial.Serial(port, baudrate, timeout=1)
time.sleep(2)  # Aguarda a conexão ser estabelecida

def send_command(command):
    ser.write(command)

def read_response():
    response = ser.readline().decode('utf-8').strip()
    return response

def get_motor_speed():
    # Comando fictício para obter a velocidade do motor, ajuste conforme a documentação
    command = bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A])  # Exemplo de comando
    send_command(command)
    time.sleep(0.1)
    return read_response()

# Loop principal
try:
    while True:
        # Comando para girar lentamente (ajuste conforme necessário)
        duty_command = bytearray([0x01, 0x10, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A])  # Exemplo de comando
        send_command(duty_command)

        # Aguarda 4 segundos
        time.sleep(4)

        # Parar o motor
        stop_command = bytearray([0x01, 0x10, 0x00, 0x00, 0x00, 0x00, 0x84, 0x0A])  # Comando para parar
        send_command(stop_command)

        # Aguarda 2 segundos
        time.sleep(2)

        # Imprimir a velocidade do motor
        speed = get_motor_speed()
        print(f'Velocidade do motor: {speed}')

except KeyboardInterrupt:
    print("Programa interrompido.")

# Fechar a conexão
ser.close()
