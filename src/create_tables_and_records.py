# Cria as tabelas do Sistema de Academia e insere os dados de exemplo.
# Como rodar (dentro da pasta src): python3 create_tables_and_records.py
import os
from conexion.oracle_queries import OracleQueries

# Pasta sql/ fica um nivel acima de src/
PASTA_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql")

TABELAS = ["aluno", "instrutor", "treino", "frequencia"]

# Mesma consulta pedida no edital para a splash screen
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'


def ler_comandos(nome_arquivo:str) -> list:
    '''
    Le um arquivo .sql e devolve a lista de comandos, separando pelo ";".
    Linhas que sao so comentario (comecam com --) sao removidas, e
    pedacos que ficarem vazios sao ignorados.
    '''
    with open(os.path.join(PASTA_SQL, nome_arquivo), "r", encoding="utf-8") as f:
        conteudo = f.read()

    comandos = []
    for pedaco in conteudo.split(";"):
        linhas = [linha for linha in pedaco.splitlines()
                  if not linha.strip().startswith("--")]
        comando = "\n".join(linhas).strip()
        if len(comando) > 0:
            comandos.append(comando)
    return comandos


def create_tables(comandos:list):
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for comando in comandos:
        print(comando)
        try:
            oracle.executeDDL(comando)
            print("-> OK\n")
        except Exception as e:
            # Na primeira execucao os DROPs falham porque nada existe ainda
            print(f"-> Aviso: {e}\n")


def generate_records(comandos:list):
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    erros = 0
    for comando in comandos:
        try:
            oracle.write(comando)   # write ja faz o COMMIT
        except Exception as e:
            erros += 1
            print(comando)
            print(f"-> ERRO: {e}\n")
    print(f"{len(comandos) - erros} registros inseridos, {erros} com erro.")


def mostrar_totais():
    oracle = OracleQueries()
    oracle.connect()

    print("\nTOTAL DE REGISTROS POR TABELA")
    for tabela in TABELAS:
        df = oracle.sqlToDataFrame(QUERY_COUNT.format(tabela=tabela))
        print(f"  {tabela.upper():<12} {df[f'total_{tabela}'].values[0]}")


def run():
    print("Criando tabelas...\n")
    create_tables(ler_comandos("create_tables_academia.sql"))
    print("Tabelas criadas!\n")

    print("Inserindo registros de exemplo...")
    generate_records(ler_comandos("inserting_samples_records.sql"))

    mostrar_totais()


if __name__ == '__main__':
    run()
