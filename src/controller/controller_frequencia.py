from datetime import date, datetime

from conexion.oracle_queries import OracleQueries


class ControllerFrequencia:
    """CRUD da tabela FREQUENCIA.
    Colunas assumidas: ID_FREQUENCIA, ID_ALUNO, ID_TREINO,
    DATA_FREQUENCIA, PRESENTE ('S' ou 'N').
    Sequence assumida: FREQUENCIA_ID_FREQUENCIA_SEQ.
    """

    @staticmethod
    def _escrever(sql, params):
        """Executa INSERT/UPDATE/DELETE e retorna as linhas afetadas."""
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            return oracle.write(sql, params)
        finally:
            oracle.close()

    @staticmethod
    def _consultar(sql, params=None):
        """Executa SELECT e retorna a lista de linhas."""
        oracle = OracleQueries()
        try:
            cursor = oracle.connect()
            cursor.execute(sql, params or {})
            return cursor.fetchall()
        finally:
            oracle.close()

    @staticmethod
    def _converter_data(data):
        """Aceita AAAA-MM-DD; se vazio, usa a data de hoje."""
        if not data:
            return date.today()
        try:
            return datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    def registrar(self, id_aluno, id_treino, data_frequencia=None,
                  presente=True) -> bool:
        sql = """
            INSERT INTO FREQUENCIA (
                ID_FREQUENCIA, ID_ALUNO, ID_TREINO,
                DATA_FREQUENCIA, PRESENTE
            )
            VALUES (
                FREQUENCIA_ID_FREQUENCIA_SEQ.NEXTVAL, :id_aluno, :id_treino,
                :data_frequencia, :presente
            )
        """
        params = {
            "id_aluno": int(id_aluno),
            "id_treino": int(id_treino),
            "data_frequencia": self._converter_data(data_frequencia),
            "presente": "S" if presente else "N",
        }
        return self._escrever(sql, params) > 0

    def atualizar(self, id_frequencia, id_aluno, id_treino,
                  data_frequencia, presente) -> bool:
        sql = """
            UPDATE FREQUENCIA
            SET ID_ALUNO = :id_aluno,
                ID_TREINO = :id_treino,
                DATA_FREQUENCIA = :data_frequencia,
                PRESENTE = :presente
            WHERE ID_FREQUENCIA = :id_frequencia
        """
        params = {
            "id_aluno": int(id_aluno),
            "id_treino": int(id_treino),
            "data_frequencia": self._converter_data(data_frequencia),
            "presente": "S" if presente else "N",
            "id_frequencia": int(id_frequencia),
        }
        return self._escrever(sql, params) > 0

    def deletar(self, id_frequencia) -> bool:
        sql = "DELETE FROM FREQUENCIA WHERE ID_FREQUENCIA = :id_frequencia"
        params = {"id_frequencia": int(id_frequencia)}
        return self._escrever(sql, params) > 0

    def buscar_por_id(self, id_frequencia):
        sql = """
            SELECT ID_FREQUENCIA, ID_ALUNO, ID_TREINO,
                   DATA_FREQUENCIA, PRESENTE
            FROM FREQUENCIA
            WHERE ID_FREQUENCIA = :id_frequencia
        """
        linhas = self._consultar(sql, {"id_frequencia": int(id_frequencia)})
        return linhas[0] if linhas else None

    def listar(self):
        sql = """
            SELECT F.ID_FREQUENCIA, A.NOME_ALUNO, T.NOME_TREINO,
                   F.DATA_FREQUENCIA, F.PRESENTE
            FROM FREQUENCIA F
            JOIN ALUNO A ON A.ID_ALUNO = F.ID_ALUNO
            JOIN TREINO T ON T.ID_TREINO = F.ID_TREINO
            ORDER BY F.DATA_FREQUENCIA DESC
        """
        return self._consultar(sql)

    def listar_por_aluno(self, id_aluno):
        sql = """
            SELECT F.ID_FREQUENCIA, T.NOME_TREINO,
                   F.DATA_FREQUENCIA, F.PRESENTE
            FROM FREQUENCIA F
            JOIN TREINO T ON T.ID_TREINO = F.ID_TREINO
            WHERE F.ID_ALUNO = :id_aluno
            ORDER BY F.DATA_FREQUENCIA DESC
        """
        return self._consultar(sql, {"id_aluno": int(id_aluno)})