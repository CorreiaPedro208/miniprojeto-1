import json
import sys
from catalogo import Catalogo


def responder_consultas(catalogo, consultas):
    respostas = {}
    for consulta in consultas:
        metodo = getattr(catalogo, consulta["tipo"])
        respostas[str(consulta["id"])] = metodo(**consulta["parametros"])
    return respostas


def main():
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2]

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, encoding="utf-8") as arquivo:
        consultas = json.load(arquivo)["consultas"]

    respostas = responder_consultas(catalogo, consultas)

    with open(caminho_respostas, "w", encoding="utf-8") as arquivo:
        json.dump(respostas, arquivo, ensure_ascii=False)

    print(f"{len(respostas)} respostas gravadas em {caminho_respostas}")


main()
