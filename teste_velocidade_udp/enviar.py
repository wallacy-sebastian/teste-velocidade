import socket
import time
import threading
from bufferPacotes import BufferPacotes
from pacote import Pacote

parar = False
tamanhoPacote = 512
quantidadeMaximaPacotes = 256
tamanhoBuffer = 30720
tempoEsperaMaximo = 5
buffer = BufferPacotes(tamanhoPacote, quantidadeMaximaPacotes, tamanhoBuffer, tempoEsperaMaximo)
confirmados = []
mutexConfirmados = threading.Lock()
delay = 0.004
HOST = 'localhost'
PORT = 5000
ADDRESS = (HOST, PORT)
dados = bytes()

for i in range(0, 500):
    dados = bytes().join([dados, b'a'])

def __modificarConfirmados(inserir = False):
    numero = False

    mutexConfirmados.acquire()
    try:
        if not inserir:
            numero = confirmados.pop(0)
        else:
            confirmados.append(inserir)
    except:
        numero = False
    finally:
        mutexConfirmados.release()

    return numero

def inserirDados():
    global parar
    while not parar:
        buffer.inserirDados(dados)

    print("Terminou t1")

def criarPacotes():
    global parar
    while not parar:
        buffer.criarPacotes()

    print("Terminou t2")

def enviarPacotes(sock):
    global parar
    while not parar:
        pacote = buffer.obterPacote()
        if pacote:
            sock.sendall(pacote)
        time.sleep(delay)

    print("Terminou t3")

def confirmarTransmissao():
    global parar
    inicio = time.time()
    agora = time.time()
    while (agora - inicio) < 20:
        numero = __modificarConfirmados()
        if numero:
            buffer.confirmarTransmissao(numero)

        time.sleep(delay)

        agora = time.time()

    parar = True
    print('')
    buffer.encerrar()
    print("Terminou t4")

# Inicializando client
print("Configurando cliente UDP")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(ADDRESS)
sock.settimeout(10.0)
sock.sendall(b'1')

# Enviando pacotes
print("Enviando pacotes ao servidor")

buffer.iniciar()

t1 = threading.Thread(target=inserirDados, args=())
t1.start()

t2 = threading.Thread(target=criarPacotes, args=())
t2.start()

t3 = threading.Thread(target=enviarPacotes, args=(sock,))
t3.start()

t4 = threading.Thread(target=confirmarTransmissao, args=())
t4.start()

sock.settimeout(2.0)

while not parar:
    try:
        numero = int.from_bytes(sock.recv(8), byteorder='little')
        __modificarConfirmados(numero)
    except:
        continue


sock.sendall(Pacote(999999, tamanhoPacote).montar())

print('\nEncerrando teste e obtendo estatísticas...\n')
t1.join()
t2.join()
t3.join()
t4.join()
# Limpando buffers e sockets
sock.close()

print("Upload")
print("Taxa de pacotes/s: %.2f" % buffer.obterTaxaPacotesSegundo())
print("Taxa de bits/s: %.2f" % buffer.obterTaxaBitsSegundo())
print("Tempo total executado: %.2f segundos" % buffer.obterTempoTotal())
print("Total de bits transmitidos: %.2f bits" % buffer.obterTotalBits())