"""Testes do terminal e da preservação do CSV, usando dados fictícios."""

import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJETO = Path(__file__).resolve().parents[1]
CABECALHO = 'data,antecedente,comportamento,consequencia,frequencia,duracao\n'
REGISTRO = '01/09/2026,tarefa,pedir ajuda,orientacao,2,1.5\n'
NOVO_REGISTRO = '1\n02/09/2026\njogo\naguardar\ninicio do jogo\n3\n2.5\n4\n'


class TestComportaData(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.pasta = Path(self.temporario.name)
        self.script = self.pasta / 'main.py'
        shutil.copyfile(PROJETO / 'main.py', self.script)
        self.csv = self.pasta / 'registros.csv'

    def executar(self, entrada):
        return subprocess.run(
            [sys.executable, str(self.script)], input=entrada,
            text=True, capture_output=True, cwd=self.pasta, timeout=5,
        )

    def test_carrega_csv_e_analisa_valores_numericos(self):
        self.csv.write_text(CABECALHO + REGISTRO, encoding='utf-8')
        resultado = self.executar('2\n3\n4\n')
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn('pedir ajuda', resultado.stdout)
        self.assertIn('Frequência total: 2', resultado.stdout)
        self.assertIn('Duração média: 1.5', resultado.stdout)

    def test_novo_registro_preserva_csv_ao_reabrir(self):
        self.csv.write_text(CABECALHO + REGISTRO, encoding='utf-8')
        resultado = self.executar(NOVO_REGISTRO)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        with self.csv.open(encoding='utf-8', newline='') as arquivo:
            registros = list(csv.DictReader(arquivo))
        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0]['comportamento'], 'pedir ajuda')
        self.assertEqual(registros[1]['comportamento'], 'aguardar')
        reabertura = self.executar('3\n4\n')
        self.assertEqual(reabertura.returncode, 0, reabertura.stderr)
        self.assertIn('Frequência total: 5', reabertura.stdout)
        self.assertIn('Duração média: 2.0', reabertura.stdout)

    def test_analise_vazia_nao_encerra_programa(self):
        resultado = self.executar('3\n4\n')
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn('Não existem dados suficientes', resultado.stdout)
        self.assertIn('Encerrando o programa', resultado.stdout)

    def test_csv_invalido_impede_gravacao(self):
        for conteudo in [
            'coluna_incorreta\nvalor\n',
            CABECALHO + '01/09/2026,tarefa,pedir ajuda,orientacao,abc,1.5\n',
            CABECALHO + '01/09/2026,tarefa,pedir ajuda,orientacao,2,nan\n',
        ]:
            with self.subTest(conteudo=conteudo):
                self.csv.write_text(conteudo, encoding='utf-8')
                resultado = self.executar(NOVO_REGISTRO)
                self.assertNotEqual(resultado.returncode, 0)
                self.assertEqual(self.csv.read_text(encoding='utf-8'), conteudo)
                self.assertNotIn('Traceback', resultado.stderr)

    def test_carrega_csv_com_bom(self):
        self.csv.write_text(CABECALHO + REGISTRO, encoding='utf-8-sig')
        resultado = self.executar('3\n4\n')
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn('Frequência total: 2', resultado.stdout)

    def test_primeiro_cadastro_cria_csv(self):
        resultado = self.executar(NOVO_REGISTRO)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        with self.csv.open(encoding='utf-8', newline='') as arquivo:
            registros = list(csv.DictReader(arquivo))
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]['frequencia'], '3')

    def test_csv_so_com_cabecalho_permite_analise_vazia(self):
        self.csv.write_text(CABECALHO, encoding='utf-8')
        resultado = self.executar('3\n4\n')
        self.assertEqual(resultado.returncode, 0, resultado.stderr)


if __name__ == '__main__':
    unittest.main()
