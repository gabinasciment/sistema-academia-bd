from datetime import datetime

from conexion.oracle_queries import OracleQueries
from controller.controller_aluno import ControllerAluno
from controller.controller_instrutor import ControllerInstrutor
from model.treino import Treino


class ControllerTreino:
    """Controlador CRUD da tabela TREINO."""

    @staticmethod
    def _escapar(texto):
        if texto is None:
            return ""
        return str(texto).strip().replace("'", "''")

    @staticmethod
    def _validar(nome_treino, objetivo):
        if not nome_treino or not nome_treino.strip():
            raise ValueError("O nome do treino é obrigatório.")
        if not objetivo or not objetivo.strip():
            raise ValueError("O objetivo do treino é obrigatório.")

    @staticmethod
    def _converter_data(data):
        try:
            return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    def inserir(self, id_aluno, id_instrutor, nome_treino, objetivo=""):
        """Cadastra um treino. A data de criação é preenchida pelo Oracle."""
        self._validar(nome_treino, objetivo)

        oracle = OracleQueries(can_write=True)
        try:
            cursor = oracle.connect()

            nome_treino = self._escapar(nome_treino)
            objetivo = self._escapar(objetivo)

            query = f"""
                INSERT INTO TREINO (
                    ID_TREINO,
                    ID_ALUNO,
                    ID_INSTRUTOR,
                    NOME_TREINO,
                    OBJETIVO
                ) VALUES (
                    TREINO_ID_TREINO_SEQ.NEXTVAL,
                    {int(id_aluno)},
                    {int(id_instrutor)},
                    '{nome_treino}',
                    '{objetivo}'
                )
            """

            oracle.write(query)

            # Mesma sessao: CURRVAL devolve o ID que acabou de ser gerado
            cursor.execute("SELECT TREINO_ID_TREINO_SEQ.CURRVAL FROM DUAL")
            return cursor.fetchone()[0]
        finally:
            oracle.close()

    def atualizar(
        self, id_treino, id_aluno, id_instrutor, nome_treino, objetivo=""
    ):
        """Atualiza os dados de um treino existente."""
        self._validar(nome_treino, objetivo)

        oracle = OracleQueries(can_write=True)
        try:
            cursor = oracle.connect()

            nome_treino = self._escapar(nome_treino)
            objetivo = self._escapar(objetivo)

            query = f"""
                UPDATE TREINO
                SET ID_ALUNO = {int(id_aluno)},
                    ID_INSTRUTOR = {int(id_instrutor)},
                    NOME_TREINO = '{nome_treino}',
                    OBJETIVO = '{objetivo}'
                WHERE ID_TREINO = {int(id_treino)}
            """

            oracle.write(query)
            return cursor.rowcount > 0
        finally:
            oracle.close()

    def deletar(self, id_treino):
        """Exclui um treino pelo ID."""
        oracle = OracleQueries(can_write=True)
        try:
            cursor = oracle.connect()

            query = f"""
                DELETE FROM TREINO
                WHERE ID_TREINO = {int(id_treino)}
            """

            oracle.write(query)
            return cursor.rowcount > 0
        finally:
            oracle.close()

    def buscar_por_id(self, id_treino):
        """Busca um treino pelo ID."""
        oracle = OracleQueries()
        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_TREINO, ID_ALUNO, ID_INSTRUTOR,
                       NOME_TREINO, OBJETIVO, DATA_CRIACAO
                FROM TREINO
                WHERE ID_TREINO = {int(id_treino)}
            """

            cursor.execute(query)
            return cursor.fetchone()
        finally:
            oracle.close()

    def listar(self):
        """Lista os treinos com os nomes dos alunos e instrutores."""
        oracle = OracleQueries()
        try:
            cursor = oracle.connect()

            query = """
                SELECT T.ID_TREINO,
                       A.NOME_ALUNO,
                       I.NOME_INSTRUTOR,
                       T.NOME_TREINO,
                       T.OBJETIVO,
                       T.DATA_CRIACAO
                FROM TREINO T
                JOIN ALUNO A ON A.ID_ALUNO = T.ID_ALUNO
                JOIN INSTRUTOR I ON I.ID_INSTRUTOR = T.ID_INSTRUTOR
                ORDER BY T.DATA_CRIACAO DESC
            """

            cursor.execute(query)
            return cursor.fetchall()
        finally:
            oracle.close()

    def obter(self, id_treino):
        """Busca o treino pelo ID e devolve um objeto Treino com os objetos
        Aluno e Instrutor associados (ou None)."""
        linha = self.buscar_por_id(id_treino)
        if not linha:
            return None
        aluno = ControllerAluno().obter(linha[1])
        instrutor = ControllerInstrutor().obter(linha[2])
        return Treino(linha[0], aluno, instrutor, linha[3], linha[4], linha[5])

    def listar_por_aluno(self, id_aluno):
        """Lista os treinos associados a um aluno."""
        oracle = OracleQueries()
        try:
            cursor = oracle.connect()

            query = f"""
                SELECT T.ID_TREINO,
                       I.NOME_INSTRUTOR,
                       T.NOME_TREINO,
                       T.OBJETIVO,
                       T.DATA_CRIACAO
                FROM TREINO T
                JOIN INSTRUTOR I ON I.ID_INSTRUTOR = T.ID_INSTRUTOR
                WHERE T.ID_ALUNO = {int(id_aluno)}
                ORDER BY T.DATA_CRIACAO DESC
            """

            cursor.execute(query)
            return cursor.fetchall()
        finally:
            oracle.close()