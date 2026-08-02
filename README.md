# Mini-Projeto TrilhaSonora

> **Entrega: sexta-feira, 07/08/2026.**
> Link do repositório no formulário de entrega da aula 09:
> **<https://www.otrilha.com/aulas/09>**. Só o link, nada de zip, nada de email.

Vocês vão construir um analisador do catálogo da **TrilhaSonora**, uma
plataforma fictícia de streaming musical. O resultado é um produto de verdade:
uma classe que modela o catálogo, um menu interativo no terminal e um modo
batch que responde 10 mil consultas de uma vez.

---

## Boas-vindas

O catálogo que vocês vão receber tem músicas e álbuns reais: Taylor Swift,
BTS, Sade, Deftones, Charlie Brown Jr. e vários outros. Os 33 usuários do
catálogo são pessoas da organização do Trilha, e algumas playlists foram
plantadas com gosto bem característico. Quando vocês cruzarem o nome com a
playlist, vão reconhecer.

Uma coisa importante antes de começar: **o dado vem sujo. É de propósito.**
A vida real é assim. Nenhuma das esquisitices que vocês encontrarem é bug
nosso: cada uma está ali para forçar uma técnica específica.

Se travar, pergunta. É pra isso que a gente existe.

---

## Como começar

Este repositório é o ponto de partida. **Deem fork**, e trabalhem no fork
de vocês:

1. Clique em **Fork** aqui no GitHub (canto superior direito).
2. Clone o *seu* fork:
   ```bash
   git clone https://github.com/<seu-usuario>/trilhasonora-miniprojeto.git
   cd trilhasonora-miniprojeto
   ```
3. Confira que o Python é 3.10 ou mais novo:
   ```bash
   python3 --version
   ```
4. Comecem a preencher os arquivos `catalogo.py`, `main.py` e `cli.py`,
   que já vieram aqui como esqueletos vazios.

Não precisa instalar nada. **Zero dependências externas**: tudo que o
projeto usa está na biblioteca padrão do Python. Se vocês precisarem de
`pip install` alguma coisa, provavelmente pegaram um caminho mais difícil
do que o necessário.

Commitem ao longo do caminho. Um repositório com um único commit
"projeto pronto" na véspera conta contra vocês no critério de qualidade.

---

## O que vocês vão entregar

Na raiz do fork de vocês, estes cinco arquivos:

| Arquivo | O que é |
|---|---|
| `catalogo.py` | A classe `Catalogo` (mais as classes auxiliares que vocês decidirem criar) |
| `main.py` | Modo batch: lê o workload de consultas e grava as respostas |
| `cli.py` | O menu interativo no terminal |
| `respostas.json` | Gerado pela solução de vocês ao rodar o `main.py` |
| `README.md` | Substituam este arquivo por uma página curta justificando suas decisões de modelagem |

Os três primeiros já estão aqui como esqueletos. O `respostas.json` vocês
geram. O `README.md` vocês reescrevem.

---

## O catálogo

Vocês recebem dois arquivos JSON com o mesmo schema:

- **`catalogo_dev.json`**: 60 conteúdos. É por onde vocês começam: dá pra
  abrir e ler com os olhos.
- **`catalogo_final.json`**: 20 mil conteúdos. É o da correção.

Os 60 do dev são exatamente os 60 primeiros do final, então o que funciona
num funciona no outro.

Cada conteúdo é uma `musica` ou um `album`:

