from datetime import datetime

from conexion.oracle_queries import OracleQueries


class ControllerTreino:
    """CRUD da tabela TREINO.

    Colunas assumidas: ID_TREINO, ID_ALUNO, ID_INSTRUTOR, NOME_TREINO,
    DESCRICAO, DATA_INICIO.
    Sequence assumida: TREINO_ID_TREINO_SEQ (confira o nome no banco).
    """

    @staticmethod
    def _escapar(texto):
        """Duplica aspas simples para não quebrar o SQL montado como texto."""
        return texto.strip().replace("'", "''")

    @staticmethod
    def _converter_data(data):
        """Valida AAAA-MM-DD e devolve a data no mesmo formato."""
        try:
            return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    @staticmethod
    def _validar(nome_treino):
        if not nome_treino or not nome_treino.strip():
            raise ValueError("O nome do treino é obrigatório.")

    def inserir(self, id_aluno, id_instrutor, nome_treino, descricao,
                data_inicio) -> bool:
        self._validar(nome_treino)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome_treino = self._escapar(nome_treino)
            descricao = self._escapar(descricao)
            data_inicio = self._converter_data(data_inicio)

            query = f"""
                INSERT INTO TREINO (
                    ID_TREINO,
                    ID_ALUNO,
                    ID_INSTRUTOR,
                    NOME_TREINO,
                    DESCRICAO,
                    DATA_INICIO
                )
                VALUES (
                    TREINO_ID_TREINO_SEQ.NEXTVAL,
                    {int(id_aluno)},
                    {int(id_instrutor)},
                    '{nome_treino}',
                    '{descricao}',
                    TO_DATE('{data_inicio}', 'YYYY-MM-DD')
                )
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def atualizar(self, id_treino, id_aluno, id_instrutor, nome_treino,
                  descricao, data_inicio) -> bool:
        self._validar(nome_treino)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome_treino = self._escapar(nome_treino)
            descricao = self._escapar(descricao)
            data_inicio = self._converter_data(data_inicio)

            query = f"""
                UPDATE TREINO
                SET
                    ID_ALUNO = {int(id_aluno)},
                    ID_INSTRUTOR = {int(id_instrutor)},
                    NOME_TREINO = '{nome_treino}',
                    DESCRICAO = '{descricao}',
                    DATA_INICIO = TO_DATE('{data_inicio}', 'YYYY-MM-DD')
                WHERE ID_TREINO = {int(id_treino)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def deletar(self, id_treino) -> bool:
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
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_TREINO, ID_ALUNO, ID_INSTRUTOR,
                       NOME_TREINO, DESCRICAO, DATA_INICIO
                FROM TREINO
                WHERE ID_TREINO = {int(id_treino)}
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
                SELECT T.ID_TREINO, A.NOME_ALUNO, I.NOME_INSTRUTOR,
                       T.NOME_TREINO, T.DESCRICAO, T.DATA_INICIO
                FROM TREINO T
                JOIN ALUNO A ON A.ID_ALUNO = T.ID_ALUNO
                JOIN INSTRUTOR I ON I.ID_INSTRUTOR = T.ID_INSTRUTOR
                ORDER BY T.DATA_INICIO DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()

    def listar_por_aluno(self, id_aluno):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT T.ID_TREINO, I.NOME_INSTRUTOR,
                       T.NOME_TREINO, T.DESCRICAO, T.DATA_INICIO
                FROM TREINO T
                JOIN INSTRUTOR I ON I.ID_INSTRUTOR = T.ID_INSTRUTOR
                WHERE T.ID_ALUNO = {int(id_aluno)}
                ORDER BY T.DATA_INICIO DESC
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()