import sys

class Pacote:
    header = {
        "numero": bytes("000000", encoding='utf8'),
        "tamanho": bytes("0000", encoding='utf8'),
        "transmitido": bytes("0", encoding='utf8')
    }

    dados = bytes()

    def __init__(self, numero = 0, tamanho = 0, pacotePronto = False) -> None:
        if not pacotePronto:
            self.header["numero"] = bytes(str(numero).zfill(6), encoding='utf8')
            self.header["tamanho"] = bytes(str(tamanho).zfill(4), encoding='utf8')
        else:
            self.header["numero"] = pacotePronto[0:6]
            self.header["tamanho"] = pacotePronto[6:10]
            self.header["transmitido"] = pacotePronto[10:11]
            self.dados = pacotePronto[11:]

    def obterNumero(self):
        return int(self.header["numero"])

    def obterTamanho(self):
        return int(self.header["tamanho"])

    def obterTransmitido(self):
        return bool(int(self.header["transmitido"]))

    def obterTamanhoDadosPermitido(self):
        return (self.obterTamanho() - 44)

    def obterTamanhoDados(self):
        return (sys.getsizeof(self.dados) - sys.getsizeof(bytes()))

    def inserirDados(self, dados):
        tamanhoDados = sys.getsizeof(dados) - sys.getsizeof(bytes())

        if tamanhoDados > self.obterTamanhoDadosPermitido():
            print("O tamanho dos dados é maior que o permitido no pacote")
            return False
        self.dados = dados
            
        return True

    def montar(self):
        header = bytes().join([self.header["numero"], self.header["tamanho"], self.header["transmitido"]])
        payload = self.dados

        pacote = bytes().join([header, payload])

        return pacote