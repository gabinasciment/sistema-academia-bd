from controller.controller_treino import ControllerTreino
from controller.controller_aluno import ControllerAluno
from controller.controller_instrutor import ControllerInstrutor


def menu_treinos():
    treino_controller = ControllerTreino()
    aluno_controller = ControllerAluno()
    instrutor_controller = ControllerInstrutor()

    while True:
        print("\n" + "=" * 40)
        print("          GERENCIAMENTO DE TREINOS")
        print("=" * 40)
        print("1 - Listar treinos")
        print("2 - Cadastrar treino")
        print("3 - Atualizar treino")
        print("4 - Excluir treino")
        print("5 - Listar treinos por aluno")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                treinos = treino_controller.listar()

                print("\n--- LISTA DE TREINOS ---")

                if not treinos:
                    print("Nenhum treino cadastrado.")
                else:
                    for treino in treinos:
                        print(
                            f"ID: {treino[0]} | "
                            f"Aluno: {treino[1]} | "
                            f"Instrutor: {treino[2]} | "
                            f"Treino: {treino[3]} | "
                            f"Objetivo: {treino[4] or '-'} | "
                            f"Data de criação: {treino[5]}"
                        )

            elif opcao == "2":
                print("\n--- CADASTRAR TREINO ---")

                alunos = aluno_controller.listar()
                instrutores = instrutor_controller.listar()

                if not alunos:
                    print("Não há alunos cadastrados. Cadastre um aluno primeiro.")
                    continue

                if not instrutores:
                    print("Não há instrutores cadastrados. Cadastre um instrutor primeiro.")
                    continue

                print("\nAlunos disponíveis:")
                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                print("\nInstrutores disponíveis:")
                for instrutor in instrutores:
                    print(f"ID: {instrutor[0]} | Nome: {instrutor[1]}")

                id_aluno = input("\nID do aluno: ").strip()
                id_instrutor = input("ID do instrutor: ").strip()
                nome_treino = input("Nome do treino: ").strip()
                objetivo = input("Objetivo do treino (opcional): ").strip()

                if treino_controller.inserir(
                    id_aluno, id_instrutor, nome_treino, objetivo
                ):
                    print("Treino cadastrado com sucesso!")
                else:
                    print("Não foi possível cadastrar o treino.")

            elif opcao == "3":
                print("\n--- ATUALIZAR TREINO ---")

                id_treino = input("ID do treino: ").strip()
                treino = treino_controller.buscar_por_id(id_treino)

                if not treino:
                    print("Treino não encontrado.")
                    continue

                alunos = aluno_controller.listar()
                instrutores = instrutor_controller.listar()

                print("\nAlunos disponíveis:")
                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                print("\nInstrutores disponíveis:")
                for instrutor in instrutores:
                    print(f"ID: {instrutor[0]} | Nome: {instrutor[1]}")

                print("\nPressione Enter para manter o valor atual.")

                id_aluno = input(f"ID do aluno [{treino[1]}]: ").strip()
                id_instrutor = input(f"ID do instrutor [{treino[2]}]: ").strip()
                nome = input(f"Nome [{treino[3]}]: ").strip()
                objetivo = input(f"Objetivo [{treino[4] or ''}]: ").strip()

                id_aluno = id_aluno or treino[1]
                id_instrutor = id_instrutor or treino[2]
                nome = nome or treino[3]
                objetivo = objetivo or (treino[4] or "")

                if treino_controller.atualizar(
                    id_treino, id_aluno, id_instrutor, nome, objetivo
                ):
                    print("Treino atualizado com sucesso!")
                else:
                    print("Nenhuma alteração realizada.")

            elif opcao == "4":
                print("\n--- EXCLUIR TREINO ---")

                id_treino = input("ID do treino: ").strip()
                treino = treino_controller.buscar_por_id(id_treino)

                if not treino:
                    print("Treino não encontrado.")
                    continue

                print(f"Treino: {treino[3]}")
                confirmacao = input(
                    "Tem certeza de que deseja excluir? (s/n): "
                ).strip().lower()

                if confirmacao == "s":
                    if treino_controller.deletar(id_treino):
                        print("Treino excluído com sucesso!")
                    else:
                        print("Não foi possível excluir o treino.")
                else:
                    print("Exclusão cancelada.")

            elif opcao == "5":
                print("\n--- TREINOS POR ALUNO ---")

                alunos = aluno_controller.listar()

                if not alunos:
                    print("Nenhum aluno cadastrado.")
                    continue

                for aluno in alunos:
                    print(f"ID: {aluno[0]} | Nome: {aluno[1]}")

                id_aluno = input("\nInforme o ID do aluno: ").strip()
                treinos = treino_controller.listar_por_aluno(id_aluno)

                if not treinos:
                    print("Esse aluno não possui treinos cadastrados.")
                else:
                    for treino in treinos:
                        print(
                            f"ID: {treino[0]} | "
                            f"Instrutor: {treino[1]} | "
                            f"Treino: {treino[2]} | "
                            f"Objetivo: {treino[3] or '-'} | "
                            f"Data de criação: {treino[4]}"
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
                    "Não foi possível salvar: o aluno ou instrutor informado "
                    "não existe no banco."
                )
            elif "ORA-02292" in mensagem:
                print(
                    "Não foi possível excluir: existem registros associados "
                    "a esse treino."
                )
            else:
                print(f"Não foi possível realizar a operação: {erro}")