
class Frequencia:
    def __init__(self, id_frequencia, aluno, data_hora_entrada):
        self.id_frequencia = id_frequencia
        self.aluno = aluno                      # objeto Aluno, nao so o ID
        self.data_hora_entrada = data_hora_entrada

    # Consultar os atributos
    def get_id_frequencia(self):
        return self.id_frequencia

    def get_aluno(self):
        return self.aluno

    def get_data_hora_entrada(self):
        return self.data_hora_entrada

    # Alterar os atributos
    def set_id_frequencia(self, id_frequencia):
        self.id_frequencia = id_frequencia

    def set_aluno(self, aluno):
        self.aluno = aluno

    def set_data_hora_entrada(self, data_hora_entrada):
        self.data_hora_entrada = data_hora_entrada

    # Exibir as informacoes da frequencia
    def to_string(self):
        data_hora = self.data_hora_entrada
        if hasattr(data_hora, "strftime"):
            data_hora = data_hora.strftime("%d/%m/%Y %H:%M")
        return (
            f"ID: {self.id_frequencia} | "
            f"Aluno: {self.aluno.get_nome_aluno()} | "
            f"Entrada: {data_hora}"
        )
