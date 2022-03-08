import socket
import time
from pacote import Pacote

# Server Setup
print("Configurando servidor UDP")
HOST = '10.90.67.91'
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(10.0)
tamanhoPacote = 512

print("Aguardando conexão...")
data, address = sock.recvfrom(4)
print(address)

# Recebendo pacotes
sock.settimeout(5.0)

print(f"Recebendo pacotes...")
qtdPacotes = 0
inicio = time.time()
while 1:
    pacote = sock.recv(tamanhoPacote)
    numero = Pacote(pacotePronto=pacote).obterNumero()
    if numero != 999999:
        sock.sendto(numero.to_bytes(6, "little"), address)
        qtdPacotes += 1
    else:
        break

agora = time.time()

print("\nCalculando estatísticas...\n")

print("Download")
print("Taxa de pacotes/s: :,%.2f" % (qtdPacotes / (agora - inicio)))
print("Taxa de bits/s: :,%.2f" % ((qtdPacotes * tamanhoPacote * 8) / (agora - inicio)))
print("Tempo total executado: :,%.2f segundos" % (agora - inicio))
print("Total de bits transmitidos: :,%.2f bits" % (qtdPacotes * tamanhoPacote * 8))

# Limpando buffers e sockets
sock.close()
