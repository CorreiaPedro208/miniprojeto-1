#!/usr/bin/env python3
"""
Verificador de respostas do mini-projeto TrilhaSonora.

Confere o respostas.json contra a amostra pública (gabarito_publico.json,
as 20 primeiras consultas). A correção completa só sai depois da entrega.

Uso:
    python verificar.py respostas.json

Formato esperado de respostas.json:
    {
      "1": 8.3,
      "2": ["t000041", "t000107"],
      "3": null,
      ...
    }
As chaves são os ids das consultas (como string) e os valores seguem as
regras canônicas do enunciado. Floats são comparados com tolerância.
"""

import argparse
import json
import sys

TOLERANCIA = 1e-6
MAX_ERROS_EXIBIDOS = 10


def valores_iguais(esperado, obtido):
    if esperado is None or obtido is None:
        return esperado is None and obtido is None
    numericos = (int, float)
    if isinstance(esperado, numericos) and isinstance(obtido, numericos):
        if isinstance(esperado, bool) or isinstance(obtido, bool):
            return esperado == obtido
        return abs(float(esperado) - float(obtido)) < TOLERANCIA
    return esperado == obtido


def main():
    parser = argparse.ArgumentParser(description="Verifica respostas.")
    parser.add_argument("respostas", help="caminho do respostas.json")
    parser.add_argument("--gabarito", default="gabarito_publico.json",
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        with open(args.respostas, encoding="utf-8") as arquivo:
            respostas = json.load(arquivo)
    except FileNotFoundError:
        sys.exit(f"ERRO: arquivo não encontrado: {args.respostas}")
    except json.JSONDecodeError as erro:
        sys.exit(f"ERRO: {args.respostas} não é um JSON válido ({erro})")

    if not isinstance(respostas, dict):
        sys.exit("ERRO: respostas.json deve ser um objeto "
                 '{"id_da_consulta": resposta, ...}')

    with open(args.gabarito, encoding="utf-8") as arquivo:
        gabarito = json.load(arquivo)

    acertos = 0
    erros = []
    for id_consulta, esperado in gabarito.items():
        if id_consulta not in respostas:
            erros.append((id_consulta, esperado, "<ausente>"))
        elif valores_iguais(esperado, respostas[id_consulta]):
            acertos += 1
        else:
            erros.append((id_consulta, esperado, respostas[id_consulta]))

    total = len(gabarito)
    print(f"Resultado: {acertos}/{total} consultas corretas "
          f"({100 * acertos / total:.1f}%)")

    extras = set(respostas) - set(gabarito)
    if extras and len(gabarito) < 100:
        # No modo público é normal ter respostas além da amostra.
        print(f"(ignoradas {len(extras)} respostas fora da amostra pública)")

    if erros:
        print(f"\nPrimeiros erros (até {MAX_ERROS_EXIBIDOS}):")
        for id_consulta, esperado, obtido in erros[:MAX_ERROS_EXIBIDOS]:
            print(f"  consulta {id_consulta}: esperado={esperado!r} "
                  f"obtido={obtido!r}")
        sys.exit(1)

    print("Tudo certo na amostra verificada. ✔")


if __name__ == "__main__":
    main()
