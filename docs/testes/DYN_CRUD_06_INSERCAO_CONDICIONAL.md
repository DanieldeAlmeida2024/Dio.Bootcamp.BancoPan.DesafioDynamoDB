# DYN-CRUD-06 — Proteção contra sobrescrita de músicas

**Data:** 15/11/2026 · **Módulo:** `aplicacao/repositorio.py`

## Risco identificado
`put_item(Item=item)` é um upsert no DynamoDB. O comando CLI `cadastrar` sobrescrevia silenciosamente a linha existente com a mesma chave composta `Artist + SongTitle`, inclusive metadados já gravados.

## Contrato implementado
- `cadastrar` usa a condição atômica `attribute_not_exists(Artist)`, impedindo alterar um item com a chave primária já cadastrada.
- `ConditionalCheckFailedException` vira `ErroValidacao` com mensagem de conflito, em vez de apresentar cadastro bem-sucedido.
- Outros erros do serviço são propagados, sem fingir sucesso.
- Uma mesma faixa de outro artista, ou outro título do mesmo artista, continua permitida.
- A tabela simulada testa que o álbum original permanece intacto quando um cadastro duplicado falha.

## Limites de homologação
A suíte automatizada usa tabela em memória, não o DynamoDB Local real. É necessário validar as condições com a API DynamoDB/boto3 e concorrência antes de uso real. Os exemplos AWS CLI originais são mantidos como material histórico, não passam a ter proteção automaticamente.
