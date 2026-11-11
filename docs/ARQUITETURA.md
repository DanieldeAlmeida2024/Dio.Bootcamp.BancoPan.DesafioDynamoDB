# Arquitetura

```mermaid
flowchart LR
  Operador --> CLI["principal.py"]
  CLI --> Repositorio["RepositorioMusicas"]
  Repositorio --> Dynamo[("DynamoDB Local ou AWS")]
```

O adaptador recebe uma tabela compatível com boto3. Testes injetam uma implementação simulada, sem custo ou credencial de nuvem. Por padrão a CLI usa endpoint local; `--aws` altera explicitamente esse comportamento.
