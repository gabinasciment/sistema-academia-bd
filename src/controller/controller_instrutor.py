from conexion.oracle_queries import OracleQueries
from model.instrutor import Instrutor


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

            # Mesma sessao: CURRVAL devolve o ID que acabou de ser gerado
            cursor.execute("SELECT INSTRUTOR_ID_INSTRUTOR_SEQ.CURRVAL FROM DUAL")
            return cursor.fetchone()[0]

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

    def obter(self, id_instrutor):
        """Busca o instrutor pelo ID e devolve um objeto Instrutor (ou None)."""
        linha = self.buscar_por_id(id_instrutor)
        if not linha:
            return None
        return Instrutor(linha[0], linha[1], linha[2], linha[3])

    def existe_email(self, email, ignorar_id=None) -> bool:
        """Verifica se ja existe instrutor com o e-mail."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = (
                "SELECT COUNT(1) FROM INSTRUTOR "
                "WHERE LOWER(EMAIL_INSTRUTOR) = LOWER('" + self._escapar(email) + "')"
            )
            if ignorar_id is not None:
                query += " AND ID_INSTRUTOR <> " + str(int(ignorar_id))

            cursor.execute(query)
            return cursor.fetchone()[0] > 0

        finally:
            oracle.close()

    def contar_treinos(self, id_instrutor) -> int:
        """Conta os treinos orientados pelo instrutor (registros filhos)."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()
            cursor.execute(
                "SELECT COUNT(1) FROM TREINO WHERE ID_INSTRUTOR = "
                + str(int(id_instrutor))
            )
            return cursor.fetchone()[0]

        finally:
            oracle.close()

    def deletar_com_treinos(self, id_instrutor) -> bool:
        """Exclui os treinos do instrutor e depois o instrutor,
        numa unica transacao."""
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()
            id_instrutor = str(int(id_instrutor))

            cursor.execute("DELETE FROM TREINO WHERE ID_INSTRUTOR = " + id_instrutor)
            cursor.execute("DELETE FROM INSTRUTOR WHERE ID_INSTRUTOR = " + id_instrutor)
            excluiu = cursor.rowcount > 0
            oracle.conn.commit()
            return excluiu

        finally:
            oracle.close()