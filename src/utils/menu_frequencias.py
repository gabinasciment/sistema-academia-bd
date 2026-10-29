from controller.controller_frequencia import ControllerFrequencia
from controller.controller_aluno import ControllerAluno


def menu_frequencias():
    frequencia_controller = ControllerFrequencia()
    aluno_controller = ControllerAluno()

    while True:
        print("\n" + "=" * 40)
        print("       GERENCIAMENTO DE FREQUÊNCIAS")
        print("=" * 40)
        print("1 - Listar frequências")
        print("2 - Registrar entrada")
        print("3 - Atualizar frequência")
        print("4 - Excluir frequência")
        print("5 - Listar frequências por aluno")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                frequencias = frequencia_controller.listar()

                print("\n--- LISTA DE FREQUÊNCIAS ---")

                if not frequencias:
                    print("Nenhuma frequência registrada.")
                else:
                    for frequencia in frequencias:
                        print(
                            f"ID: {frequencia[0]} | "
                            f"Aluno: {frequencia[1]} | "
                            f"Data e hora: {frequencia[2]}"
                        )

            elif opcao == "2":
                print("\n--- REGISTRAR ENTRADA ---")

                alunos = aluno_controller.listar()

                if not alunos:
                    print("Não há alunos cadastrados.")
                    continue

                print("Alunos disponíveis:")
                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                id_aluno = input("\nID do aluno: ").strip()

                usar_data = input(
                    "Informar data/hora manualmente? (s/n): "
                ).strip().lower()

                if usar_data == "s":
                    data_hora = input(
                        "Data e hora (AAAA-MM-DD HH:MM ou "
                        "AAAA-MM-DD HH:MM:SS): "
                    ).strip()

                    sucesso = frequencia_controller.registrar_entrada(
                        id_aluno, data_hora
                    )
                else:
                    sucesso = frequencia_controller.registrar_entrada(
                        id_aluno
                    )

                if sucesso:
                    print("Entrada registrada com sucesso!")
                else:
                    print("Não foi possível registrar a entrada.")

            elif opcao == "3":
                print("\n--- ATUALIZAR FREQUÊNCIA ---")

                id_frequencia = input("ID da frequência: ").strip()
                frequencia = frequencia_controller.buscar_por_id(
                    id_frequencia
                )

                if not frequencia:
                    print("Frequência não encontrada.")
                    continue

                alunos = aluno_controller.listar()

                print("\nAlunos disponíveis:")
                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                id_aluno = input(
                    f"ID do aluno [{frequencia[1]}]: "
                ).strip() or frequencia[1]

                data_atual = frequencia[2].strftime("%Y-%m-%d %H:%M:%S")
                data_hora = input(
                    f"Data/hora [{data_atual}]: "
                ).strip() or data_atual

                if frequencia_controller.atualizar(
                    id_frequencia, id_aluno, data_hora
                ):
                    print("Frequência atualizada com sucesso!")
                else:
                    print("Nenhuma alteração realizada.")

            elif opcao == "4":
                print("\n--- EXCLUIR FREQUÊNCIA ---")

                id_frequencia = input("ID da frequência: ").strip()
                frequencia = frequencia_controller.buscar_por_id(
                    id_frequencia
                )

                if not frequencia:
                    print("Frequência não encontrada.")
                    continue

                confirmacao = input(
                    "Confirma a exclusão? (s/n): "
                ).strip().lower()

                if confirmacao == "s":
                    if frequencia_controller.deletar(id_frequencia):
                        print("Frequência excluída com sucesso!")
                    else:
                        print("Não foi possível excluir a frequência.")
                else:
                    print("Exclusão cancelada.")

            elif opcao == "5":
                print("\n--- FREQUÊNCIAS POR ALUNO ---")

                alunos = aluno_controller.listar()

                if not alunos:
                    print("Nenhum aluno cadastrado.")
                    continue

                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                id_aluno = input("\nID do aluno: ").strip()
                frequencias = frequencia_controller.listar_por_aluno(
                    id_aluno
                )

                if not frequencias:
                    print("Nenhuma frequência encontrada para esse aluno.")
                else:
                    for frequencia in frequencias:
                        print(
                            f"ID: {frequencia[0]} | "
                            f"Data e hora: {frequencia[1]}"
                        )

            elif opcao == "0":
                print("Voltando ao menu principal...")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError as erro:
            print(f"Dados inválidos: {erro}")

        except Exception as erro:
            mensagem = str(erro)

            if "ORA-02291" in mensagem:
                print(
                    "Não foi possível salvar: o aluno informado "
                    "não existe no banco."
                )
            else:
                print(f"Não foi possível realizar a operação: {erro}")