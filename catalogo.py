import json
from collections import deque


def converter_rating(rating):
    if rating is None:
        return None
    if isinstance(rating, str):
        rating = rating.replace(",", ".")
    return float(rating)


def converter_data(data):
    if data is None:
        return None
    if "/" in data:
        dia, mes, ano = data.split("/")
        return f"{ano}-{mes}-{dia}"
    return data


def achatar_generos(generos):
    if isinstance(generos, str):
        return [generos]
    planos = []
    for item in generos:
        planos.extend(achatar_generos(item))
    return planos


class Conteudo:
    def __init__(self, dados):
        self.id = dados["id"]
        self.titulo = dados["titulo"]
        self.artista = dados["artista"]
        self.ano = dados["ano"]
        self.rating = converter_rating(dados.get("rating"))
        self.generos = sorted(achatar_generos(dados.get("generos", [])))
        self.plataformas = sorted(dados.get("plataformas", []))
        self.data_adicionado = converter_data(dados.get("data_adicionado"))


class Musica(Conteudo):
    def __init__(self, dados):
        super().__init__(dados)
        self.nome_do_tipo = "música"
        self.duracao_seg = dados.get("duracao_seg")
        self.engajamento = dados.get("engajamento", {})


class Album(Conteudo):
    def __init__(self, dados):
        super().__init__(dados)
        self.nome_do_tipo = "álbum"
        self.faixas = dados.get("faixas", [])


class Usuario:
    def __init__(self, dados):
        self.id = dados["id"]
        self.nome = dados["nome"]
        self.playlist = dados["playlist"]

    def item_na_posicao(self, posicao):
        if posicao < 0 or posicao >= len(self.playlist):
            return None
        return self.playlist[posicao]


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

        self._ids_por_genero = {}
        for conteudo in self._conteudos.values():
            for genero in conteudo.generos:
                if genero not in self._ids_por_genero:
                    self._ids_por_genero[genero] = []
                self._ids_por_genero[genero].append(conteudo.id)

        for ids in self._ids_por_genero.values():
            ids.sort()

        self._usuarios = {}
        self._id_por_nome_minusculo = {}
        for registro in dados["usuarios"]:
            usuario = Usuario(registro)
            self._usuarios[usuario.id] = usuario
            self._id_por_nome_minusculo[usuario.nome.lower()] = usuario.id

        # fila de reprodução, começa vazia
        self._fila = deque()

    def listar_usuarios(self) -> list[str]:
        nomes = []
        for usuario in self._usuarios.values():
            nomes.append(usuario.nome)
        return sorted(nomes)

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        return self._id_por_nome_minusculo.get(nome.lower())

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        return list(usuario.playlist)

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        return usuario.item_na_posicao(posicao)

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        conjuntos = []
        for usuario_id in usuario_ids:
            usuario = self._usuarios.get(usuario_id)
            if usuario is None:
                return []
            conjuntos.append(set(usuario.playlist))

        if len(conjuntos) == 0:
            return []

        comuns = conjuntos[0]
        for conjunto in conjuntos[1:]:
            comuns = comuns & conjunto
        return sorted(comuns)

    def rating_de(self, conteudo_id: str) -> float | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return conteudo.rating

    def generos_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return list(conteudo.generos)

    def plataformas_de(self, conteudo_id: str) -> list[str] | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return list(conteudo.plataformas)

    def data_adicionado_de(self, conteudo_id: str) -> str | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return conteudo.data_adicionado

    def conteudos_do_genero(self, genero: str) -> list[str]:
        return list(self._ids_por_genero.get(genero, []))

    def descricao_de(self, conteudo_id: str) -> str | None:
        conteudo = self._conteudos.get(conteudo_id)
        if conteudo is None:
            return None
        return f"{conteudo.titulo}, de {conteudo.artista} ({conteudo.nome_do_tipo})"

    def enfileirar(self, conteudo_id: str) -> bool:
        if conteudo_id not in self._conteudos:
            return False
        self._fila.append(conteudo_id)
        return True

    def proximo(self) -> str | None:
        if len(self._fila) == 0:
            return None
        return self._fila.popleft()

    def fila_atual(self) -> list[str]:
        return list(self._fila)
