
class Instrutor:
    def __init__(self, id_instrutor, nome_instrutor, email_instrutor,
                 telefone_instrutor):
        self.id_instrutor = id_instrutor
        self.nome_instrutor = nome_instrutor
        self.email_instrutor = email_instrutor
        self.telefone_instrutor = telefone_instrutor

    # Consultar os atributos
    def get_id_instrutor(self):
        return self.id_instrutor

    def get_nome_instrutor(self):
        return self.nome_instrutor

    def get_email_instrutor(self):
        return self.email_instrutor

    def get_telefone_instrutor(self):
        return self.telefone_instrutor

    # Alterar os atributos
    def set_id_instrutor(self, id_instrutor):
        self.id_instrutor = id_instrutor

    def set_nome_instrutor(self, nome_instrutor):
        self.nome_instrutor = nome_instrutor

    def set_email_instrutor(self, email_instrutor):
        self.email_instrutor = email_instrutor

    def set_telefone_instrutor(self, telefone_instrutor):
        self.telefone_instrutor = telefone_instrutor

    # Exibir as informacoes do instrutor
    def to_string(self):
        return (
            f"ID: {self.id_instrutor} | "
            f"Nome: {self.nome_instrutor} | "
            f"Email: {self.email_instrutor} | "
            f"Telefone: {self.telefone_instrutor}"
        )
