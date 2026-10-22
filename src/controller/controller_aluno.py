from conexion.oracle_queries import OracleQueries


class ControllerAluno:

    def inserir(self, nome, email, telefone, data_nascimento, genero):
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = nome.replace("'", "''")
            email = email.replace("'", "''")
            telefone = telefone.replace("'", "''")
            genero = genero.replace("'", "''")

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
            print("Aluno cadastrado com sucesso!")

        except Exception as erro:
            print("Erro ao cadastrar aluno:", erro)

        finally:
            oracle.close()

    def atualizar(
        self, id_aluno, nome, email, telefone,
        data_nascimento, genero
    ):
        oracle = OracleQueries(can_write=True)

        try:
            cursor = oracle.connect()

            nome = nome.replace("'", "''")
            email = email.replace("'", "''")
            telefone = telefone.replace("'", "''")
            genero = genero.replace("'", "''")

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

            if cursor.rowcount > 0:
                print("Aluno atualizado com sucesso!")
            else:
                print("Nenhum aluno encontrado com esse ID.")

        except Exception as erro:
            print("Erro ao atualizar aluno:", erro)

        finally:
            oracle.close()