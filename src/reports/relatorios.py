from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        with open("sql/relatorio_treinos_por_aluno.sql") as f:
            self.query_relatorio_treinos_por_aluno = f.read()

        with open("sql/relatorio_treinos_com_instrutores.sql") as f:
            self.query_relatorio_treinos_com_instrutores = f.read()


    def get_relatorio_treinos_por_aluno(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_treinos_por_aluno))
        input("Pressione Enter para Sair do Relatório de Treinos por Aluno")

    def get_relatorio_treinos_com_instrutores(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_treinos_com_instrutores))
        input("Pressione Enter para Sair do Relatório de Treinos com Instrutores")