```json
{
  "plataforma": "TrilhaSonora",
  "meta": { "seed": 2026, "total_conteudos": 60, "total_usuarios": 33 },
  "conteudos": [
    {
      "id": "t000002",
      "tipo": "musica",
      "titulo": "Cruel Summer",
      "artista": "Taylor Swift",
      "ano": 2019,
      "generos": ["Pop"],
      "plataformas": ["Spotify", "Apple Music"],
      "data_adicionado": "2023-04-08",
      "rating": 9.2,
      "duracao_seg": 257,
      "engajamento": { "execucoes": 197125335, "curtidas": 656016 }
    },
    {
      "id": "t000009",
      "tipo": "album",
      "titulo": "Diamond Life",
      "artista": "Sade",
      "ano": 1984,
      "generos": ["Smooth Jazz", "Soul"],
      "plataformas": ["Spotify", "Tidal"],
      "data_adicionado": "27/07/2023",
      "rating": "8.5",
      "faixas": [
        { "numero": 1, "titulo": "Your Love Is King", "duracao_seg": 231 },
        { "numero": 2, "titulo": "Hang On to Your Love", "duracao_seg": null }
      ]
    }
  ],
  "usuarios": [
    { "id": "u01", "nome": "Ayres", "playlist": ["t000009", "t000022"] }
  ]
}
```

As diferenças entre os dois tipos:

- **`musica`** tem `duracao_seg` (inteiro) e `engajamento` (com `execucoes` e `curtidas`).
- **`album`** tem `faixas` (lista de objetos com `numero`, `titulo` e `duracao_seg`).

E `usuarios` é uma lista à parte: cada um tem `id`, `nome` e uma `playlist`,
que é uma lista de ids de conteúdo, e **a ordem da playlist importa**.

### As 7 sujeiras intencionais

| Sujeira | Frequência | O que ela força vocês a aprender |
|---|---|---|
| `rating` ausente (a chave nem existe no objeto) | 5% | Checar presença antes de acessar (`in`, `.get()`) |
| `rating` como string `"8.3"` em vez de número | 3% | Conversão de tipos |
| `data_adicionado` em 2 formatos (`2020-07-24` e `24/07/2020`) | 50/50 | Condicional + parsing de string |
| `generos` como string solta, não lista | 15% | Checagem de tipo (`isinstance`) |
| `generos` como lista aninhada (`["Pop", ["Synth-Pop"]]`, até 3 níveis) | 15% | Achatar estrutura recursiva (dá pra fazer com uma pilha) |
| `engajamento.execucoes` como string com vírgula (`"12,500,000"`) | 20% | Limpeza de string antes do `int()` |
| Faixa de álbum com `duracao_seg: null` | 4% | Somar defensivamente, pulando os nulos |

Reparem que a lista acima é praticamente um roteiro do que vocês precisam
implementar.

---

## A classe `Catalogo`

O coração do projeto é a classe `Catalogo`, em `catalogo.py`. Ela carrega o
JSON **uma vez** e expõe os métodos que o resto do código consome. Tanto o
`main.py` quanto o `cli.py` usam essa classe, e nada além dela. Se o
`cli.py` estiver abrindo o JSON na mão, tem coisa errada na modelagem.

### A interface obrigatória

A classe precisa ter exatamente estes **16 métodos**, com exatamente estas
assinaturas. Os nomes dos parâmetros importam (o `consultas.json` usa esses
mesmos nomes, veja a seção *Modo batch*):

```python
class Catalogo:
    def __init__(self, caminho_json: str): ...

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]: ...
    def buscar_usuario_por_nome(self, nome: str) -> str | None: ...
    def playlist_de(self, usuario_id: str) -> list[str] | None: ...
    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: ...
    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: ...

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool: ...
    def proximo(self) -> str | None: ...
    def fila_atual(self) -> list[str]: ...
```

Podem criar quantos métodos auxiliares quiserem além desses. O que não pode
é faltar um dos 16, ou trocar o nome de um parâmetro.

### A fila de reprodução

Os três últimos métodos são uma **fila de reprodução**, igual à "fila" do
Spotify ou do Apple Music, e diferente da playlist. A `Catalogo` mantém
**uma fila por instância**, que começa vazia no `__init__`.

- **`enfileirar(conteudo_id)`**: adiciona o conteúdo **no final** da fila.
  Se o id não existe no catálogo, **não** enfileira e retorna `False`.
  Se enfileirou, retorna `True`. Pode enfileirar o mesmo id várias vezes
  (uma música pode estar duas vezes na fila).
