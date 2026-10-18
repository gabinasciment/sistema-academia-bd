###########################################################################
# Modulo de conexao com o Banco de Dados Oracle
#
# Adaptado do projeto de exemplo da disciplina
# (https://github.com/howardroatti/example_crud_oracle - Prof. Howard Roatti)
#
# Mudancas em relacao ao exemplo:
#   - o arquivo de usuario/senha e encontrado a partir da pasta deste
#     modulo, entao funciona de qualquer pasta em que o programa rodar
#   - self.cur e self.conn comecam como None, para nao dar erro ao
#     fechar um objeto que nunca chegou a conectar
#   - connect() tenta o SID (XE) e, se falhar, o service name (XEPDB1)
###########################################################################
import json
import os
import cx_Oracle
from pandas import DataFrame

# Pasta onde este arquivo esta (src/conexion)
PASTA_CONEXION = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_AUTENTICACAO = os.path.join(PASTA_CONEXION, "passphrase", "authentication.oracle")


class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'
        self.sid = 'XE'
        self.conn = None
        self.cur = None

        # O arquivo tem o formato: usuario,senha
        with open(ARQUIVO_AUTENTICACAO, "r") as f:
            self.user, self.passwd = f.read().strip().split(',')

    def __del__(self):
        if self.cur:
            self.close()

    def connectionString(self, in_container:bool=False):
        '''
        Monta a string de conexao (DSN) com o servidor Oracle.
        - in_container=False: conecta pelo SID (XE)
        - in_container=True:  conecta pelo service name (XEPDB1)
        '''
        if not in_container:
            return cx_Oracle.makedsn(host=self.host, port=self.port, sid=self.sid)
        return cx_Oracle.makedsn(host=self.host, port=self.port, service_name=self.service_name)

    def connect(self):
        '''
        Abre a conexao com o Oracle e devolve o cursor,
        que e o objeto usado para executar os comandos SQL.
        Tenta primeiro pelo SID (XE) e, se nao conseguir, pelo
        service name (XEPDB1), usado nas versoes mais novas do Oracle.
        '''
        try:
            self.conn = cx_Oracle.connect(user=self.user,
                                          password=self.passwd,
                                          dsn=self.connectionString())
        except cx_Oracle.DatabaseError:
            self.conn = cx_Oracle.connect(user=self.user,
                                          password=self.passwd,
                                          dsn=self.connectionString(in_container=True))
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query:str) -> DataFrame:
        '''
        Executa uma consulta (SELECT) e devolve o resultado
        como uma tabela do Pandas (DataFrame).
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query:str) -> tuple:
        '''
        Executa uma consulta e devolve (lista de linhas, lista com os nomes das colunas).
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query:str):
        '''
        Executa uma consulta e devolve o resultado em formato JSON.
        '''
        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query:str):
        '''
        Executa um INSERT, UPDATE ou DELETE e grava de vez (COMMIT).
        So funciona se o objeto foi criado com can_write=True.
        '''
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str):
        '''
        Executa um comando DDL (CREATE, DROP, ALTER).
        No Oracle esses comandos ja gravam sozinhos, sem precisar de COMMIT.
        '''
        self.cur.execute(query)
