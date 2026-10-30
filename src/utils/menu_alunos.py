from controller.controller_aluno import ControllerAluno


def menu_alunos():
    controller = ControllerAluno()

    while True:
        print("\n" + "=" * 40)
        print("          GERENCIAR ALUNOS")
        print("=" * 40)
        print("1 - Listar alunos")
        print("2 - Cadastrar aluno")
        print("3 - Atualizar aluno")
        print("4 - Excluir aluno")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opcao: ").strip()

        # LISTAR ALUNOS
        if opcao == "1":
            try:
                alunos = controller.listar()

                print("\n========== LISTA DE ALUNOS ==========")

                if not alunos:
                    print("Nenhum aluno encontrado.")
                else:
                    for aluno in alunos:
                        print("-" * 40)
                        print(f"ID: {aluno[0]}")
                        print(f"Nome: {aluno[1]}")
                        print(f"E-mail: {aluno[2]}")
                        print(f"Telefone: {aluno[3]}")
                        print(f"Data de nascimento: {aluno[4]}")
                        print(f"Gênero: {aluno[5]}")

            except Exception as erro:
                print(f"\nNao foi possivel listar os alunos: {erro}")

            input("\nPressione ENTER para continuar...")

        # CADASTRAR ALUNO
        elif opcao == "2":
            print("\n========== CADASTRAR ALUNO ==========")

            try:
                nome = input("Nome: ").strip()
                email = input("E-mail: ").strip()
                telefone = input("Telefone: ").strip()
                data_nascimento = input(
                    "Data de nascimento (AAAA-MM-DD): "
                ).strip()
                genero = input("Genero: ").strip()

                sucesso = controller.inserir(
                    nome,
                    email,
                    telefone,
                    data_nascimento,
                    genero
                )

                if sucesso:
                    print("\nAluno cadastrado com sucesso!")
                else:
                    print("\nNao foi possivel confirmar o cadastro.")

            except ValueError as erro:
                print(f"\nDados invalidos: {erro}")
            except Exception as erro:
                print(f"\nErro ao cadastrar aluno: {erro}")

            input("\nPressione ENTER para continuar...")

        # ATUALIZAR ALUNO
        elif opcao == "3":
            print("\n========== ATUALIZAR ALUNO ==========")

            try:
                id_aluno = input("ID do aluno que deseja atualizar: ").strip()

                if not id_aluno.isdigit() or int(id_aluno) <= 0:
                    print("\nInforme um ID numerico valido.")
                    input("\nPressione ENTER para continuar...")
                    continue

                aluno = controller.buscar_por_id(int(id_aluno))

                if not aluno:
                    print("\nAluno nao encontrado.")
                else:
                    print("\nDados atuais do aluno:")
                    print(f"ID: {aluno[0]}")
                    print(f"Nome: {aluno[1]}")
                    print(f"E-mail: {aluno[2]}")
                    print(f"Telefone: {aluno[3]}")
                    print(f"Data de nascimento: {aluno[4]}")
                    print(f"Genero: {aluno[5]}")

                    print("\nDigite os novos dados do aluno.")

                    nome = input("Novo nome: ").strip()
                    email = input("Novo e-mail: ").strip()
                    telefone = input("Novo telefone: ").strip()
                    data_nascimento = input(
                        "Nova data de nascimento (AAAA-MM-DD): "
                    ).strip()
                    genero = input("Novo genero: ").strip()

                    confirmar = input(
                        "\nConfirma a atualizacao? (s/n): "
                    ).strip().lower()

                    if confirmar == "s":
                        sucesso = controller.atualizar(
                            int(id_aluno),
                            nome,
                            email,
                            telefone,
                            data_nascimento,
                            genero
                        )

                        if sucesso:
                            print("\nAluno atualizado com sucesso!")
                        else:
                            print("\nNenhum aluno foi atualizado.")
                    else:
                        print("\nAtualizacao cancelada.")

            except ValueError as erro:
                print(f"\nDados invalidos: {erro}")
            except Exception as erro:
                print(f"\nErro ao atualizar aluno: {erro}")

            input("\nPressione ENTER para continuar...")

        # EXCLUIR ALUNO
        elif opcao == "4":
            print("\n========== EXCLUIR ALUNO ==========")

            try:
                id_aluno = input("ID do aluno que deseja excluir: ").strip()

                if not id_aluno.isdigit() or int(id_aluno) <= 0:
                    print("\nInforme um ID numerico valido.")
                else:
                    aluno = controller.buscar_por_id(int(id_aluno))

                    if not aluno:
                        print("\nAluno nao encontrado.")
                    else:
                        print("\nAluno selecionado para exclusao:")
                        print(f"ID: {aluno[0]}")
                        print(f"Nome: {aluno[1]}")
                        print(f"E-mail: {aluno[2]}")
                        print(f"Telefone: {aluno[3]}")

                        confirmar = input(
                            "\nTem certeza de que deseja excluir este aluno? (s/n): "
                        ).strip().lower()

                        if confirmar == "s":
                            sucesso = controller.deletar(int(id_aluno))

                            if sucesso:
                                print("\nAluno excluido com sucesso!")
                            else:
                                print("\nNenhum aluno foi excluido.")
                        else:
                            print("\nExclusao cancelada.")

         
            except ValueError as erro:
                print(f"\nID invalido: {erro}")

            except Exception as erro:
                mensagem = str(erro)

                if "ORA-02292" in mensagem:
                    print("\nNao foi possivel excluir o aluno.")
                    print("Este aluno possui treinos ou frequencias associados.")
                    print("Exclua primeiro os registros relacionados ou")
                    print("escolha outro aluno para realizar a exclusao.")
                else:
                    print(f"\nErro ao excluir aluno: {erro}")


            input("\nPressione ENTER para continuar...")

        # VOLTAR AO MENU PRINCIPAL
        elif opcao == "0":
            break

        else:
            print("\nOpcao invalida. Tente novamente.")