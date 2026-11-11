# Catálogo de músicas DynamoDB — especificação

> **DYN-DOC** · versão 1.0.0 · 11/11/2026 · código `06ee79293492067989f546584654844e11cd4281` · análise estática; execução em DynamoDB não comprovada.

## Problema e limite
Laboratório de acesso a dados NoSQL que cadastra, consulta, lista e exclui músicas. O código usa a API `boto3.resource('dynamodb')`, com DynamoDB Local como destino padrão; acessar AWS real exige a opção explícita `--aws`. O exercício preserva exemplos em `src/itemmusic.json`, `src/batchmusic.json` e `src/keyconditions.json`.

## Modelo físico e chaves
A tabela é `Music` por padrão. Chave particionada `Artist` (HASH) e chave de classificação `SongTitle` (RANGE), ambas `S`. O atributo adicional `AlbumTitle` não participa da identidade. O comando `criar-tabela` usa `BillingMode='PAY_PER_REQUEST'`, inclusive quando o usuário opta por AWS real, o que pode gerar custos.

## Operações e contratos do código
| Operação CLI | Método adaptador | Protocolo boto3 | Retorno |
|---|---|---|---|
| `cadastrar --artista --titulo [--album]` | `RepositorioMusicas.cadastrar` | `put_item` | Objeto com Artist/SongTitle/AlbumTitle |
| `consultar --artista --titulo` | `consultar` | `get_item` | Item ou `None` |
| `excluir --artista --titulo` | `excluir` | `delete_item` | CLI imprime `excluido: true` sem confirmar existência anterior |
| `listar --limite` | `listar_pagina` | `scan` | itens + próxima chave de continuação |
| `criar-tabela` | recurso DynamoDB | `list_tables/create_table` | Nome da tabela |

`RepositorioMusicas.validar` exige artista e título não vazios após `strip`, limitados a 120 e 200 caracteres respectivamente. O scan aceita limite entre 1 e 100 e usa `ExclusiveStartKey` quando fornecida. A CLI expõe `--limite`, mas **não expõe ainda opção para retomar uma página pela chave**.

## Preparação local
```bash
python -m pip install -r requirements.txt
# inicie DynamoDB Local separadamente na porta 8000
python principal.py criar-tabela
python principal.py cadastrar --artista "Elis Regina" --titulo "Exemplo" --album "Disco"
python principal.py consultar --artista "Elis Regina" --titulo "Exemplo"
python -m unittest discover -s tests -v
```

## Decisões e riscos
- Um `put_item` sem `ConditionExpression` pode sobrescrever item existente. Exigir política explícita antes de produção.
- `scan` percorre a tabela e tem custo crescente; para consultas por artista avaliar `query` e índices apropriados.
- O fluxo não usa transações; exclusão idempotente significa resposta de sucesso mesmo se o registro não existia.
- `boto3` usa credenciais locais fictícias exclusivamente para DynamoDB Local; nunca versionar chaves AWS reais.
- Sem CI de integração real nem LocalStack/DynamoDB Local validado nesta revisão.
