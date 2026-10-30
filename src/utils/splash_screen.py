
import time
from conexion.oracle_queries import OracleQueries


def exibir_splash():
    print("=" * 60)
    print("                 SISTEMA DE ACADEMIA")
    print("=" * 60)
    print("Disciplina: Banco de Dados")
    print("Professor: Howard Roatti")
    print("Semestre: 2026/2")
    print()
    print("Componentes do grupo:")
    print("  Esther Bagatelli")
    print("  Érika Pimenta")
    print("  Gabriela Nascimento")
    print("  Laysa Costa")
    print("  Lara Marchesi")
    print("  Caio Ferrari")
    print()
    print("-" * 60)
    print("QUANTIDADE DE REGISTROS POR ENTIDADE")
    print("-" * 60)

    oracle = OracleQueries()

    try:
        oracle.connect()

        tabelas = ["aluno", "instrutor", "treino", "frequencia"]

        for tabela in tabelas:
            query = (
                f"SELECT COUNT(1) AS total_{tabela} "
                f"FROM {tabela}"
            )
            resultado = oracle.sqlToMatrix(query)
            total = resultado[0][0][0]

            print(f"{tabela.capitalize():<15}: {total}")

    except Exception as erro:
        print("\nNão foi possível consultar os registros no Oracle.")
        print(f"Erro: {erro}")

    finally:
        oracle.close()

    print("=" * 60)
    print()
    time.sleep(2)
