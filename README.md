# Laboratório DynamoDB — catálogo de músicas

Projeto de aprendizado inspirado no desafio DynamoDB da DIO. Inclui comandos AWS CLI originais e, adicionalmente, **CLI Python com operações de cadastro, consulta, listagem e exclusão**.

## Executar localmente

Requer Python 3.10+, Java/DynamoDB Local (ou container equivalente) e boto3.

```bash
python -m pip install -r requirements.txt
python principal.py criar-tabela
python principal.py cadastrar --artista "Elis" --titulo "Exemplo" --album "Disco"
python principal.py consultar --artista "Elis" --titulo "Exemplo"
python principal.py listar --limite 20
python principal.py excluir --artista "Elis" --titulo "Exemplo"
```

Por padrão os comandos utilizam `http://localhost:8000` com credenciais fictícias locais. **Somente `--aws` conecta à AWS real**, podendo gerar custos. A configuração e a tabela precisam existir para operações de negócio.

## Sem exclusão falsa

O comando `excluir` usa `DeleteItem(ReturnValues='ALL_OLD')` e apresenta `{"excluido": true}` **apenas quando havia um registro**. Excluir uma chave inexistente retorna `false`. O laboratório também valida tipos e limites de artista, título e álbum.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes utilizam uma tabela simulada: a integração real com DynamoDB Local/AWS é uma etapa separada.

## Arquitetura

- `principal.py`: CLI.
- `aplicacao/repositorio.py`: adaptação boto3 com validação.
- `tests/test_musicas.py`: testes de comportamento.
- `docs/REQUISITOS.md`, `docs/ARQUITETURA.md`, `docs/UML.puml`, `docs/PLANO_TESTES.md`: documentação.
- `AGENTS.md`: contexto para ferramentas de IA.

---

## Material original do desafio

## Referência do desafio DynamoDB da DIO
Repositório para o live coding do dia 30/09/2021 sobre o Amazon DynamoDB

### Serviço utilizado
  - Amazon DynamoDB
  - Amazon CLI para execução em linha de comando

### Comandos para execução do experimento:


- Criar uma tabela

```
aws dynamodb create-table \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema \
        AttributeName=Artist,KeyType=HASH \
        AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5
```

- Inserir um item

```
aws dynamodb put-item \
    --table-name Music \
    --item file://itemmusic.json \
```

- Inserir múltiplos itens

```
aws dynamodb batch-write-item \
    --request-items file://batchmusic.json
```

- Criar um index global secundário baeado no título do álbum

```
aws dynamodb update-table \
    --table-name Music \
    --attribute-definitions AttributeName=AlbumTitle,AttributeType=S \
    --global-secondary-index-updates \
        "[{\"Create\":{\"IndexName\": \"AlbumTitle-index\",\"KeySchema\":[{\"AttributeName\":\"AlbumTitle\",\"KeyType\":\"HASH\"}], \
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\": 10, \"WriteCapacityUnits\": 5      },\"Projection\":{\"ProjectionType\":\"ALL\"}}}]"
```

- Criar um index global secundário baseado no nome do artista e no título do álbum

```
aws dynamodb update-table \
    --table-name Music \
    --attribute-definitions\
        AttributeName=Artist,AttributeType=S \
        AttributeName=AlbumTitle,AttributeType=S \
    --global-secondary-index-updates \
        "[{\"Create\":{\"IndexName\": \"ArtistAlbumTitle-index\",\"KeySchema\":[{\"AttributeName\":\"Artist\",\"KeyType\":\"HASH\"}, {\"AttributeName\":\"AlbumTitle\",\"KeyType\":\"RANGE\"}], \
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\": 10, \"WriteCapacityUnits\": 5      },\"Projection\":{\"ProjectionType\":\"ALL\"}}}]"
```

- Criar um index global secundário baseado no título da música e no ano

```
aws dynamodb update-table \
    --table-name Music \
    --attribute-definitions\
        AttributeName=SongTitle,AttributeType=S \
        AttributeName=SongYear,AttributeType=S \
    --global-secondary-index-updates \
        "[{\"Create\":{\"IndexName\": \"SongTitleYear-index\",\"KeySchema\":[{\"AttributeName\":\"SongTitle\",\"KeyType\":\"HASH\"}, {\"AttributeName\":\"SongYear\",\"KeyType\":\"RANGE\"}], \
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\": 10, \"WriteCapacityUnits\": 5      },\"Projection\":{\"ProjectionType\":\"ALL\"}}}]"
```

- Pesquisar item por artista

```
aws dynamodb query \
    --table-name Music \
    --key-condition-expression "Artist = :artist" \
    --expression-attribute-values  '{":artist":{"S":"Iron Maiden"}}'
```
- Pesquisar item por artista e título da música

```
aws dynamodb query \
    --table-name Music \
    --key-condition-expression "Artist = :artist and SongTitle = :title" \
    --expression-attribute-values file://keyconditions.json
```

- Pesquisa pelo index secundário baseado no título do álbum

```
aws dynamodb query \
    --table-name Music \
    --index-name AlbumTitle-index \
    --key-condition-expression "AlbumTitle = :name" \
    --expression-attribute-values  '{":name":{"S":"Fear of the Dark"}}'
```

- Pesquisa pelo index secundário baseado no nome do artista e no título do álbum

```
aws dynamodb query \
    --table-name Music \
    --index-name ArtistAlbumTitle-index \
    --key-condition-expression "Artist = :v_artist and AlbumTitle = :v_title" \
    --expression-attribute-values  '{":v_artist":{"S":"Iron Maiden"},":v_title":{"S":"Fear of the Dark"} }'
```

- Pesquisa pelo index secundário baseado no título da música e no ano

```
aws dynamodb query \
    --table-name Music \
    --index-name SongTitleYear-index \
    --key-condition-expression "SongTitle = :v_song and SongYear = :v_year" \
    --expression-attribute-values  '{":v_song":{"S":"Wasting Love"},":v_year":{"S":"1992"} }'
```

## Documentação técnica v1.0.0

- [Especificação e modelo DynamoDB](docs/projeto/ESPECIFICACAO.md)
- [Diagramas UML](docs/uml/README.md)
- [Casos de teste](docs/testes/PLANO_DE_TESTES.md)
- [Controle de versões](docs/controle/VERSIONAMENTO.md)
