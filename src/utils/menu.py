def exibir_menu_principal():
    print("\n" + "=" * 40)
    print("          MENU PRINCIPAL")
    print("=" * 40)
    print("1 - Gerenciar alunos")
    print("2 - Gerenciar instrutores")
    print("3 - Gerenciar treinos")
    print("4 - Gerenciar frequencias")
    print("5 - Relatorios")
    print("0 - Sair")
    print("=" * 40)

    opcao = input("Escolha uma opcao: ").strip()

    return opcao