- **`proximo()`**: remove e retorna o **primeiro** id da fila (FIFO,
  o primeiro que entrou é o primeiro que sai). Fila vazia → `None`.
- **`fila_atual()`**: retorna uma **cópia** da fila como `list`, na ordem
  FIFO (a frente primeiro). Fila vazia → `[]`.

Pensem na estrutura de dados certa aqui. `list.pop(0)` funciona, mas remove
do início de uma lista é O(n). A `collections.deque` da biblioteca padrão
é O(1) nas duas pontas e é o jeito idiomático de fazer fila em Python.

**Atenção ao estado:** a fila é a única parte do `Catalogo` que muda depois
do `__init__`. O batch processa as 10 mil consultas **em ordem**, e cada
`enfileirar` e cada `proximo` mexem no estado que as próximas consultas vão
observar. Se vocês processarem as consultas fora de ordem, as respostas de
fila saem todas erradas. A fila **não** é persistida entre execuções: toda
vez que o `main.py` roda, parte da fila vazia.

### O resto da modelagem é decisão de vocês

Criar `Musica`, `Album`, `Usuario`, `Faixa`: escolham o que faz sentido.
Mas atenção: **cada classe que vocês criarem precisa justificar a própria
existência.** No `README.md` do repositório, escrevam 1 a 2 linhas por classe
explicando por que ela existe e não é só um dicionário. A frase precisa ser
do tipo "essa classe agrupa estado e comportamento que pertencem juntos
porque...". Não vale "criei porque POO".

Se vocês criarem uma classe que só guarda dados e nunca faz nada, ela não
justifica. Se ela tem métodos que só fazem sentido para aquele tipo de dado,
ela justifica.

---

## O CLI interativo

```bash
python3 cli.py catalogo_final.json
```

O CLI é onde o projeto vira produto: é a interface pela qual uma pessoa
responde **todas** as perguntas sobre o catálogo, sem escrever código.
Ele abre um menu que fica rodando até a pessoa digitar `0`:

```
TrilhaSonora
============
1. Listar todos os usuários
2. Ver playlist completa de um usuário
3. Conteúdo na posição N da playlist
4. Interseção de playlists (N usuários)
5. Dados de um conteúdo (rating, duração, gêneros, plataformas, data, execuções)
6. Conteúdos de um gênero
7. Enfileirar conteúdo na fila de reprodução
8. Tocar próximo da fila
9. Ver fila atual
0. Sair
>
```

### O que cada opção precisa usar

Toda opção do menu é uma casca fina em volta de um ou mais métodos da
`Catalogo`. Não pode ter lógica de negócio dentro do `cli.py`. Se vocês
estiverem achatando gênero ou convertendo data dentro do CLI, essa lógica
está no arquivo errado.

| Opção | Método(s) da `Catalogo` que ela usa |
|---|---|
| 1 | `listar_usuarios()` |
| 2 | `buscar_usuario_por_nome(nome)` → `playlist_de(usuario_id)` |
| 3 | `buscar_usuario_por_nome(nome)` → `conteudo_na_posicao(usuario_id, posicao)` |
| 4 | `buscar_usuario_por_nome(nome)` para cada nome → `intersecao_playlists(usuario_ids)` |
| 5 | `rating_de`, `duracao_total_de`, `generos_de`, `plataformas_de`, `data_adicionado_de` e (só se for música) `execucoes_de` |
| 6 | `conteudos_do_genero(genero)` |
| 7 | `enfileirar(conteudo_id)` |
| 8 | `proximo()` |
| 9 | `fila_atual()` |

Três detalhes que fazem diferença na usabilidade:

**As opções 2, 3 e 4 pedem o _nome_ do usuário, não o id.** Ninguém decora
`u17`. A pessoa digita "Nicholas", e o CLI converte para o id internamente
com `buscar_usuario_por_nome()` antes de chamar os outros métodos. Se o nome
não existir, avise em vez de estourar um erro.

