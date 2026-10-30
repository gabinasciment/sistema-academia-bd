from datetime import datetime

from conexion.oracle_queries import OracleQueries
from controller.controller_aluno import ControllerAluno
from model.frequencia import Frequencia


class ControllerFrequencia:
    """CRUD da tabela FREQUENCIA.

    Colunas: ID_FREQUENCIA, ID_ALUNO, DATA_HORA_ENTRADA.
    Sequence assumida: FREQUENCIA_ID_FREQUENCIA_SEQ (confira o nome no banco).
    """

    @staticmethod
    def _converter_data_hora(valor):
        """Valida 'AAAA-MM-DD HH:MM[:SS]' e devolve 'AAAA-MM-DD HH:MM:SS'."""
        for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(valor, formato).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                continue
        raise ValueError(
            "Data/hora inválida. Use o formato AAAA-MM-DD HH:MM:SS."
        )

    def registrar_entrada(self, id_aluno, data_hora_entrada=None) -> bool:
        """Registra a entrada do aluno. Sem data/hora, usa o momento atual."""
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            if data_hora_entrada:
                data_hora = self._converter_data_hora(data_hora_entrada)
                valor_data = f"TO_DATE('{data_hora}', 'YYYY-MM-DD HH24:MI:SS')"
            else:
                valor_data = "SYSDATE"

            query = f"""
                INSERT INTO FREQUENCIA (
                    ID_FREQUENCIA,
                    ID_ALUNO,
                    DATA_HORA_ENTRADA
                )
                VALUES (
                    FREQUENCIA_ID_FREQUENCIA_SEQ.NEXTVAL,
                    {int(id_aluno)},
                    {valor_data}
                )
            """

            oracle.write(query)

            # Mesma sessao: CURRVAL devolve o ID que acabou de ser gerado
            cursor.execute("SELECT FREQUENCIA_ID_FREQUENCIA_SEQ.CURRVAL FROM DUAL")
            return cursor.fetchone()[0]

        finally:
            oracle.close()

    def atualizar(self, id_frequencia, id_aluno, data_hora_entrada) -> bool:
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            data_hora = self._converter_data_hora(data_hora_entrada)

            query = f"""
                UPDATE FREQUENCIA
                SET
                    ID_ALUNO = {int(id_aluno)},
                    DATA_HORA_ENTRADA =
                        TO_DATE('{data_hora}', 'YYYY-MM-DD HH24:MI:SS')
                WHERE ID_FREQUENCIA = {int(id_frequencia)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def deletar(self, id_frequencia) -> bool:
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            query = f"""
                DELETE FROM FREQUENCIA
                WHERE ID_FREQUENCIA = {int(id_frequencia)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def buscar_por_id(self, id_frequencia):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_FREQUENCIA, ID_ALUNO, DATA_HORA_ENTRADA
                FROM FREQUENCIA
                WHERE ID_FREQUENCIA = {int(id_frequencia)}
            """

            cursor.execute(query)
            return cursor.fetchone()

        finally:
            oracle.close()

    def listar(self):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = """
                SELECT F.ID_FREQUENCIA, A.NOME_ALUNO, F.DATA_HORA_ENTRADA
                FROM FREQUENCIA F
                JOIN ALUNO A ON A.ID_ALUNO = F.ID_ALUNO
                ORDER BY F.DATA_HORA_ENTRADA DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()

    def obter(self, id_frequencia):
        """Busca a frequencia pelo ID e devolve um objeto Frequencia com o
        objeto Aluno associado (ou None)."""
        linha = self.buscar_por_id(id_frequencia)
        if not linha:
            return None
        aluno = ControllerAluno().obter(linha[1])
        return Frequencia(linha[0], aluno, linha[2])

    def listar_por_aluno(self, id_aluno):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_FREQUENCIA, DATA_HORA_ENTRADA
                FROM FREQUENCIA
                WHERE ID_ALUNO = {int(id_aluno)}
                ORDER BY DATA_HORA_ENTRADA DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()