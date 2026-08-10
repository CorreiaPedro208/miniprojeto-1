# Mini-Projeto TrilhaSonora

Analisador do catálogo da TrilhaSonora, uma plataforma fictícia de streaming musical. O projeto tem a classe Catalogo, um modo batch que responde 10 mil consultas de uma vez e um menu interativo no terminal.

## Como rodar

Modo batch (carrega sempre o `catalogo_final.json`):

```bash
python3 main.py consultas.json respostas.json
```

Menu interativo:

```bash
python3 cli.py catalogo_final.json
```

Não precisa instalar nada, só Python 3.10 ou mais novo.

## Arquivos

- catalogo.py: a classe Catalogo e as classes auxiliares
- main.py: modo batch
- cli.py: menu interativo
- respostas.json: gerado pelo main.py

## As classes que criei

### Conteudo, Musica e Album

Conteudo é a classe base e guarda o que música e álbum têm em comum: id, título, artista, ano, rating, gêneros, plataformas e data. Esses campos já entram limpos, porque a conversão acontece no construtor.

Musica e Album existem porque respondem duas perguntas de jeitos diferentes: duracao_total() e execucoes(). Na música a duração é o campo duracao_seg. No álbum é a soma das faixas, pulando as que vêm com duração nula. E música tem contagem de execuções, álbum não tem.

Como cada uma sabe responder por conta própria, a Catalogo não precisa perguntar o tipo do conteúdo. Não existe nenhum if tipo == "musica" dentro dela. O tipo é decidido uma vez só, na carga, pela função criar_conteudo().

### Usuario

Guarda o nome e a playlist, e tem o método item_na_posicao(). Ela existe porque a ordem importa e a posição precisa ser conferida antes de indexar. Se usasse playlist[posicao] direto, uma posição negativa devolveria o último item em vez de None.

### Por que Faixa não virou classe

A faixa só é lida quando o álbum soma a própria duração, e não faz mais nada além disso. Uma classe só para guardar numero, titulo e duracao_seg seria desnecessario.
