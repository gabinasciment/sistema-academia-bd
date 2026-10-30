from controller.controller_aluno import ControllerAluno
from controller.controller_instrutor import ControllerInstrutor
from controller.controller_treino import ControllerTreino
from utils import menu_alunos, menu_instrutores
from utils.config import confirmar, ler_id, ler_texto

controller = ControllerTreino()
aluno_controller = ControllerAluno()
instrutor_controller = ControllerInstrutor()


def listar() -> bool:
    """Lista os treinos (PK + campos descritivos). Devolve False se não houver."""
    treinos = controller.listar()

    print("\n---------------- TREINOS CADASTRADOS ----------------")
    if not treinos:
        print("Nenhum treino cadastrado.")
        return False

    for treino in treinos:
        print(
            f"ID: {treino[0]:<4} | Treino: {treino[3]:<22} | "
            f"Aluno: {treino[1]:<20} | Instrutor: {treino[2]}"
        )
    return True


def listar_por_aluno():
    """Mostra os treinos de um aluno escolhido."""
    if not menu_alunos.listar():
        return

    id_aluno = ler_id("\nID do aluno: ")
    if id_aluno is None:
        return

    treinos = controller.listar_por_aluno(id_aluno)
    print("\n--------------- TREINOS DO ALUNO ---------------")
    if not treinos:
        print("Esse aluno não possui treinos cadastrados.")
        return

    for treino in treinos:
        print(
            f"ID: {treino[0]} | Instrutor: {treino[1]} | Treino: {treino[2]} | "
            f"Objetivo: {treino[3] or '-'} | Criado em: {treino[4]:%d/%m/%Y}"
        )


def _escolher_aluno_e_instrutor(id_aluno_atual=None, id_instrutor_atual=None):
    """Mostra alunos e instrutores e devolve os IDs escolhidos (ou None, None)."""
    if not menu_alunos.listar() or not menu_instrutores.listar():
        print("\nÉ preciso ter alunos e instrutores cadastrados.")
        return None, None

    id_aluno = ler_texto("\nID do aluno", id_aluno_atual)
    id_instrutor = ler_texto("ID do instrutor", id_instrutor_atual)

    # Verifica se o aluno e o instrutor existem antes de gravar
    if not id_aluno.isdigit() or aluno_controller.obter(int(id_aluno)) is None:
        print("\nAluno não encontrado.")
        return None, None
    if not id_instrutor.isdigit() or instrutor_controller.obter(int(id_instrutor)) is None:
        print("\nInstrutor não encontrado.")
        return None, None

    return int(id_aluno), int(id_instrutor)


def inserir():
    print("\n================ CADASTRAR TREINO ================")

    id_aluno, id_instrutor = _escolher_aluno_e_instrutor()
    if id_aluno is None:
        return

    nome_treino = ler_texto("Nome do treino")
    objetivo = ler_texto("Objetivo do treino")

    novo_id = controller.inserir(id_aluno, id_instrutor, nome_treino, objetivo)

    print("\nTreino cadastrado com sucesso!")
    print(controller.obter(novo_id).to_string())


def atualizar():
    print("\n================ ATUALIZAR TREINO ================")

    if not listar():
        return

    id_treino = ler_id("\nID do treino que deseja atualizar: ")
    if id_treino is None:
        return

    treino = controller.obter(id_treino)
    if treino is None:
        print("\nTreino não encontrado.")
        return

    print("\nDados atuais:")
    print(treino.to_string())
    print("\nInforme os novos dados (ENTER mantém o valor atual).")

    id_aluno, id_instrutor = _escolher_aluno_e_instrutor(
        treino.get_aluno().get_id_aluno(),
        treino.get_instrutor().get_id_instrutor()
    )
    if id_aluno is None:
        return

    nome_treino = ler_texto("Nome do treino", treino.get_nome_treino())
    objetivo = ler_texto("Objetivo", treino.get_objetivo() or "")

    controller.atualizar(id_treino, id_aluno, id_instrutor, nome_treino, objetivo)

    # Exibe o registro atualizado (edital 6.d.7)
    print("\nTreino atualizado com sucesso! Registro atualizado:")
    print(controller.obter(id_treino).to_string())


def excluir():
    print("\n================= EXCLUIR TREINO =================")

    if not listar():
        return

    id_treino = ler_id("\nID do treino que deseja excluir: ")
    if id_treino is None:
        return

    treino = controller.obter(id_treino)
    if treino is None:
        print("\nTreino não encontrado.")
        return

    print("\nTreino selecionado:")
    print(treino.to_string())

    if not confirmar("\nTem certeza de que deseja excluir este treino? (s/n): "):
        print("\nExclusão cancelada. Voltando ao menu principal.")
        return False

    # TREINO nao e chave estrangeira em nenhuma outra tabela
    controller.deletar(id_treino)
    print("\nTreino excluído com sucesso!")
