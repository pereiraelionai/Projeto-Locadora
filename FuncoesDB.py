import sqlite3


class BancoDados:
    def __init__(self):
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()

    def salvar_db(self, nome, cpf, endereco, email, telefone):
        texto = 'INSERT OR IGNORE INTO Cliente (Nome, CPF, Endereço, Email, Telefone) VALUES (?, ?, ?, ?, ?)'
        self.cursor.execute(texto, (nome, cpf, endereco, email, telefone))
        self.conexao.commit()

    def salvar_veiculo_db(self, modelo, marca, ano, placa, alugado, batido, kmatual, valordiaria, descricao, tipo):
        texto = 'INSERT OR IGNORE INTO Veiculo (Modelo, Marca, AnoModelo, Placa, Alugado, Batido, KmAtual, ' \
                'ValorDIaria, Descricao, TipoVeiculo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(texto, (modelo, marca, ano, placa, alugado, batido, kmatual, valordiaria, descricao, tipo,))
        self.conexao.commit()

    def salvar_aluguel_db(self, dataaluguel, dataprazo, valoraluguel, kmsaida, nomecliente, codveic, nomeveic):
        texto = 'INSERT OR IGNORE INTO Aluguel (DataAluguel, DataPrazo, ValorAluguel, KmSaída, NomeCliente, ' \
                'CodVeiculo, NomeVeiculo) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(texto, (dataaluguel, dataprazo, valoraluguel, kmsaida, nomecliente, codveic, nomeveic))
        self.conexao.commit()

    def salvar_dev_db(self, devolucao, multa, kmentrada, codAluguel):
        texto = 'UPDATE OR IGNORE Aluguel SET DataDevolucao=?, ValorMulta=?, KmEntrada=? WHERE CodigoAlug=?'
        self.cursor.execute(texto, (devolucao, multa, kmentrada, codAluguel))
        self.conexao.commit()


if __name__ == '__main__':
    teste = BancoDados()
