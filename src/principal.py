from reports.relatorios import Relatorio
from utils import config
from utils import menu_alunos, menu_instrutores, menu_treinos, menu_frequencias
from utils.splash_screen import exibir_splash

# Cada entidade tem as mesmas funcoes: listar, inserir, atualizar e excluir
ENTIDADES = {
    "1": menu_alunos,
    "2": menu_instrutores,
    "3": menu_treinos,
    "4": menu_frequencias,
}


def escolher_entidade(titulo: str):
    """Exibe o menu de entidades (edital 6.b.1, 6.c.1, 6.d.1) e devolve o
    modulo da entidade escolhida, ou None para voltar ao menu principal."""
    while True:
        print(config.MENU_ENTIDADES.format(titulo=titulo.center(50)))
        opcao = input("Escolha uma entidade: ").strip()

        if opcao == "0":
            return None
        if opcao in ENTIDADES:
            return ENTIDADES[opcao]
        print("\nOpção inválida. Tente novamente.")


def menu_relatorios():
    relatorio = Relatorio()

    while True:
        print(config.MENU_RELATORIOS)
        opcao = input("Escolha um relatório: ").strip()

        try:
            if opcao == "1":
                relatorio.get_relatorio_treinos_por_aluno()
            elif opcao == "2":
                relatorio.get_relatorio_treinos_com_instrutores()
            elif opcao == "3":
                menu_treinos.listar_por_aluno()
                input("\nPressione ENTER para voltar ao menu de relatórios...")
            elif opcao == "4":
                menu_frequencias.listar_por_aluno()
                input("\nPressione ENTER para voltar ao menu de relatórios...")
            elif opcao == "0":
                return
            else:
                print("\nOpção inválida. Tente novamente.")
        except Exception as erro:
            print("\n" + config.mensagem_erro(erro))


def inserir_registros():
    entidade = escolher_entidade("INSERIR REGISTROS")
    if entidade:
        config.executar_operacao(
            entidade.inserir, "Deseja inserir mais algum registro?"
        )


def remover_registros():
    entidade = escolher_entidade("REMOVER REGISTROS")
    if entidade:
        config.executar_operacao(
            entidade.excluir, "Deseja excluir mais algum registro?"
        )


def atualizar_registros():
    entidade = escolher_entidade("ATUALIZAR REGISTROS")
    if entidade:
        config.executar_operacao(
            entidade.atualizar, "Deseja atualizar mais algum registro?"
        )


def main():
    exibir_splash()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_relatorios()
        elif opcao == "2":
            inserir_registros()
        elif opcao == "3":
            remover_registros()
        elif opcao == "4":
            atualizar_registros()
        elif opcao == "5":
            print("\nObrigado por utilizar o Sistema de Academia!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
