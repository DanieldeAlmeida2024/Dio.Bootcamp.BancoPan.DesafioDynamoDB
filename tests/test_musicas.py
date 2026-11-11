import unittest
from aplicacao.repositorio import RepositorioMusicas, ErroValidacao

class TabelaFalsa:
    def __init__(self): self.dados = {}
    def put_item(self, Item): self.dados[(Item['Artist'], Item['SongTitle'])] = Item
    def get_item(self, Key):
        item = self.dados.get((Key['Artist'], Key['SongTitle']))
        return {'Item': item} if item else {}
    def delete_item(self, Key): self.dados.pop((Key['Artist'], Key['SongTitle']), None)
    def scan(self, Limit, **kwargs): return {'Items': list(self.dados.values())[:Limit]}

class TestesMusicas(unittest.TestCase):
    def setUp(self): self.repo = RepositorioMusicas(TabelaFalsa())
    def test_crud(self):
        self.repo.cadastrar('Elis', 'Exemplo', 'Disco')
        self.assertEqual('Disco', self.repo.consultar('Elis', 'Exemplo')['AlbumTitle'])
        self.assertEqual(1, len(self.repo.listar_pagina()['itens']))
        self.repo.excluir('Elis', 'Exemplo')
        self.assertIsNone(self.repo.consultar('Elis', 'Exemplo'))
    def test_chaves_invalidas(self):
        with self.assertRaises(ErroValidacao): self.repo.cadastrar(' ', 'Exemplo')
    def test_paginacao(self):
        with self.assertRaises(ErroValidacao): self.repo.listar_pagina(999)
