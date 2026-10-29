
from utils.menu_alunos import menu_alunos
from utils.menu_instrutores import menu_instrutores
from utils.splash_screen import exibir_splash
from utils.menu import exibir_menu_principal
from utils.menu_treinos import menu_treinos
from utils.menu_frequencias import menu_frequencias
from reports.relatorios import Relatorio


def menu_relatorios():
    relatorio = Relatorio()

    while True:
        print("\n" + "=" * 40)
        print("          MENU DE RELATORIOS")
        print("=" * 40)
        print("1 - Treinos por aluno")
        print("2 - Treinos com instrutores")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            relatorio.get_relatorio_treinos_por_aluno()
        elif opcao == "2":
            relatorio.get_relatorio_treinos_com_instrutores()
        elif opcao == "0":
            break
        else:
            print("Opcao invalida. Tente novamente.")


def main():
    exibir_splash()

    while True:
        opcao = exibir_menu_principal()

        if opcao == "1":
            menu_alunos()
        elif opcao == "2":
            menu_instrutores()
        elif opcao == "3":
            menu_treinos()
        elif opcao == "4":
            menu_frequencias()
        elif opcao == "5":
            menu_relatorios()
        elif opcao == "0":
            print("\nEncerrando o Sistema de Academia...")
            break
        else:
            print("\nOpcao invalida. Tente novamente.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()