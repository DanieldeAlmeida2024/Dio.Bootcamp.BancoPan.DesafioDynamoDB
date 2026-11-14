import unittest
from aplicacao.repositorio import RepositorioMusicas, ErroValidacao

class TabelaFalsa:
    def __init__(self): self.dados = {}
    def put_item(self, Item): self.dados[(Item['Artist'], Item['SongTitle'])] = Item
    def get_item(self, Key):
        item = self.dados.get((Key['Artist'], Key['SongTitle']))
        return {'Item': item} if item else {}
    def delete_item(self, Key, ReturnValues):
        assert ReturnValues == 'ALL_OLD'
        item = self.dados.pop((Key['Artist'], Key['SongTitle']), None)
        return {'Attributes': item} if item else {}
    def scan(self, Limit, **kwargs): return {'Items': list(self.dados.values())[:Limit]}

class TestesMusicas(unittest.TestCase):
    def setUp(self): self.repo = RepositorioMusicas(TabelaFalsa())
    def test_crud(self):
        self.repo.cadastrar('Elis', 'Exemplo', 'Disco')
        self.assertEqual('Disco', self.repo.consultar('Elis', 'Exemplo')['AlbumTitle'])
        self.assertEqual(1, len(self.repo.listar_pagina()['itens']))
        self.assertTrue(self.repo.excluir('Elis', 'Exemplo'))
        self.assertFalse(self.repo.excluir('Elis', 'Exemplo'))
        self.assertIsNone(self.repo.consultar('Elis', 'Exemplo'))
    def test_chaves_invalidas(self):
        with self.assertRaises(ErroValidacao): self.repo.cadastrar(' ', 'Exemplo')
    def test_paginacao(self):
        with self.assertRaises(ErroValidacao): self.repo.listar_pagina(999)

    def test_validacoes_de_tipos_e_limites(self):
        for artista, titulo in [(None, 'Faixa'), (42, 'Faixa'), ('Artista', None)]:
            with self.subTest(artista=artista, titulo=titulo):
                with self.assertRaises(ErroValidacao):
                    self.repo.cadastrar(artista, titulo)
        for album in [None, 'x' * 201]:
            with self.subTest(album=album):
                with self.assertRaises(ErroValidacao):
                    self.repo.cadastrar('Artista', 'Faixa', album)
        for limite in [True, -1, 101, '20']:
            with self.subTest(limite=limite):
                with self.assertRaises(ErroValidacao):
                    self.repo.listar_pagina(limite)
