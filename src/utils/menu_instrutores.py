from controller.controller_instrutor import ControllerInstrutor


def menu_instrutores():
    controller = ControllerInstrutor()

    while True:
        print("\n" + "=" * 40)
        print("       GERENCIAMENTO DE INSTRUTORES")
        print("=" * 40)
        print("1 - Listar instrutores")
        print("2 - Cadastrar instrutor")
        print("3 - Atualizar instrutor")
        print("4 - Excluir instrutor")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                instrutores = controller.listar()

                print("\n--- LISTA DE INSTRUTORES ---")

                if not instrutores:
                    print("Nenhum instrutor cadastrado.")
                else:
                    for instrutor in instrutores:
                        print(
                            f"ID: {instrutor[0]} | "
                            f"Nome: {instrutor[1]} | "
                            f"E-mail: {instrutor[2]} | "
                            f"Telefone: {instrutor[3]}"
                        )

            elif opcao == "2":
                print("\n--- CADASTRAR INSTRUTOR ---")
                nome = input("Nome: ").strip()
                email = input("E-mail: ").strip()
                telefone = input("Telefone: ").strip()

                if controller.inserir(nome, email, telefone):
                    print("Instrutor cadastrado com sucesso!")
                else:
                    print("Não foi possível cadastrar o instrutor.")

            elif opcao == "3":
                print("\n--- ATUALIZAR INSTRUTOR ---")
                id_instrutor = input("ID do instrutor: ").strip()

                instrutor = controller.buscar_por_id(id_instrutor)

                if not instrutor:
                    print("Instrutor não encontrado.")
                    continue

                print("Pressione Enter para manter o valor atual.")

                nome = input(f"Nome [{instrutor[1]}]: ").strip()
                email = input(f"E-mail [{instrutor[2]}]: ").strip()
                telefone = input(f"Telefone [{instrutor[3]}]: ").strip()

                nome = nome or instrutor[1]
                email = email or instrutor[2]
                telefone = telefone or instrutor[3]

                if controller.atualizar(
                    id_instrutor, nome, email, telefone
                ):
                    print("Instrutor atualizado com sucesso!")
                else:
                    print("Nenhuma alteração realizada.")

            elif opcao == "4":
                print("\n--- EXCLUIR INSTRUTOR ---")
                id_instrutor = input("ID do instrutor: ").strip()

                instrutor = controller.buscar_por_id(id_instrutor)

                if not instrutor:
                    print("Instrutor não encontrado.")
                    continue

                print(f"Nome: {instrutor[1]}")
                confirmacao = input(
                    "Tem certeza de que deseja excluir? (s/n): "
                ).strip().lower()

                if confirmacao == "s":
                    if controller.deletar(id_instrutor):
                        print("Instrutor excluído com sucesso!")
                    else:
                        print("Não foi possível excluir o instrutor.")
                else:
                    print("Exclusão cancelada.")

            elif opcao == "0":
                print("Voltando ao menu principal...")
                break

            else:
                print("Opção inválida. Tente novamente.")

        except ValueError as erro:
            print(f"Entrada inválida: {erro}")

        except Exception as erro:
            mensagem = str(erro)

            if "ORA-02292" in mensagem:
                print(
                    "\nNão foi possível excluir o instrutor, pois "
                    "ele está associado a um ou mais treinos."
                )
                print(
                    "Remova ou reassocie esses treinos antes de "
                    "tentar excluir o instrutor."
                )
            else:
                print(f"Não foi possível realizar a operação: {erro}")