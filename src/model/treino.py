
from datetime import datetime


class Treino:
    def __init__(self, id_treino, aluno, instrutor,
                 nome_treino, objetivo=None, data_criacao=None):
        self.id_treino = id_treino
        self.aluno = aluno
        self.instrutor = instrutor
        self.nome_treino = nome_treino
        self.objetivo = objetivo
        self.data_criacao = (
            data_criacao if data_criacao is not None
            else datetime.now()
        )

    # Metodos para consultar os atributos
    def get_id_treino(self):
        return self.id_treino

    def get_aluno(self):
        return self.aluno

    def get_instrutor(self):
        return self.instrutor

    def get_nome_treino(self):
        return self.nome_treino

    def get_objetivo(self):
        return self.objetivo

    def get_data_criacao(self):
        return self.data_criacao

    # Metodos para alterar os atributos
    def set_id_treino(self, id_treino):
        self.id_treino = id_treino

    def set_aluno(self, aluno):
        self.aluno = aluno

    def set_instrutor(self, instrutor):
        self.instrutor = instrutor

    def set_nome_treino(self, nome_treino):
        self.nome_treino = nome_treino

    def set_objetivo(self, objetivo):
        self.objetivo = objetivo

    def set_data_criacao(self, data_criacao):
        self.data_criacao = data_criacao

    # Exibir informacoes do treino
    def to_string(self):
        return (
            f"ID: {self.id_treino} | "
            f"Aluno: {self.aluno.get_nome_aluno()} | "
            f"Instrutor: {self.instrutor.get_nome_instrutor()} | "
            f"Treino: {self.nome_treino} | "
            f"Objetivo: {self.objetivo} | "
            f"Data de criacao: {self.data_criacao}"
        )
