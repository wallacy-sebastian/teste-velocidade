# -*- coding: utf-8 -*-
import socket
import time
from sys import getsizeof

HOST = "localhost"
PORT = 7000

ponto_env = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ponto_env.connect((HOST, PORT))

print("CONECTADO")

tam = getsizeof("Redes é a melhor matéria") #tamanho do pacote

inicio = time.time()
numero_pacotes = 1

while True:
    progresso = numero_pacotes*tam
    packet = "Redes é a melhor matéria"
    sent = ponto_env.send(packet.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")
    fim = time.time()
    if(fim - inicio) >= 20:
        break
    print("\r", end='')
    print(f"Bytes enviados: {progresso*8} B", end='')
    numero_pacotes += 1
    
ponto_env.close()
print("\n")
print(f"Número de pacotes: {numero_pacotes}")
print(f"Upload\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(fim-inicio))}\nBits/s: {'{:,.2f}'.format((numero_pacotes*tam*8)/(fim-inicio))}")
print(f"Total de bytes: {'{:,}'.format(numero_pacotes*tam)}\nTempo: {fim-inicio}")

###########################################################

HOST = "localhost"
PORT = 6000
ADDRESS = (HOST, PORT)

# Inicializando client
print("Configurando cliente UDP")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(ADDRESS)
time.sleep(1)

print("CONECTADO")

tam = getsizeof("Redes é a melhor matéria") #tamanho do pacote

inicio = time.time()
numero_pacotes = 1

while True:
    progresso = numero_pacotes*tam
    packet = "Redes é a melhor matéria"
    sent = sock.send(packet.encode())
    if sent == 0:
        raise RuntimeError("socket connection broken")
    fim = time.time()
    if(fim - inicio) >= 20:
        break
    print("\r", end='')
    print(f"Bytes enviados: {progresso*8} B", end='')
    numero_pacotes += 1

sock.sendall((0).to_bytes(1, 'little'))
sock.close()
print("\n")
print(f"Número de pacotes: {numero_pacotes}")
print(f"Upload\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(fim-inicio))}\nBits/s: {'{:,.2f}'.format((numero_pacotes*tam*8)/(fim-inicio))}")
print(f"Total de bytes: {'{:,}'.format(numero_pacotes*tam)}\nTempo: {fim-inicio}")