**A posição da opção 3 é 1-based para o humano.** A pessoa digita `1` para
ver o primeiro item da playlist, não `0`. O método `conteudo_na_posicao` em
si continua 0-based, esse é o contrato da `Catalogo` e é o que o
`consultas.json` assume. A conversão `posicao_digitada - 1` mora dentro do
`cli.py`. E antes de pedir a posição, mostre o tamanho da playlist:

```
Playlist de Nicholas tem 14 itens (posições 1 a 14).
Qual posição? > 3
```

Isso economiza chute do usuário.

**Mostrem nome, não id.** Uma playlist impressa como
`['t000009', 't000022', 't000041']` é inútil para qualquer pessoa. Resolvam os ids
para título e artista na hora de exibir. Um método auxiliar na `Catalogo`
que devolve `"Diamond Life, de Sade (álbum)"` a partir do id resolve isso e
serve várias opções do menu.

Podem usar `print` e `input` normalmente, sem framework externo. O menu
não pode quebrar se a pessoa digitar besteira: uma letra onde se espera
número, um id que não existe, um enter vazio. Trate isso.

### Opcional: histórico das últimas consultas

Se quiserem ir além do mínimo, adicionem um item `10. Ver histórico` que
mostra **as últimas 10 consultas** feitas no CLI (qualquer opção, com os
parâmetros que a pessoa digitou). A estrutura indicada é
`collections.deque(maxlen=10)`, uma fila com limite de tamanho que descarta
sozinha as entradas mais antigas, sem vocês escreverem uma linha de lógica
para isso.

Esse item é opcional e não entra no piso obrigatório, mas conta no critério
de qualidade.

---

## Modo batch

```bash
python3 main.py consultas.json respostas.json
```

Lê o arquivo de consultas, responde todas **na ordem em que aparecem**, e
grava o resultado.

Reparem que o `main.py` recebe dois caminhos, e nenhum deles é o do catálogo.
Isso é de propósito: **o batch carrega sempre o `catalogo_final.json`**, os
20 mil. O `consultas.json` foi gerado em cima dele, então rodar o batch no
`catalogo_dev.json` faz praticamente toda resposta sair errada. Use o dev
para desenvolver a `Catalogo` e para brincar no CLI, mas o `respostas.json`
que vocês entregam sai do final.

Formato do `consultas.json` que vocês recebem:

```json
{
  "consultas": [
    {"id": 1, "tipo": "rating_de", "parametros": {"conteudo_id": "t000007"}},
    {"id": 2, "tipo": "intersecao_playlists", "parametros": {"usuario_ids": ["u01", "u05"]}},
    {"id": 3, "tipo": "conteudo_na_posicao", "parametros": {"usuario_id": "u03", "posicao": 2}},
    {"id": 4, "tipo": "enfileirar", "parametros": {"conteudo_id": "t000002"}},
    {"id": 5, "tipo": "proximo", "parametros": {}},
    {"id": 6, "tipo": "fila_atual", "parametros": {}}
  ]
}
```

Formato do `respostas.json` que vocês geram. As chaves são os ids das
consultas, **como string**:

```json
{
  "1": 9.4,
  "2": ["t000003", "t000041"],
  "3": "t000018",
  "4": true,
  "5": "t000002",
  "6": []
}
```

Os 15 `tipo`s possíveis são exatamente os 15 métodos da `Catalogo` que
retornam valor (todos menos o `__init__`). O mapeamento é direto: o tipo
`"rating_de"` chama `catalogo.rating_de(...)`, e assim por diante.

**As chaves de `parametros` são exatamente os nomes dos parâmetros dos
métodos.** Isso não é coincidência: é para que vocês possam despachar sem
escrever quinze `if`. Vale a pena descobrir o que `getattr` e `**` fazem
antes de escrever o décimo `elif`.

---

## Regras canônicas

