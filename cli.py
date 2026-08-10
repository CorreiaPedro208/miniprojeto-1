import sys
from catalogo import Catalogo


def mostrar_menu():
    print()
    print("TrilhaSonora")
    print("============")
    print("1. Listar todos os usuários")
    print("2. Ver playlist completa de um usuário")
    print("3. Conteúdo na posição N da playlist")
    print("4. Interseção de playlists (N usuários)")
    print("5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)")
    print("6. Conteúdos de um gênero")
    print("7. Enfileirar conteúdo na fila de reprodução")
    print("8. Tocar próximo da fila")
    print("9. Ver fila atual")
    print("0. Sair")


def ler_inteiro(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        return None


def pedir_usuario_id(catalogo, mensagem):
    nome = input(mensagem).strip()
    usuario_id = catalogo.buscar_usuario_por_nome(nome)
    if usuario_id is None:
        print(f"Não existe usuário chamado {nome}.")
    return usuario_id


def mostrar_usuarios(catalogo):
    for nome in catalogo.listar_usuarios():
        print(nome)


def ver_playlist(catalogo):
    usuario_id = pedir_usuario_id(catalogo, "Nome do usuário: ")
    if usuario_id is None:
        return
    playlist = catalogo.playlist_de(usuario_id)
    for posicao, conteudo_id in enumerate(playlist, start=1):
        print(f"{posicao}. {catalogo.descricao_de(conteudo_id)}")


def ver_conteudo_na_posicao(catalogo):
    nome = input("Nome do usuário: ").strip()
    usuario_id = catalogo.buscar_usuario_por_nome(nome)
    if usuario_id is None:
        print(f"Não existe usuário chamado {nome}.")
        return

    playlist = catalogo.playlist_de(usuario_id)
    print(f"Playlist de {nome} tem {len(playlist)} itens (posições 1 a {len(playlist)}).")

    posicao = ler_inteiro("Qual posição? > ")
    if posicao is None:
        print("Digite um número.")
        return

    conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao - 1)
    if conteudo_id is None:
        print("Não existe conteúdo nessa posição.")
        return
    print(catalogo.descricao_de(conteudo_id))


def ver_intersecao(catalogo):
    quantidade = ler_inteiro("Quantos usuários? > ")
    if quantidade is None or quantidade < 2:
        print("Informe um número maior que 1.")
        return

    usuario_ids = []
    for numero in range(quantidade):
        usuario_id = pedir_usuario_id(catalogo, f"Nome do usuário {numero + 1}: ")
        if usuario_id is None:
            return
        usuario_ids.append(usuario_id)

    comuns = catalogo.intersecao_playlists(usuario_ids)
    if len(comuns) == 0:
        print("Não há conteúdo em comum.")
        return
    for conteudo_id in comuns:
        print(catalogo.descricao_de(conteudo_id))


def ver_dados_do_conteudo(catalogo):
    conteudo_id = input("Id do conteúdo: ").strip()
    descricao = catalogo.descricao_de(conteudo_id)
    if descricao is None:
        print("Não existe conteúdo com esse id.")
        return

    print(descricao)
    print("Rating:", catalogo.rating_de(conteudo_id))
    print("Duração (seg):", catalogo.duracao_total_de(conteudo_id))
    print("Gêneros:", ", ".join(catalogo.generos_de(conteudo_id)))
    print("Plataformas:", ", ".join(catalogo.plataformas_de(conteudo_id)))
    print("Adicionado em:", catalogo.data_adicionado_de(conteudo_id))

    execucoes = catalogo.execucoes_de(conteudo_id)
    if execucoes is not None:
        print("Execuções:", execucoes)


def ver_conteudos_do_genero(catalogo):
    genero = input("Gênero: ").strip()
    ids = catalogo.conteudos_do_genero(genero)
    if len(ids) == 0:
        print("Nenhum conteúdo desse gênero.")
        return
    print(f"{len(ids)} conteúdos:")
    for conteudo_id in ids:
        print(catalogo.descricao_de(conteudo_id))


def enfileirar_conteudo(catalogo):
    conteudo_id = input("Id do conteúdo: ").strip()
    if catalogo.enfileirar(conteudo_id):
        print(f"Enfileirado: {catalogo.descricao_de(conteudo_id)}")
    else:
        print("Não existe conteúdo com esse id.")


def tocar_proximo(catalogo):
    conteudo_id = catalogo.proximo()
    if conteudo_id is None:
        print("A fila está vazia.")
    else:
        print(f"Tocando: {catalogo.descricao_de(conteudo_id)}")


def ver_fila(catalogo):
    fila = catalogo.fila_atual()
    if len(fila) == 0:
        print("A fila está vazia.")
        return
    for posicao, conteudo_id in enumerate(fila, start=1):
        print(f"{posicao}. {catalogo.descricao_de(conteudo_id)}")


def main():
    catalogo = Catalogo(sys.argv[1])

    while True:
        mostrar_menu()
        opcao = input("> ").strip()

        if opcao == "0":
            print("Até mais.")
            break
        elif opcao == "1":
            mostrar_usuarios(catalogo)
        elif opcao == "2":
            ver_playlist(catalogo)
        elif opcao == "3":
            ver_conteudo_na_posicao(catalogo)
        elif opcao == "4":
            ver_intersecao(catalogo)
        elif opcao == "5":
            ver_dados_do_conteudo(catalogo)
        elif opcao == "6":
            ver_conteudos_do_genero(catalogo)
        elif opcao == "7":
            enfileirar_conteudo(catalogo)
        elif opcao == "8":
            tocar_proximo(catalogo)
        elif opcao == "9":
            ver_fila(catalogo)
        else:
            print("Opção inválida.")


main()
