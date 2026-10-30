
class Aluno:
    def __init__(self, id_aluno, nome_aluno, email_aluno,
                 telefone_aluno, data_nascimento, genero):
        self.id_aluno = id_aluno
        self.nome_aluno = nome_aluno
        self.email_aluno = email_aluno
        self.telefone_aluno = telefone_aluno
        self.data_nascimento = data_nascimento
        self.genero = genero

    # Consultar os atributos
    def get_id_aluno(self):
        return self.id_aluno

    def get_nome_aluno(self):
        return self.nome_aluno

    def get_email_aluno(self):
        return self.email_aluno

    def get_telefone_aluno(self):
        return self.telefone_aluno

    def get_data_nascimento(self):
        return self.data_nascimento

    def get_genero(self):
        return self.genero

    # Alterar os atributos
    def set_id_aluno(self, id_aluno):
        self.id_aluno = id_aluno

    def set_nome_aluno(self, nome_aluno):
        self.nome_aluno = nome_aluno

    def set_email_aluno(self, email_aluno):
        self.email_aluno = email_aluno

    def set_telefone_aluno(self, telefone_aluno):
        self.telefone_aluno = telefone_aluno

    def set_data_nascimento(self, data_nascimento):
        self.data_nascimento = data_nascimento

    def set_genero(self, genero):
        self.genero = genero

    # Exibir as informacoes do aluno
    def to_string(self):
        nascimento = self.data_nascimento
        if hasattr(nascimento, "strftime"):
            nascimento = nascimento.strftime("%d/%m/%Y")
        return (
            f"ID: {self.id_aluno} | "
            f"Nome: {self.nome_aluno} | "
            f"Email: {self.email_aluno} | "
            f"Telefone: {self.telefone_aluno} | "
            f"Nascimento: {nascimento} | "
            f"Genero: {self.genero}"
        )
