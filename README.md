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

## O que o __init__ prepara

O catálogo final tem 20 mil conteúdos e o batch faz 10 mil consultas. Se cada consulta percorresse a lista inteira para achar um id, daria 200 milhões de comparações. Então o __init__ lê o JSON uma vez e monta quatro dicionários:

- _conteudos: id do conteúdo para o objeto Musica ou Album
- _usuarios: id do usuário para o objeto Usuario
- _id_por_nome_minusculo: nome em minúsculo para o id, que é o que faz a busca por nome ignorar maiúscula
- _ids_por_genero: gênero para a lista de ids daquele gênero, já ordenada

Com esses quatro nenhum método precisa varrer nada, todos viram acesso direto.

A limpeza também acontece na carga e não na consulta. Cada conteúdo já nasce com o rating convertido, a data em ISO, os gêneros achatados e as plataformas ordenadas.

## O método que não dá para indexar

O intersecao_playlists é o único sem índice possível. Os outros respondem sobre uma coisa só, um id ou um nome ou um gênero, então dá para deixar a resposta pronta num dicionário. A interseção depende de uma combinação de usuários, e com 33 usuários passa de 8 bilhões de combinações. Não tem como pré-calcular isso.

O jeito foi usar os índices que já existem. O método pega a playlist de cada usuário no _usuarios, transforma em set e faz a interseção na hora. Como a maior playlist tem 49 itens, sai rápido mesmo sem índice.

## Onde cada sujeira é tratada

- rating ausente e rating em string: converter_rating()
- data nos dois formatos: converter_data()
- gênero como string solta e gênero em lista aninhada: achatar_generos()
- execucoes com vírgula: converter_execucoes()
- faixa com duracao_seg nulo: o duracao_total() do Album pula ela na soma

As quatro primeiras rodam no construtor de Conteudo, então o dado sujo nunca chega nos métodos de consulta.
