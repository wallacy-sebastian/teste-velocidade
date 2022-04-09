from sys import getsizeof
import socket
import time

HOST = "localhost"
PORT = 7000

print("Teste de Velocidade TCP")
print("Escolha qual o tipo conexão será feita.")
enviar = int(input("Enviar (1); Receber (2)\n"))

if enviar == 1:
    ponto_env = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ponto_env.connect((HOST, PORT))

    print("CONECTADO")

    tam = getsizeof("Redes é a melhor matéria") #tamanho do pacote

    inicio = time.time()
    numero_pacotes = 0
    packet = "Redes é a melhor matéria".encode()
    progresso = 0

    while True:
        fim = time.time()
        if(fim - inicio) >= 20:
            break
        sent = ponto_env.send(packet)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        progresso += sent
        #numero_pacotes += 1
        print(f"\rBits enviados: {progresso*8}", end='')
        
    numero_pacotes = progresso // getsizeof(packet)
    ponto_env.close()
    print("\n")
    print(f"Número de pacotes: {numero_pacotes}")
    print(f"Upload\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(fim-inicio))}")
    print(f"Bits/s: {'{:,.2f}'.format((progresso*8)/(fim-inicio))}")
    print(f"Total de bytes: {'{:,}'.format(progresso)}")
    print(f"Tempo: {fim-inicio}")
else:
    ponto_rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ponto_rec.bind((HOST,PORT))
    ponto_rec.listen(1)
    print("Esperando conexão ...")

    conn,addr= ponto_rec.accept()
    print(addr)

    inicio = time.time()
    numero_pacotes = 0
    tam = getsizeof("Redes é a melhor matéria")
    progresso = 0

    while True:
        dados = conn.recv(tam)
        fim = time.time()
        if not dados:
            print("\nFim da conexão\n")
            break
        progresso += getsizeof(dados) - getsizeof(b'')
        #numero_pacotes += 1
        print(f"\rBits recebidos: {progresso*8}", end='')

    numero_pacotes = progresso // getsizeof("Redes é a melhor matéria".encode())
    ponto_rec.close()
    print(f"Número de pacotes recebidos: {numero_pacotes}")
    print(f"Download\nPacotes/s: {'{:,.2f}'.format(numero_pacotes/(fim-inicio))}")
    print(f"Bits/s: {'{:,.2f}'.format((progresso*8)/(fim-inicio))}")
    print(f"Total de bytes: {'{:,}'.format(progresso)}")
    print(f"Tempo: {fim-inicio}")
