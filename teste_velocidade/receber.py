from sys import getsizeof
import socket
import time

HOST = "localhost"
PORT = 7000
ponto_rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ponto_rec.bind((HOST,PORT))
ponto_rec.listen(1)
# ponto_rec.settimeout(10.0)
print("Esperando conexão ...")

conn,addr= ponto_rec.accept()

start = time.time()
numero_pacotes = 1
tam = getsizeof("Redes é a melhor matéria")

while True:
    dados=conn.recv(getsizeof("Redes é a melhor matéria"))
    end = time.time()
    if(end-start) >= 23:
        break
    if not dados:
        print("Fim da conexão")
        break
    print("\r", end='')
    print(f"numero de pacotes recebidos: {numero_pacotes}", end='')
    numero_pacotes += 1
ponto_rec.close()
print("\n")
print(f"Download\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(end-start))}")
print(f"Bits/s: {'{:,.2f}'.format((numero_pacotes*tam*8)/(end-start))}")
print(f"Total de bytes: {'{:,.2f}'.format(numero_pacotes*tam)}\nTempo: {end-start}")


##########################################################################

HOST = "localhost"
PORT = 6000
ponto_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ponto_rec.bind((HOST,PORT))
print("Esperando conexão ...")
data, address = ponto_rec.recvfrom(4)
print(address)

start = time.time()
numero_pacotes = 1
tam = getsizeof("Redes é a melhor matéria")

while True:
    dados=ponto_rec.recv(tam)
    end = time.time()
    if(end-start) >= 23:
        break
    if int.from_bytes(dados, "little") == 0:
        print("Fim da conexão")
        break
    print("\r", end='')
    print(f"numero de pacotes recebidos: {numero_pacotes}", end='')
    numero_pacotes += 1
ponto_rec.close()
print("\n")
print(f"Download\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(end-start))}")
print(f"Bits/s: {'{:,.2f}'.format((numero_pacotes*tam*8)/(end-start))}")
print(f"Total de bytes: {'{:,.2f}'.format(numero_pacotes*tam)}\nTempo: {end-start}")
