"""CLI para DynamoDB Local, com AWS real mediante --aws."""
import argparse
import json
from aplicacao.repositorio import RepositorioMusicas

def criar_recurso(usar_aws, endpoint, regiao):
    try:
        import boto3
    except ImportError as erro:
        raise SystemExit('Instale dependências: pip install -r requirements.txt') from erro
    if usar_aws:
        return boto3.resource('dynamodb', region_name=regiao)
    return boto3.resource('dynamodb', region_name=regiao, endpoint_url=endpoint,
                          aws_access_key_id='local', aws_secret_access_key='local')

def main():
    parser = argparse.ArgumentParser(description='Catálogo de músicas DynamoDB')
    parser.add_argument('--aws', action='store_true', help='Conectar AWS real (sujeito a custos)')
    parser.add_argument('--endpoint', default='http://localhost:8000')
    parser.add_argument('--regiao', default='us-east-1')
    parser.add_argument('--tabela', default='Music')
    sub = parser.add_subparsers(dest='comando', required=True)
    sub.add_parser('criar-tabela')
    add = sub.add_parser('cadastrar'); add.add_argument('--artista', required=True); add.add_argument('--titulo', required=True); add.add_argument('--album', default='')
    buscar = sub.add_parser('consultar'); buscar.add_argument('--artista', required=True); buscar.add_argument('--titulo', required=True)
    excluir = sub.add_parser('excluir'); excluir.add_argument('--artista', required=True); excluir.add_argument('--titulo', required=True)
    listar = sub.add_parser('listar'); listar.add_argument('--limite', type=int, default=20)
    args = parser.parse_args()
    recurso = criar_recurso(args.aws, args.endpoint, args.regiao)
    if args.comando == 'criar-tabela':
        if args.tabela not in recurso.meta.client.list_tables().get('TableNames', []):
            recurso.create_table(TableName=args.tabela, KeySchema=[{'AttributeName': 'Artist', 'KeyType': 'HASH'}, {'AttributeName': 'SongTitle', 'KeyType': 'RANGE'}], AttributeDefinitions=[{'AttributeName': 'Artist', 'AttributeType': 'S'}, {'AttributeName': 'SongTitle', 'AttributeType': 'S'}], BillingMode='PAY_PER_REQUEST')
        print(f'Tabela disponível: {args.tabela}')
        return
    repo = RepositorioMusicas(recurso.Table(args.tabela))
    if args.comando == 'cadastrar': resultado = repo.cadastrar(args.artista, args.titulo, args.album)
    elif args.comando == 'consultar': resultado = repo.consultar(args.artista, args.titulo)
    elif args.comando == 'excluir':
        resultado = {'excluido': repo.excluir(args.artista, args.titulo)}
    else: resultado = repo.listar_pagina(limite=args.limite)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
