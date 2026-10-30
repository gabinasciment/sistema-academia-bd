###########################################################################
# Menus do sistema e funcoes de apoio da interface (console)
# Segue a ideia do src/utils/config.py do projeto de exemplo da disciplina
###########################################################################

LINHA = "=" * 50

MENU_PRINCIPAL = f"""
{LINHA}
                 MENU PRINCIPAL
{LINHA}
1 - Relatórios
2 - Inserir registros
3 - Remover registros
4 - Atualizar registros
5 - Sair
{LINHA}"""

MENU_RELATORIOS = f"""
{LINHA}
                   RELATÓRIOS
{LINHA}
1 - Quantidade de treinos por aluno (agrupamento)
2 - Treinos com alunos e instrutores (junção)
3 - Treinos de um aluno
4 - Frequências de um aluno
0 - Voltar ao menu principal
{LINHA}"""

MENU_ENTIDADES = f"""
{LINHA}
{{titulo}}
{LINHA}
1 - Alunos
2 - Instrutores
3 - Treinos
4 - Frequências
0 - Voltar ao menu principal
{LINHA}"""

# Consulta de contagem de registros por tabela (edital, item 5.c)
QUERY_COUNT = "select count(1) as total_{tabela} from {tabela}"

# Mensagens para os erros mais comuns do Oracle
ERROS_ORACLE = {
    "ORA-00001": "Já existe um registro com esse valor (ex.: e-mail repetido).",
    "ORA-01400": "Um campo obrigatório ficou vazio.",
    "ORA-02291": "O registro relacionado informado não existe (verifique o ID).",
    "ORA-02292": "O registro possui registros relacionados em outra tabela.",
    "ORA-12541": "Não foi possível conectar ao Oracle: nenhum listener no endereço "
                 "configurado. Verifique se o banco está ligado e se o endereço "
                 "(ORACLE_HOST) está correto.",
    "ORA-12514": "Não foi possível conectar ao Oracle: serviço do banco não encontrado.",
    "ORA-01017": "Usuário ou senha do Oracle inválidos "
                 "(src/conexion/passphrase/authentication.oracle).",
    "DPI-1047": "Oracle Instant Client não encontrado nesta máquina.",
}


def mensagem_erro(erro: Exception) -> str:
    texto = str(erro)
    for codigo, mensagem in ERROS_ORACLE.items():
        if codigo in texto:
            return f"{mensagem} [{codigo}]"
    return f"Não foi possível realizar a operação: {texto}"


def confirmar(pergunta: str) -> bool:
    """Pergunta Sim/Não até o usuário responder s ou n."""
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda com S (sim) ou N (não).")


def ler_id(mensagem: str):
    """Lê um ID numérico. Devolve None se o valor digitado for inválido."""
    valor = input(mensagem).strip()
    if not valor.isdigit() or int(valor) <= 0:
        print("\nInforme um ID numérico válido.")
        return None
    return int(valor)


def ler_texto(rotulo: str, atual=None) -> str:
    """Lê um texto. Na atualização, ENTER vazio mantém o valor atual."""
    if atual is None:
        return input(f"{rotulo}: ").strip()
    valor = input(f"{rotulo} [{atual}]: ").strip()
    return valor if valor else str(atual)


def executar_operacao(operacao, pergunta_repetir: str):
    """
    Executa uma operação (inserir, remover ou atualizar) e pergunta se o
    usuário deseja repeti-la na mesma entidade (edital 6.b.5, 6.c.6, 6.d.8).
    Se a operação devolver False (o usuário cancelou a confirmação),
    volta direto ao menu principal (edital 6.c.5).
    """
    while True:
        try:
            if operacao() is False:
                return
        except ValueError as erro:
            print(f"\nDados inválidos: {erro}")
        except Exception as erro:
            print("\n" + mensagem_erro(erro))

        if not confirmar(f"\n{pergunta_repetir} (s/n): "):
            return