Estas 17 regras são o contrato do projeto. São elas que decidem se uma
resposta está certa. Se bater dúvida sobre um caso de borda, a resposta
está aqui:

```
1.  id de conteúdo inexistente -> null em qualquer consulta de conteúdo
2.  usuario_id inexistente -> null (playlist_de, conteudo_na_posicao)
                           -> []   (intersecao_playlists)
3.  listar_usuarios: TODOS os nomes em ordem alfabética (sorted padrão
                     do Python); sem parâmetros
4.  buscar_usuario_por_nome: case-insensitive ("NiCHoLas" == "Nicholas");
                             nome inexistente -> null
5.  rating_de:        ausente -> null; string -> converter para float
6.  duracao_total_de: musica -> duracao_seg
                      album  -> soma das faixas, ignorando as de duracao_seg null
7.  generos_de: achatar qualquer estrutura (string, lista, aninhada);
                devolver em ordem alfabética
8.  conteudos_do_genero e plataformas_de: ordem alfabética;
                                          sem resultados -> []
9.  conteudos_do_genero: comparação exata, sensível a maiúscula/minúscula
10. playlist_de: na ordem original da playlist (NÃO alfabética)
11. conteudo_na_posicao: 0-based; posição fora do intervalo -> null
12. intersecao_playlists: ordem alfabética; se algum usuario_id não
                          existe -> []
13. data_adicionado_de: sempre no formato ISO YYYY-MM-DD
                        (converter o DD/MM/YYYY quando vier assim)
14. execucoes_de: retornar int (converter "12,500,000" -> 12500000);
                  só é consultado em ids de música
15. enfileirar: id inexistente -> não enfileira, retorna false
                id existente   -> enfileira no fim, retorna true
16. proximo:    fila vazia -> null; senão remove e retorna o primeiro (FIFO)
    fila_atual: cópia da fila como list, ordem FIFO; vazia -> []
                (começa vazia no __init__, não persiste entre execuções)
17. respostas.json: chaves como string; floats comparados com tolerância 1e-6
```

---

## O `__init__` é onde mora a decisão

Reparem no tamanho dos dois catálogos: o `catalogo_dev.json` tem 60
conteúdos, o `catalogo_final.json` tem 20 mil. E o `consultas.json` tem
10 mil consultas. Multipliquem essas duas coisas antes de escrever a
primeira linha do `main.py`.

Procurar um id percorrendo a lista de 20 mil conteúdos funciona. Fazer isso
10 mil vezes é outra conversa. Um dicionário `{id: conteudo}` construído
**uma vez** no `__init__` transforma essa busca inteira num acesso direto,
e é por isso que o `__init__` recebe o caminho do JSON: ele carrega e
prepara, os outros métodos só consultam.

Pensem em quais dicionários cada um dos 16 métodos precisaria para responder
sem varrer nada. Alguns pedem mais de um índice. Um deles não dá para
indexar de jeito nenhum: descubram qual, e por quê.

---

## Autoverificação (escrita por vocês)

Vocês não precisam esperar a correção para saber se acertaram. No repositório
vem o `gabarito_publico.json`: as respostas **corretas** das 20 primeiras
consultas do `consultas.json`. O formato é o mesmo do `respostas.json` que
vocês vão gerar, id da consulta como chave:

```json
{
  "1": 9.4,
  "2": ["t000003", "t000041"],
  "3": null
}
```

O que a gente **não** entrega é o programa que compara os dois arquivos.
Esse é de vocês. Escrevam um `conferir.py` que abre o `gabarito_publico.json`
e o `respostas.json` de vocês, compara chave por chave e diz quantas bateram
e quais não bateram.

Não é trabalho perdido nem enfeite: é o jeito de vocês pararem de conferir
resposta no olho. Cada vez que mudarem a `Catalogo`, rodar esse script leva
um segundo e responde se vocês quebraram alguma coisa. Sem ele, cada mudança
vira uma rodada de desconfiança.

