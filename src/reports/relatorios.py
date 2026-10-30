import os

from conexion.oracle_queries import OracleQueries

# Pasta src/sql encontrada a partir deste arquivo, para os relatorios
# funcionarem de qualquer pasta em que o programa for executado
PASTA_SQL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql"
)


def ler_sql(nome_arquivo: str) -> str:
    with open(os.path.join(PASTA_SQL, nome_arquivo), "r", encoding="utf-8") as f:
        return f.read()


class Relatorio:
    def __init__(self):
        self.query_relatorio_treinos_por_aluno = ler_sql("relatorio_treinos_por_aluno.sql")
        self.query_relatorio_treinos_com_instrutores = ler_sql("relatorio_treinos_com_instrutores.sql")

    def exibir(self, titulo: str, query: str):
        oracle = OracleQueries()
        try:
            oracle.connect()
            resultado = oracle.sqlToDataFrame(query)
        finally:
            oracle.close()

        print("\n" + "=" * 70)
        print(titulo.center(70))
        print("=" * 70)
        if resultado.empty:
            print("Nenhum registro encontrado.")
        else:
            print(resultado.to_string(index=False))
        input("\nPressione ENTER para voltar ao menu de relatórios...")

    def get_relatorio_treinos_por_aluno(self):
        self.exibir("QUANTIDADE DE TREINOS POR ALUNO", self.query_relatorio_treinos_por_aluno)

    def get_relatorio_treinos_com_instrutores(self):
        self.exibir("TREINOS COM ALUNOS E INSTRUTORES", self.query_relatorio_treinos_com_instrutores)
