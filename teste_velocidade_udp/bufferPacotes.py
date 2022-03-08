import threading
import time
from pacote import Pacote


class BufferPacotes():
    ## Limitações
    quantidadePacotesPermitido = 0
    tamanhoPacote = 0
    tamanhoBufferPermitido = 0

    ## Informações relevantes para a classe
    ultimoPacoteCriado = -1
    pacotes = {}
    pacotesEspera = {}
    dados = bytes()

    ## Estatísticas
    erros = []
    tempoEspera = 0
    pacotesEnviados = 0
    tempoMedioEnvio = 0
    taxaBitsS = 0
    taxaPacotesS = 0
    tempoTotal = 0
    totalBits = 0
    inicio = 0

    ## Variáveis auxiliares de threading
    mutexDados = threading.Lock()
    mutexPacotes = threading.Lock()
    mutexPacotesEspera = threading.Lock()

    def __init__(self, tamanhoPacote, quantidadeMaximaPacotes, tamanhoBuffer, tempoEsperaMaximo) -> None:
        self.tamanhoPacote = tamanhoPacote
        self.quantidadePacotesPermitido = quantidadeMaximaPacotes
        self.tamanhoBufferPermitido = tamanhoBuffer
        self.tempoEspera = tempoEsperaMaximo

    def __modificarDados(self, inserir = False):
        dados = bytes()

        self.mutexDados.acquire()
        try:
            if not inserir:
                dados = self.dados
                self.dados = bytes()
            else:
                self.dados = bytes().join([self.dados, inserir])
        except:
            print("Não foi possível modificar os dados.")
        finally:
            self.mutexDados.release()

        return dados

    def __modificarPacotes(self, chave, inserir = False):
        self.mutexPacotes.acquire()
        try:
            if not inserir:
                pacote = self.pacotes.pop(chave)
            else:
                pacote = {
                    "pacote": inserir,
                    "momentoEnviado": 0
                }

                self.pacotes[chave] = pacote
        except:
            print("Não foi possível modificar os pacotes.")
            pacote = False
        finally:
            self.mutexPacotes.release()

        return pacote

    def iniciar(self):
        self.inicio = time.time()

    def criarPacotes(self):
        dados = self.__modificarDados()
        tamanhoPacotePermitido = Pacote(-1, self.tamanhoPacote).obterTamanhoDadosPermitido()

        for i in range(0, len(dados), tamanhoPacotePermitido):
            inicio = time.time()
            agora = time.time()
            while (agora - inicio) < 5:
                if len(self.pacotes) < self.quantidadePacotesPermitido:
                    break
                agora = time.time()

            if (agora - inicio) >= 5:
                break
            pacote = Pacote(self.ultimoPacoteCriado+1, self.tamanhoPacote)
            pacote.inserirDados(self.dados[i:(i + tamanhoPacotePermitido)])
            self.ultimoPacoteCriado += 1
            self.__modificarPacotes(self.ultimoPacoteCriado, pacote.montar())

    def __modificarPacotesEspera(self, chave = 0, inserir = False):
        pacote = bytes()

        self.mutexPacotesEspera.acquire()
        try:
            if not inserir:
                pacote = self.pacotesEspera.pop(chave)
            else:
                self.pacotesEspera[chave] = inserir
        except:
            print("O pacote já foi enviado.")
            pacote = False
        finally:
            self.mutexPacotesEspera.release()

        return pacote

    def obterPacote(self):
        erroEnvio = False
        try:
            if len(self.pacotesEspera) > 0:
                numero = list(self.pacotesEspera)[0]
                if (time.time() - self.pacotesEspera[numero]["momentoEnviado"]) > self.tempoEspera:
                    erroEnvio = True

            if erroEnvio:
                pacote = self.__modificarPacotesEspera(numero)
                if pacote:
                    agora = time.time()
                    pacote["momentoEnviado"] = agora
                    self.__modificarPacotesEspera(numero, pacote)
                    self.erros.append(numero)
                else:
                    return False
            else:
                numero = list(self.pacotes)[0]
                pacote = self.__modificarPacotes(numero)
                agora = time.time()
                pacote["momentoEnviado"] = agora

                self.__modificarPacotesEspera(numero, pacote)

            return pacote["pacote"]
        except:
            print("Nenhum pacote foi obtido")
            return False

    def inserirDados(self, dados):
        inicio = time.time()
        agora = time.time()
        while (agora - inicio) < 5:
            if (len(self.dados) + len(dados)) < self.tamanhoBufferPermitido:
                self.__modificarDados(dados)
                break
            agora = time.time()

    def confirmarTransmissao(self, chave):
        self.__modificarPacotesEspera(chave)
        self.pacotesEnviados += 1

    def obterTaxaPacotesSegundo(self):
        return self.taxaPacotesS

    def obterTaxaBitsSegundo(self):
        return self.taxaBitsS

    def obterTotalBits(self):
        self.totalBits = self.taxaBitsS * self.tempoTotal

        return self.totalBits

    def obterTempoTotal(self):
        return self.tempoTotal
    
    def encerrar(self):
        agora = time.time()
        self.tempoTotal = agora - self.inicio
        self.taxaPacotesS = self.pacotesEnviados / self.tempoTotal
        self.taxaBitsS = self.tamanhoPacote * self.taxaPacotesS * 8