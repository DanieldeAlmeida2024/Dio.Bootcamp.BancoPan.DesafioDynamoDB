"""Adaptador para boto3; regras básicas de validação independem do SDK."""
class ErroValidacao(ValueError):
    pass

class RepositorioMusicas:
    def __init__(self, tabela): self.tabela = tabela

    @staticmethod
    def validar(artista, titulo):
        artista, titulo = artista.strip(), titulo.strip()
        if not artista or not titulo:
            raise ErroValidacao('Artista e título são obrigatórios.')
        if len(artista) > 120 or len(titulo) > 200:
            raise ErroValidacao('Artista ou título excede o limite.')
        return artista, titulo

    def cadastrar(self, artista, titulo, album=''):
        artista, titulo = self.validar(artista, titulo)
        item = {'Artist': artista, 'SongTitle': titulo, 'AlbumTitle': album.strip()}
        self.tabela.put_item(Item=item)
        return item

    def consultar(self, artista, titulo):
        artista, titulo = self.validar(artista, titulo)
        return self.tabela.get_item(Key={'Artist': artista, 'SongTitle': titulo}).get('Item')

    def excluir(self, artista, titulo):
        artista, titulo = self.validar(artista, titulo)
        self.tabela.delete_item(Key={'Artist': artista, 'SongTitle': titulo})

    def listar_pagina(self, limite=20, chave_continuacao=None):
        if not 1 <= limite <= 100:
            raise ErroValidacao('Limite deve ser de 1 a 100.')
        argumentos = {'Limit': limite}
        if chave_continuacao:
            argumentos['ExclusiveStartKey'] = chave_continuacao
        pagina = self.tabela.scan(**argumentos)
        return {'itens': pagina.get('Items', []), 'proxima_chave': pagina.get('LastEvaluatedKey')}
