from datetime import datetime
from conexion.oracle_queries import OracleQueries


class ControllerAluno:

    @staticmethod
    def _converter_data(data_nascimento):
        try:
            return datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    @staticmethod
    def _executar(sql, params):
        """Executa uma escrita e retorna o numero de linhas afetadas."""
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            return oracle.write(sql, params)
        finally:
            oracle.close()

    def inserir(self, nome, email, telefone, data_nascimento, genero) -> bool:
        sql = """
            INSERT INTO ALUNO (
                ID_ALUNO, NOME_ALUNO, EMAIL_ALUNO,
                TELEFONE_ALUNO, DATA_NASCIMENTO, GENERO
            )
            VALUES (
                ALUNO_ID_ALUNO_SEQ.NEXTVAL, :nome, :email,
                :telefone, :data_nascimento, :genero
            )
        """
        params = {
            "nome": nome.strip(),
            "email": email.strip(),
            "telefone": telefone.strip(),
            "data_nascimento": self._converter_data(data_nascimento),
            "genero": genero.strip(),
        }
        return self._executar(sql, params) > 0

    def atualizar(self, id_aluno, nome, email, telefone,
                  data_nascimento, genero) -> bool:
        sql = """
            UPDATE ALUNO
            SET NOME_ALUNO = :nome,
                EMAIL_ALUNO = :email,
                TELEFONE_ALUNO = :telefone,
                DATA_NASCIMENTO = :data_nascimento,
                GENERO = :genero
            WHERE ID_ALUNO = :id_aluno
        """
        params = {
            "nome": nome.strip(),
            "email": email.strip(),
            "telefone": telefone.strip(),
            "data_nascimento": self._converter_data(data_nascimento),
            "genero": genero.strip(),
            "id_aluno": int(id_aluno),
        }
        return self._executar(sql, params) > 0