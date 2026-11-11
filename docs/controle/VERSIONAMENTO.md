# Versionamento dos documentos DynamoDB

**DYN-DOC v1.0.0**, 11/11/2026. Código analisado: `06ee79293492067989f546584654844e11cd4281`.

| Arquivo | Versão | Justificativa |
|---|---|---|
| [Projeto](../projeto/ESPECIFICACAO.md) | 1.0.0 | Chave composta e CRUD boto3 |
| [UML](../uml/README.md) | 1.0.0 | Modelo da tabela, componentes e paginação |
| [Testes](../testes/PLANO_DE_TESTES.md) | 1.0.0 | Suíte fake e integração pendente |

Política: **MAJOR** para mudança da chave ou contrato, **MINOR** para novos comandos/atributos, **PATCH** para correção documental. Cada versão precisa apontar SHA e evidências do ambiente, diferenciando unitário, DynamoDB Local e AWS real.