Duas armadilhas na comparação, que valem para qualquer conferidor de dados:

- **Float não se compara com `==`.** `0.1 + 0.2` não é `0.3` em Python
  (testem no terminal, é real). Comparem a diferença absoluta contra uma
  tolerância pequena, tipo `abs(a - b) < 1e-6`.
- **Resposta ausente não é resposta errada.** Se um id do gabarito nem
  aparece no `respostas.json` de vocês, isso é um bug diferente de ter
  respondido o valor errado. Vale distinguir os dois na saída.

As 20 consultas públicas cobrem vários tipos e alguns casos de borda. Se as
20 baterem, a confiança é alta. Podem commitar o `conferir.py` no repositório:
ele conta a favor de vocês no critério de qualidade.

---

## Antes de entregar

Façam o caminho inteiro numa **cópia limpa** do repositório: clonem o fork de
vocês numa pasta nova, rodem o `main.py` do zero e passem o conferidor de
vocês no `respostas.json` que sair dali.

É o teste mais barato que existe e pega 90% dos problemas de entrega,
principalmente o clássico "funciona na minha pasta porque tem um arquivo que
eu esqueci de commitar".

---

## Como vamos avaliar

A avaliação tem duas dimensões.

### As respostas (piso obrigatório)

O `respostas.json` de vocês precisa estar certo. Esse é o piso: sem isso, o
projeto não está completo, por mais bonito que esteja o código.

Não tem ambiguidade para negociar aqui, porque as 17 regras canônicas estão
todas escritas acima. Toda decisão de caso de borda já foi tomada e está
documentada: o que fazer com id inexistente, com rating ausente, com data no
formato errado, com fila vazia. Se a resposta de vocês difere, é porque uma
das 17 não foi seguida.

### Qualidade (o que eu vou ler)

Eu (João) leio todo o código de vocês. Não é automático, é leitura humana.
Vou olhar quatro coisas:

**Nomes.** `x`, `lista` e `temp` são nomes ruins. `usuario`,
`total_segundos` e `conteudo_atual` são nomes bons. Um nome bom diz o que a
coisa é sem precisar de um comentário ao lado explicando.

**Funções pequenas.** Uma função de 80 linhas que chama outra de 60
geralmente quer dizer que dá para quebrar em partes menores com propósito
único. Cada função deve fazer uma coisa, e o nome dela deve descrever essa
coisa.

**Modelagem.** Cada classe que vocês criarem precisa fazer algo que um
dicionário não faria. Se a justificativa no README for fraca, a classe não
justifica a existência dela.

**Tratamento defensivo na dose certa.** `.get()` onde faz sentido é bom.
`try/except Exception` envolvendo blocos inteiros para "garantir que
funciona" é sinal de que o código não entende o dado que está tratando.
Tratamento defensivo deve ser cirúrgico, não genérico: vocês sabem
exatamente quais são as 7 sujeiras, então tratem essas 7.

Vocês recebem feedback escrito individual depois da correção.

---

## Como entregar

1. Confiram que a raiz do fork tem `catalogo.py`, `main.py`, `cli.py`,
   `respostas.json` e o `README.md` de vocês.
2. Façam o teste da cópia limpa da seção *Antes de entregar* uma última vez.
3. `git push` para o fork de vocês.
4. Mandem **o link do repositório** no formulário de entrega da aula 09:
   <https://www.otrilha.com/aulas/09>

**Prazo: sexta-feira, 07/08/2026.** Se o repositório de vocês for privado,
não esqueçam de nos dar acesso. 

---

## Fechamento

Vocês têm tudo que precisam para construir isso. Comecem pelo
`catalogo_dev.json`, 60 conteúdos, dá para ler com os olhos. Entendam o
que tem dentro, façam funcionar ali, e só depois liguem no
`catalogo_final.json`. Se em algum momento a coisa parecer pesada demais,
voltem no `__init__`: quase sempre a resposta está lá.

Boa construção. Qualquer dúvida, chama a gente.
