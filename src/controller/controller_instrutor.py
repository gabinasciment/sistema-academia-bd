from conexion.oracle_queries import OracleQueries


class ControllerInstrutor:
    """Controlador CRUD da tabela INSTRUTOR."""

    @staticmethod
    def _escapar(texto):
        """Prepara textos para uso em consultas SQL."""
        if texto is None:
            return ""
        return str(texto).strip().replace("'", "''")

    @staticmethod
    def _validar(nome, email, telefone):
        """Verifica se os campos obrigatórios foram preenchidos."""
        if not nome or not nome.strip():
            raise ValueError("O nome do instrutor é obrigatório.")

        if not email or not email.strip():
            raise ValueError("O e-mail do instrutor é obrigatório.")

        if not telefone or not telefone.strip():
            raise ValueError("O telefone do instrutor é obrigatório.")

    def inserir(self, nome, email, telefone) -> bool:
        """Cadastra um novo instrutor."""
        self._validar(nome, email, telefone)

        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)

            query = f"""
                INSERT INTO INSTRUTOR (
                    ID_INSTRUTOR,
                    NOME_INSTRUTOR,
                    EMAIL_INSTRUTOR,
                    TELEFONE_INSTRUTOR
                ) VALUES (
                    INSTRUTOR_ID_INSTRUTOR_SEQ.NEXTVAL,
                    '{nome}',
                    '{email}',
                    '{telefone}'
                )
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def atualizar(self, id_instrutor, nome, email, telefone) -> bool:
        """Atualiza os dados de um instrutor existente."""
        self._validar(nome, email, telefone)

        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            id_instrutor = int(id_instrutor)
            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)

            query = f"""
                UPDATE INSTRUTOR
                SET NOME_INSTRUTOR = '{nome}',
                    EMAIL_INSTRUTOR = '{email}',
                    TELEFONE_INSTRUTOR = '{telefone}'
                WHERE ID_INSTRUTOR = {id_instrutor}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def deletar(self, id_instrutor) -> bool:
        """Exclui um instrutor pelo ID."""
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            id_instrutor = int(id_instrutor)

            query = f"""
                DELETE FROM INSTRUTOR
                WHERE ID_INSTRUTOR = {id_instrutor}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def buscar_por_id(self, id_instrutor):
        """Busca um instrutor pelo ID."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            id_instrutor = int(id_instrutor)

            query = f"""
                SELECT ID_INSTRUTOR,
                       NOME_INSTRUTOR,
                       EMAIL_INSTRUTOR,
                       TELEFONE_INSTRUTOR
                FROM INSTRUTOR
                WHERE ID_INSTRUTOR = {id_instrutor}
            """

            cursor.execute(query)
            return cursor.fetchone()

        finally:
            oracle.close()

    def listar(self):
        """Retorna todos os instrutores cadastrados."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = """
                SELECT ID_INSTRUTOR,
                       NOME_INSTRUTOR,
                       EMAIL_INSTRUTOR,
                       TELEFONE_INSTRUTOR
                FROM INSTRUTOR
                ORDER BY NOME_INSTRUTOR
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()