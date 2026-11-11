# Plano de testes — catálogo DynamoDB

> **DYN-DOC** · versão 1.0.0 · 11/11/2026 · código `06ee79293492067989f546584654844e11cd4281` · análise estática; execução em DynamoDB não comprovada.

## Evidência existente
A suíte `tests/test_musicas.py` usa `TabelaFalsa` que implementa `put_item`, `get_item`, `delete_item` e `scan`. São testes de regras/adaptador **sem serviço DynamoDB**.

| Caso | Situação | Verificação |
|---|---|---|
| DYN-T01 | Automatizado — `test_crud` | Cadastrar, consultar, listar e excluir uma música |
| DYN-T02 | Automatizado — `test_chaves_invalidas` | Artista vazio rejeitado com `ErroValidacao` |
| DYN-T03 | Automatizado — `test_paginacao` | Limite 999 é recusado |
| DYN-T04 | Pendente | Título vazio/200/201 caracteres |
| DYN-T05 | Pendente | Artista de 120 e 121 caracteres |
| DYN-T06 | Pendente | Dois `put_item` com mesma chave: definir sobrescrita/condição |
| DYN-T07 | Pendente | Recuperar segunda página com `LastEvaluatedKey` real |
| DYN-T08 | Pendente | `scan` de tabela vazia |
| DYN-T09 | Pendente | Serviço offline e tratamento de exceção boto3 |
| DYN-T10 | Pendente | Comando AWS real exigindo `--aws` e credenciais válidas |
| DYN-T11 | Pendente | Resiliência à criação da tabela seguida de uso imediato |

## Camadas de execução
1. **Unitário:** `python -m unittest discover -s tests -v`; sem rede.
2. **Integração local:** DynamoDB Local com tabela `Music`, chave composta e operações reais.
3. **Nuvem autorizada:** somente ambiente AWS dedicado, orçamento e política IAM de menor privilégio; não utilizar dados pessoais.

## Critério de liberação
Nenhuma exceção não tratada, identidade de item preservada, paginação documentada e nenhuma operação AWS real sem opção/credencial explícitas. Evidência precisa incluir commit, endpoint, modo local/AWS e resultado.
