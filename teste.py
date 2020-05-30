import sqlite3


class TesteBanco:
    def __init__(self, arquivo):
        self.conexao = sqlite3.connect(arquivo)
        self.cursor = self.conexao.cursor()

    def atualizar(self, nome, cpf, endereco, email, telefone):
        texto = 'UPDATE OR IGNORE Cliente SET Nome=?, CPF=?, Endereço=?, Email=?, Telefone=? WHERE CodCliente'
