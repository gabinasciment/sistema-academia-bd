from datetime import datetime

from conexion.oracle_queries import OracleQueries
from model.aluno import Aluno


class ControllerAluno:
    """CRUD da tabela ALUNO.

    Colunas: ID_ALUNO, NOME_ALUNO, EMAIL_ALUNO, TELEFONE_ALUNO,
    DATA_NASCIMENTO, GENERO.
    Sequence: ALUNO_ID_ALUNO_SEQ.
    """

    @staticmethod
    def _escapar(texto):
        """Duplica aspas simples para não quebrar o SQL montado como texto."""
        return texto.strip().replace("'", "''")

    @staticmethod
    def _converter_data(data_nascimento):
        """Valida AAAA-MM-DD e devolve a data no mesmo formato."""
        try:
            return datetime.strptime(
                data_nascimento, "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    @staticmethod
    def _validar(nome):
        if not nome or not nome.strip():
            raise ValueError("O nome do aluno é obrigatório.")

    def inserir(self, nome, email, telefone, data_nascimento, genero) -> bool:
        self._validar(nome)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)
            genero = self._escapar(genero)
            data_nascimento = self._converter_data(data_nascimento)

            query = f"""
                INSERT INTO ALUNO (
                    ID_ALUNO,
                    NOME_ALUNO,
                    EMAIL_ALUNO,
                    TELEFONE_ALUNO,
                    DATA_NASCIMENTO,
                    GENERO
                )
                VALUES (
                    ALUNO_ID_ALUNO_SEQ.NEXTVAL,
                    '{nome}',
                    '{email}',
                    '{telefone}',
                    TO_DATE('{data_nascimento}', 'YYYY-MM-DD'),
                    '{genero}'
                )
            """

            oracle.write(query)

            # Mesma sessao: CURRVAL devolve o ID que acabou de ser gerado
            cursor.execute("SELECT ALUNO_ID_ALUNO_SEQ.CURRVAL FROM DUAL")
            return cursor.fetchone()[0]

        finally:
            oracle.close()

    def atualizar(self, id_aluno, nome, email, telefone,
                  data_nascimento, genero) -> bool:
        self._validar(nome)
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = self._escapar(nome)
            email = self._escapar(email)
            telefone = self._escapar(telefone)
            genero = self._escapar(genero)
            data_nascimento = self._converter_data(data_nascimento)

            query = f"""
                UPDATE ALUNO
                SET
                    NOME_ALUNO = '{nome}',
                    EMAIL_ALUNO = '{email}',
                    TELEFONE_ALUNO = '{telefone}',
                    DATA_NASCIMENTO =
                        TO_DATE('{data_nascimento}', 'YYYY-MM-DD'),
                    GENERO = '{genero}'
                WHERE ID_ALUNO = {int(id_aluno)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def deletar(self, id_aluno) -> bool:
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            query = f"""
                DELETE FROM ALUNO
                WHERE ID_ALUNO = {int(id_aluno)}
            """

            oracle.write(query)
            return cursor.rowcount > 0

        finally:
            oracle.close()

    def buscar_por_id(self, id_aluno):
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = f"""
                SELECT ID_ALUNO, NOME_ALUNO, EMAIL_ALUNO,
                       TELEFONE_ALUNO, DATA_NASCIMENTO, GENERO
                FROM ALUNO
                WHERE ID_ALUNO = {int(id_aluno)}
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
                SELECT ID_ALUNO, NOME_ALUNO, EMAIL_ALUNO,
                       TELEFONE_ALUNO, DATA_NASCIMENTO, GENERO
                FROM ALUNO
                ORDER BY NOME_ALUNO
            """

            cursor.execute(query)
            return cursor.fetchall()

        finally:
            oracle.close()

    def obter(self, id_aluno):
        """Busca o aluno pelo ID e devolve um objeto Aluno (ou None)."""
        linha = self.buscar_por_id(id_aluno)
        if not linha:
            return None
        return Aluno(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5])

    def existe_email(self, email, ignorar_id=None) -> bool:
        """Verifica se ja existe aluno com o e-mail (antes de inserir/atualizar)."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            query = (
                "SELECT COUNT(1) FROM ALUNO "
                "WHERE LOWER(EMAIL_ALUNO) = LOWER('" + self._escapar(email) + "')"
            )
            if ignorar_id is not None:
                query += " AND ID_ALUNO <> " + str(int(ignorar_id))

            cursor.execute(query)
            return cursor.fetchone()[0] > 0

        finally:
            oracle.close()

    def contar_dependentes(self, id_aluno):
        """Conta os registros filhos do aluno: (treinos, frequencias)."""
        oracle = OracleQueries()

        try:
            cursor = oracle.connect()

            cursor.execute(
                "SELECT COUNT(1) FROM TREINO WHERE ID_ALUNO = " + str(int(id_aluno))
            )
            treinos = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(1) FROM FREQUENCIA WHERE ID_ALUNO = " + str(int(id_aluno))
            )
            frequencias = cursor.fetchone()[0]

            return treinos, frequencias

        finally:
            oracle.close()

    def deletar_com_dependentes(self, id_aluno) -> bool:
        """Exclui os treinos e frequencias do aluno e depois o aluno,
        numa unica transacao (se algo falhar, nada e apagado)."""
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()
            id_aluno = str(int(id_aluno))

            cursor.execute("DELETE FROM TREINO WHERE ID_ALUNO = " + id_aluno)
            cursor.execute("DELETE FROM FREQUENCIA WHERE ID_ALUNO = " + id_aluno)
            cursor.execute("DELETE FROM ALUNO WHERE ID_ALUNO = " + id_aluno)
            excluiu = cursor.rowcount > 0
            oracle.conn.commit()
            return excluiu

        finally:
            oracle.close()