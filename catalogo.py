import json
from collections import deque


class Conteudo:
    def __init__(self, dados):
        self.id = dados["id"]
        self.titulo = dados["titulo"]
        self.artista = dados["artista"]
        self.ano = dados["ano"]
        self.rating = dados.get("rating")
        self.generos = dados.get("generos")
        self.plataformas = dados.get("plataformas")
        self.data_adicionado = dados.get("data_adicionado")


class Musica(Conteudo):
    def __init__(self, dados):
        super().__init__(dados)
        self.duracao_seg = dados.get("duracao_seg")
        self.engajamento = dados.get("engajamento", {})


class Album(Conteudo):
    def __init__(self, dados):
        super().__init__(dados)
        self.faixas = dados.get("faixas", [])


class Usuario:
    def __init__(self, dados):
        self.id = dados["id"]
        self.nome = dados["nome"]
        self.playlist = dados["playlist"]


def criar_conteudo(dados):
    if dados["tipo"] == "musica":
        return Musica(dados)
    else:
        return Album(dados)


class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self._conteudos = {}
        for registro in dados["conteudos"]:
            conteudo = criar_conteudo(registro)
            self._conteudos[conteudo.id] = conteudo

        self._usuarios = {}
        for registro in dados["usuarios"]:
            usuario = Usuario(registro)
            self._usuarios[usuario.id] = usuario

        # fila de reprodução, começa vazia
        self._fila = deque()
