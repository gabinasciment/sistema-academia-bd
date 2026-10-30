from controller.controller_aluno import ControllerAluno
from controller.controller_frequencia import ControllerFrequencia
from utils import menu_alunos
from utils.config import confirmar, ler_id, ler_texto

controller = ControllerFrequencia()
aluno_controller = ControllerAluno()


def listar() -> bool:
    """Lista as frequências (PK + campos descritivos). Devolve False se não houver."""
    frequencias = controller.listar()

    print("\n-------------- FREQUÊNCIAS REGISTRADAS --------------")
    if not frequencias:
        print("Nenhuma frequência registrada.")
        return False

    for frequencia in frequencias:
        print(
            f"ID: {frequencia[0]:<4} | Aluno: {frequencia[1]:<22} | "
            f"Entrada: {frequencia[2]:%d/%m/%Y %H:%M}"
        )
    return True


def listar_por_aluno():
    """Mostra as frequências de um aluno escolhido."""
    if not menu_alunos.listar():
        return

    id_aluno = ler_id("\nID do aluno: ")
    if id_aluno is None:
        return

    frequencias = controller.listar_por_aluno(id_aluno)
    print("\n------------- FREQUÊNCIAS DO ALUNO -------------")
    if not frequencias:
        print("Nenhuma frequência encontrada para esse aluno.")
        return

    for frequencia in frequencias:
        print(f"ID: {frequencia[0]} | Entrada: {frequencia[1]:%d/%m/%Y %H:%M}")


def _escolher_aluno(id_aluno_atual=None):
    """Mostra os alunos e devolve o ID escolhido (ou None)."""
    if not menu_alunos.listar():
        print("\nÉ preciso ter alunos cadastrados.")
        return None

    id_aluno = ler_texto("\nID do aluno", id_aluno_atual)

    # Verifica se o aluno existe antes de gravar
    if not id_aluno.isdigit() or aluno_controller.obter(int(id_aluno)) is None:
        print("\nAluno não encontrado.")
        return None

    return int(id_aluno)


def inserir():
    print("\n============== REGISTRAR FREQUÊNCIA ==============")

    id_aluno = _escolher_aluno()
    if id_aluno is None:
        return

    data_hora = ler_texto(
        "Data e hora da entrada (AAAA-MM-DD HH:MM, ENTER = agora)"
    )

    novo_id = controller.registrar_entrada(id_aluno, data_hora or None)

    print("\nFrequência registrada com sucesso!")
    print(controller.obter(novo_id).to_string())


def atualizar():
    print("\n============== ATUALIZAR FREQUÊNCIA ==============")

    if not listar():
        return

    id_frequencia = ler_id("\nID da frequência que deseja atualizar: ")
    if id_frequencia is None:
        return

    frequencia = controller.obter(id_frequencia)
    if frequencia is None:
        print("\nFrequência não encontrada.")
        return

    print("\nDados atuais:")
    print(frequencia.to_string())
    print("\nInforme os novos dados (ENTER mantém o valor atual).")

    id_aluno = _escolher_aluno(frequencia.get_aluno().get_id_aluno())
    if id_aluno is None:
        return

    data_atual = frequencia.get_data_hora_entrada().strftime("%Y-%m-%d %H:%M")
    data_hora = ler_texto("Data e hora da entrada (AAAA-MM-DD HH:MM)", data_atual)

    controller.atualizar(id_frequencia, id_aluno, data_hora)

    # Exibe o registro atualizado (edital 6.d.7)
    print("\nFrequência atualizada com sucesso! Registro atualizado:")
    print(controller.obter(id_frequencia).to_string())


def excluir():
    print("\n=============== EXCLUIR FREQUÊNCIA ===============")

    if not listar():
        return

    id_frequencia = ler_id("\nID da frequência que deseja excluir: ")
    if id_frequencia is None:
        return

    frequencia = controller.obter(id_frequencia)
    if frequencia is None:
        print("\nFrequência não encontrada.")
        return

    print("\nFrequência selecionada:")
    print(frequencia.to_string())

    if not confirmar("\nTem certeza de que deseja excluir esta frequência? (s/n): "):
        print("\nExclusão cancelada. Voltando ao menu principal.")
        return False

    # FREQUENCIA nao e chave estrangeira em nenhuma outra tabela
    controller.deletar(id_frequencia)
    print("\nFrequência excluída com sucesso!")
