# Guia de desenvolvimento — DynamoDB

Projeto didático. Preserve os exemplos AWS CLI já existentes. O código Python divide CLI e adaptador de persistência.

1. Use `--aws` somente com autorização para consumir serviços faturáveis.
2. Nunca versionar credenciais, segredos ou dados pessoais.
3. Manter validação de Artist e SongTitle antes das chamadas ao SDK.
4. Garantir testes com mocks e validação separada com DynamoDB Local.
5. Executar `python -m unittest discover -s tests -v` antes de afirmar que o código funciona.
