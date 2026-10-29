from conexion.oracle_queries import OracleQueries


class ControllerInstrutor:
    """CRUD da tabela INSTRUTOR.

    Colunas assumidas: ID_INSTRUTOR, NOME_INSTRUTOR, EMAIL_INSTRUTOR,
    TELEFONE_INSTRUTOR, ESPECIALIDADE.
    Sequence assumida: INSTRUTOR_ID_INSTRUTOR_SEQ (confira o nome no banco).
    """

    @staticmethod
    def _escapar(texto):
        """Duplica aspas simples para não quebrar o SQL montado como texto."""
        return texto.strip().replace("'", "''")

    @staticmethod
    def _validar(nome):
        if not nome or not nome.strip():
            raise ValueError("O nome do instrutor é obrigatório.")

    def inserir(self, nome, email, telefone, especialidade) -> bool:
        self._validar(nome)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)
            especialidade = self._escapar(especialidade)

            query = f"""
                INSERT INTO INSTRUTOR (
                    ID_INSTRUTOR,
                    NOME_INSTRUTOR,
                    EMAIL_INSTRUTOR,
                    TELEFONE_INSTRUTOR,
                    ESPECIALIDADE
                )
                VALUES (
                    INSTRUTOR_ID_INSTRUTOR_SEQ.NEXTVAL,
                    '{nome}',
                    '{email}',
                    '{telefone}',
                    '{especialidade}'
                )
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def atualizar(self, id_instrutor, nome, email, telefone,
                  especialidade) -> bool:
        self._validar(nome)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)
            especialidade = self._escapar(especialidade)

            query = f"""
                UPDATE INSTRUTOR
                SET
                    NOME_INSTRUTOR = '{nome}',
                    EMAIL_INSTRUTOR = '{email}',
                    TELEFONE_INSTRUTOR = '{telefone}',
                    ESPECIALIDADE = '{especialidade}'
                WHERE ID_INSTRUTOR = {int(id_instrutor)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def deletar(self, id_instrutor) -> bool:
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            query = f"""
                DELETE FROM INSTRUTOR
                WHERE ID_INSTRUTOR = {int(id_instrutor)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def buscar_por_id(self, id_instrutor):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_INSTRUTOR, NOME_INSTRUTOR, EMAIL_INSTRUTOR,
                       TELEFONE_INSTRUTOR, ESPECIALIDADE
                FROM INSTRUTOR
                WHERE ID_INSTRUTOR = {int(id_instrutor)}
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
                SELECT ID_INSTRUTOR, NOME_INSTRUTOR, EMAIL_INSTRUTOR,
                       TELEFONE_INSTRUTOR, ESPECIALIDADE
                FROM INSTRUTOR
                ORDER BY NOME_INSTRUTOR
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()