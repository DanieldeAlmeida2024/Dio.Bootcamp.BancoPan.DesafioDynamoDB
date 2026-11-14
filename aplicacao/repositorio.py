"""Adaptador para boto3; regras básicas de validação independem do SDK."""
class ErroValidacao(ValueError):
    pass

class RepositorioMusicas:
    def __init__(self, tabela): self.tabela = tabela

    @staticmethod
    def validar(artista, titulo):
        if not isinstance(artista, str) or not isinstance(titulo, str):
            raise ErroValidacao('Artista e título devem ser textos.')
        artista, titulo = artista.strip(), titulo.strip()
        if not artista or not titulo:
            raise ErroValidacao('Artista e título são obrigatórios.')
        if len(artista) > 120 or len(titulo) > 200:
            raise ErroValidacao('Artista ou título excede o limite.')
        return artista, titulo

    def cadastrar(self, artista, titulo, album=''):
        artista, titulo = self.validar(artista, titulo)
        if not isinstance(album, str) or len(album.strip()) > 200:
            raise ErroValidacao('Álbum deve ser texto com até 200 caracteres.')
        item = {'Artist': artista, 'SongTitle': titulo, 'AlbumTitle': album.strip()}
        self.tabela.put_item(Item=item)
        return item

    def consultar(self, artista, titulo):
        artista, titulo = self.validar(artista, titulo)
        return self.tabela.get_item(Key={'Artist': artista, 'SongTitle': titulo}).get('Item')

    def excluir(self, artista, titulo):
        artista, titulo = self.validar(artista, titulo)
        resposta = self.tabela.delete_item(
            Key={'Artist': artista, 'SongTitle': titulo}, ReturnValues='ALL_OLD'
        )
        return bool(resposta.get('Attributes'))

    def listar_pagina(self, limite=20, chave_continuacao=None):
        if type(limite) is not int or not 1 <= limite <= 100:
            raise ErroValidacao('Limite deve ser de 1 a 100.')
        argumentos = {'Limit': limite}
        if chave_continuacao:
            argumentos['ExclusiveStartKey'] = chave_continuacao
        pagina = self.tabela.scan(**argumentos)
        return {'itens': pagina.get('Items', []), 'proxima_chave': pagina.get('LastEvaluatedKey')}
