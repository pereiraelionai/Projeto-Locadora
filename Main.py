# Main do app
import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PROJETO.FuncoesDB import BancoDados
from View_Projeto.MainPrincipal import Principal
from View_Projeto.Cadastrar_Cliente import CadCliente
from View_Projeto.Pesquisar_Cliente import PeqCliente
from View_Projeto.Cadastro_Veiculo import CadVeiculo
from View_Projeto.Pesquisar_Veiculo import PeqVeiculo
from View_Projeto.Aluguel_Veiculos import CadAluguel
from View_Projeto.Pesquisar_Aluguel import PeqAluguel


class Main(QMainWindow, Principal):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnCadastrarCliente.clicked.connect(self.exibir_cadastro)
        self.btnListarClientes.clicked.connect(self.exibir_clientes)
        self.btnCadastrarVeiculo.clicked.connect(self.exibi_cad_veiculos)
        self.btnListarVeiculos.clicked.connect(self.exibir_lista_veiculos)
        self.btnAlugarVeiculo.clicked.connect(self.exibir_alugar)
        self.btnListarAlugueis.clicked.connect(self.exibir_alugueis)


    def exibir_cadastro(self):
        self.janela_exibir = Cliente(self)
        self.janela_exibir.show()

    def exibir_clientes(self):
        self.janela_pesquisa = TelaLista(self)
        self.janela_pesquisa.show()

    def exibi_cad_veiculos(self):
        self.janela_cad_veiculo = Veiculo(self)
        self.janela_cad_veiculo.show()

    def exibir_lista_veiculos(self):
        self.janela_veiculos = ListaVeiculo(self)
        self.janela_veiculos.show()
        self.janela_veiculos.mostrar_veiculos()

    def exibir_alugar(self):
        self.janela_alugar = Alugar(self)
        self.janela_alugar.show()
        self.janela_alugar.mostra_veiculo()
        self.janela_alugar.mostra_cliente()

    def exibir_alugueis(self):
        self.janela_alugueis = ListaAluguel(self)
        self.janela_alugueis.exibir_lista_alugueis()
        self.janela_alugueis.show()


class Cliente(QMainWindow, CadCliente, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.nome = None
        self.cpf = None
        self.telefone = None
        self.email = None
        self.endereco = None
        self.btnSalvar.clicked.connect(self.salvar)

    def salvar(self):
        self.nome = self.inputNome.text().title().strip()
        self.cpf = self.inputCPF.text().title().strip()
        self.telefone = self.inputTelefone.text().title().strip()
        self.endereco = self.inputEndereco.text().title().strip()
        self.email = self.inputEmail.text().strip()
        self.salvar_db(self.nome, self.cpf, self.endereco, self.email, self.telefone)
        self.nome = self.inputNome.setText('')
        self.cpf = self.inputCPF.setText('')
        self.telefone = self.inputTelefone.setText('')
        self.endereco = self.inputEndereco.setText('')
        self.email = self.inputEmail.setText('')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Cliente Cadastrado com Sucesso')
        msg.setWindowTitle('Cadastrar Cliente')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def alterar_nome(self, valor):
        self.inputNome.setText(valor)


class Veiculo(QMainWindow, CadVeiculo, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.modelo = None
        self.marca = None
        self.placa = None
        self.tipo_veiculo = None
        self.kmatual = None
        self.valodiaria = None
        self.ano = None
        self.alugado = None
        self.batido = None
        self.descricao = None
        self.btnSalvar.clicked.connect(self.salvar_veiculo)

    def salvar_veiculo(self):
        self.modelo = self.inputModelo.text().title().strip()
        self.marca = self.inputMarca.text().strip()
        self.placa = self.inputPlaca.text().upper().strip()
        self.tipo_veiculo = self.inputVeiculo.text().title().strip()
        self.kmatual = self.inputKmAtual.text().strip()
        self.valodiaria = self.inputValorDiaria.text().strip()
        self.ano = self.inputAno.text()
        self.descricao = self.inputDescricao.toPlainText()
        if self.rbAlugado.isChecked():
            self.alugado = self.rbAlugado.text()
        elif self.rbDisponivel.isChecked():
            self.alugado = self.rbDisponivel.text()
        if self.rbBatido.isChecked():
            self.batido = self.rbBatido.text()
        elif self.rbPerfeitoEstado.isChecked():
            self.batido = self.rbPerfeitoEstado.text()
        self.salvar_veiculo_db(self.modelo, self.marca, self.ano, self.placa, self.alugado, self.batido, self.kmatual,
                               self.valodiaria, self.descricao, self.tipo_veiculo)
        self.inputModelo.setText('')
        self.inputMarca.setText('')
        self.inputPlaca.setText('')
        self.inputVeiculo.setText('')
        self.inputKmAtual.setText('')
        self.inputValorDiaria.setText('')
        self.inputAno.setText('')
        self.inputDescricao.setText('')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Veículo cadastrado com sucesso!')
        msg.setWindowTitle('Cadastrar Veículo')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class Alugar(QMainWindow, CadAluguel, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.btnSalvar.clicked.connect(self.cli_atual)
        self.btnSalvar.clicked.connect(self.vei_atual)
        self.btnSalvar.clicked.connect(self.veic_atual)
        self.btnSalvar.clicked.connect(self.status_veiculo)
        self.btnSalvar.clicked.connect(self.cadastrar_aluguel)
        self.btnPesquisar.clicked.connect(self.pesquisar_cliente)
        self.btnPesquisar_2.clicked.connect(self.pesquisa_veiculo)
        self.dataaluguel = None
        self.dataprazo = None
        self.datadevolucao = None
        self.valoraluguel = None
        self.valormulta = None
        self.kmentrada = None
        self.kmsaida = None
        self.codcliente = None
        self.codveiculo = None

    def cadastrar_aluguel(self):
        self.dataaluguel = self.inputDataAluguel.text().strip()
        self.dataprazo = self.inputPrazodeEntrega.text().strip()
        self.valoraluguel = self.inputValorAluguel.text().strip()
        self.kmsaida = self.inputKMSaida.text().strip()
        self.salvar_aluguel_db(self.dataaluguel, self.dataprazo, self.valoraluguel, self.kmsaida,
                               self.nomecliente, self.nomeveiculo, self.nomeveiculonome)
        self.inputDataAluguel.setText('')
        self.inputPrazodeEntrega.setText('')
        self.inputValorAluguel.setText('')
        self.inputKMSaida.setText('')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Aluguel cadastrado com sucesso!')
        msg.setWindowTitle('Aluguel de Veículo')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def status_veiculo(self):
        teste = AlteraVeiculo()
        teste.rbAlugado.setChecked(True)
        status = teste.rbAlugado.text()
        texto = 'UPDATE OR IGNORE Veiculo SET Alugado=? WHERE CodVeiculo=?'
        self.cursor.execute(texto, (status, self.nomeveiculo))

    def veic_atual(self):
        linha = self.tabelaVeiculo.currentItem().row()
        self.nomeveiculonome = self.tabelaVeiculo.item(linha, 1).text()

    def cli_atual(self):
        linha = self.tabelaCliente.currentItem().row()
        self.nomecliente = self.tabelaCliente.item(linha, 1).text()

    def vei_atual(self):
        linha = self.tabelaVeiculo.currentItem().row()
        self.nomeveiculo = self.tabelaVeiculo.item(linha, 0).text()

    def mostra_cliente(self):
        texto = 'SELECT * FROM Cliente'
        self.cursor.execute(texto)
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            self.nome = linha[1]
            cpf = linha[2]
            endereco = linha[3]
            email = linha[4]
            telefone = linha[5]
            self.tabelaCliente.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            nome = QTableWidgetItem(self.nome)
            cpf = QTableWidgetItem(cpf)
            endereco = QTableWidgetItem(endereco)
            email = QTableWidgetItem(email)
            telefone = QTableWidgetItem(telefone)
            self.tabelaCliente.setItem(row, 0, cod)
            self.tabelaCliente.setItem(row, 1, nome)
            self.tabelaCliente.setItem(row, 2, cpf)
            self.tabelaCliente.setItem(row, 3, endereco)
            self.tabelaCliente.setItem(row, 4, email)
            self.tabelaCliente.setItem(row, 5, telefone)
            row += 1

    def mostra_veiculo(self):
        texto = 'SELECT * FROM Veiculo'
        self.cursor.execute(texto)
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            modelo = linha[1]
            marca = linha[2]
            ano = linha[3]
            placa = linha[4]
            kmatual = linha[5]
            alugado = linha[6]
            batido = linha[7]
            valordiaria = linha[8]
            tipoveic = linha[9]
            descricao = linha[10]
            if kmatual == 'Não': # Deu algum problema aqui
                self.tabelaVeiculo.insertRow(row)
                cod = QTableWidgetItem(str(cod))
                modelo = QTableWidgetItem(modelo)
                marca = QTableWidgetItem(marca)
                ano = QTableWidgetItem(str(ano))
                placa = QTableWidgetItem(placa)
                kmatual = QTableWidgetItem(kmatual)
                alugado = QTableWidgetItem(str(alugado))
                batido = QTableWidgetItem(str(batido))
                valordiaria = QTableWidgetItem(str(valordiaria))
                tipoveic = QTableWidgetItem(tipoveic)
                descricao = QTableWidgetItem(descricao)
                self.tabelaVeiculo.setItem(row, 0, cod)
                self.tabelaVeiculo.setItem(row, 1, modelo)
                self.tabelaVeiculo.setItem(row, 2, marca)
                self.tabelaVeiculo.setItem(row, 3, ano)
                self.tabelaVeiculo.setItem(row, 4, placa)
                self.tabelaVeiculo.setItem(row, 5, kmatual)
                self.tabelaVeiculo.setItem(row, 6, alugado)
                self.tabelaVeiculo.setItem(row, 7, batido)
                self.tabelaVeiculo.setItem(row, 8, valordiaria)
                self.tabelaVeiculo.setItem(row, 9, descricao)
                self.tabelaVeiculo.setItem(row, 10, tipoveic)
                row += 1

    def exec_pesquisa_cliente(self, texto, nome):
        self.cursor.execute(texto, (f'%{nome}%',))
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            nome = linha[1]
            cpf = linha[2]
            endereco = linha[3]
            email = linha[4]
            telefone = linha[5]
            self.tabelaCliente.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            nome = QTableWidgetItem(nome)
            cpf = QTableWidgetItem(cpf)
            endereco = QTableWidgetItem(endereco)
            email = QTableWidgetItem(email)
            telefone = QTableWidgetItem(telefone)
            self.tabelaCliente.setItem(row, 0, cod)
            self.tabelaCliente.setItem(row, 1, nome)
            self.tabelaCliente.setItem(row, 2, cpf)
            self.tabelaCliente.setItem(row, 3, endereco)
            self.tabelaCliente.setItem(row, 4, email)
            self.tabelaCliente.setItem(row, 5, telefone)
            row += 1

    def pesquisar_cliente(self):
        atributo = self.tipoPesquisa.currentText()
        if atributo == 'Nome':
            texto = 'SELECT * FROM Cliente WHERE Nome LIKE ?'
            nome = self.inputTipoPesquisa.text().title().strip()
            self.exec_pesquisa_cliente(texto, nome)
            self.inputTipoPesquisa.setText('')
        elif atributo == 'CPF':
            texto = 'SELECT * FROM Cliente WHERE CPF LIKE ?'
            nome = self.inputTipoPesquisa.text().strip()
            self.exec_pesquisa_cliente(texto, nome)
            self.inputTipoPesquisa.setText('')
        elif atributo == 'Código':
            texto = 'SELECT * FROM Cliente WHERE CodCliente LIKE ?'
            nome = self.inputTipoPesquisa.text().strip()
            self.exec_pesquisa_cliente(texto, nome)
            self.inputTipoPesquisa.setText('')

    def exec_pesquisa_veiculo(self, texto, nome):
        self.cursor.execute(texto, (f'%{nome}%',))
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            modelo = linha[1]
            marca = linha[2]
            ano = linha[3]
            placa = linha[4]
            kmatual = linha[5]
            alugado = linha[6]
            batido = linha[7]
            valordiaria = linha[8]
            tipoveic = linha[9]
            descricao = linha[10]
            self.tabelaVeiculo.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            modelo = QTableWidgetItem(modelo)
            marca = QTableWidgetItem(marca)
            ano = QTableWidgetItem(str(ano))
            placa = QTableWidgetItem(placa)
            kmatual = QTableWidgetItem(kmatual)
            alugado = QTableWidgetItem(str(alugado))
            batido = QTableWidgetItem(str(batido))
            valordiaria = QTableWidgetItem(str(valordiaria))
            tipoveic = QTableWidgetItem(tipoveic)
            descricao = QTableWidgetItem(descricao)
            self.tabelaVeiculo.setItem(row, 0, cod)
            self.tabelaVeiculo.setItem(row, 1, modelo)
            self.tabelaVeiculo.setItem(row, 2, marca)
            self.tabelaVeiculo.setItem(row, 3, ano)
            self.tabelaVeiculo.setItem(row, 4, placa)
            self.tabelaVeiculo.setItem(row, 5, kmatual)
            self.tabelaVeiculo.setItem(row, 6, alugado)
            self.tabelaVeiculo.setItem(row, 7, batido)
            self.tabelaVeiculo.setItem(row, 8, valordiaria)
            self.tabelaVeiculo.setItem(row, 9, descricao)
            self.tabelaVeiculo.setItem(row, 10, tipoveic)
            row += 1

    def pesquisa_veiculo(self):
        atributo = self.tipoPesquisaVeiculo.currentText()
        if atributo == 'Código':
            nome = self.inputPesquisaVeiculo.text()
            texto = 'SELECT * FROM Veiculo WHERE CodVeiculo LIKE ?'
            self.exec_pesquisa_veiculo(texto, nome)
            self.inputPesquisaVeiculo.setText('')
        elif atributo == 'Marca':
            nome = self.inputPesquisaVeiculo.text()
            texto = 'SELECT * FROM Veiculo WHERE Marca LIKE ?'
            self.exec_pesquisa_veiculo(texto, nome)
            self.inputPesquisaVeiculo.setText('')
        elif atributo == 'Modelo':
            nome = self.inputPesquisaVeiculo.text()
            texto = 'SELECT * FROM Veiculo WHERE Modelo LIKE ?'
            self.exec_pesquisa_veiculo(texto, nome)
            self.inputPesquisaVeiculo.setText('')
        elif atributo in 'AlugadoDisponível':
            nome = self.inputPesquisaVeiculo.text()
            texto = 'SELECT * FROM Veiculo WHERE Alugado LIKE ?'
            self.exec_pesquisa_veiculo(texto, nome)
            self.inputPesquisaVeiculo.setText('')


class AlteraCliente(QMainWindow, CadCliente, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.codigo = None
        self.new_nome = None
        self.new_cpf = None
        self.new_telefone = None
        self.new_email = None
        self.new_endereco = None

    def alterar(self):
        self.new_nome = self.inputNome.text().title().strip()
        self.new_cpf = self.inputCPF.text().title().strip()
        self.new_telefone = self.inputTelefone.text().title().strip()
        self.new_email = self.inputEmail.text().strip()
        self.new_endereco = self.inputEndereco.text().strip()
        texto = 'UPDATE OR IGNORE Cliente SET Nome=?, CPF=?, Endereço=?, Email=?, Telefone=? WHERE CodCliente=?'
        self.cursor.execute(texto, (self.new_nome, self.new_cpf, self.new_endereco, self.new_email, self.new_telefone, self.codigo))
        self.conexao.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Cliente Alterado com Sucesso')
        msg.setWindowTitle('Alterar Cliente')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class AlteraVeiculo(QMainWindow, CadVeiculo, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.btnSalvar.clicked.connect(self.alterar_veic)
        self.codigo = None
        self.new_modelo = None
        self.new_marca = None
        self.new_placa = None
        self.new_tipo_veiculo = None
        self.new_kmatual = None
        self.new_valodiaria = None
        self.new_ano = None
        self.new_alugado = None
        self.new_batido = None
        self.new_descricao = None

    def alterar_veic(self):
        self.new_modelo = self.inputModelo.text().title().strip()
        self.new_marca = self.inputMarca.text().strip()
        self.new_placa = self.inputPlaca.text().upper().strip()
        self.new_tipo_veiculo = self.inputVeiculo.text().title().strip()
        self.new_kmatual = self.inputKmAtual.text().strip()
        self.new_valodiaria = self.inputValorDiaria.text().strip()
        self.new_ano = self.inputAno.text().strip()
        self.new_descricao = self.inputDescricao.toPlainText().title().strip()
        if self.rbAlugado.isChecked():
            self.new_alugado = self.rbAlugado.text()
        elif self.rbDisponivel.isChecked():
            self.new_alugado = self.rbDisponivel.text()
        if self.rbBatido.isChecked():
            self.new_batido = self.rbBatido.text()
        elif self.rbPerfeitoEstado.isChecked():
            self.new_batido = self.rbPerfeitoEstado.text()
        texto = 'UPDATE OR IGNORE Veiculo SET Modelo=?, Marca=?, AnoModelo=?, Placa=?, Alugado=?, Batido=?, KmAtual=?, ' \
                'ValorDIaria=?, Descricao=?, TipoVeiculo=? WHERE CodVeiculo=?'
        self.cursor.execute(texto, (self.new_modelo, self.new_marca, self.new_ano, self.new_placa, self.new_alugado,
                                    self.new_batido, self.new_kmatual, self.new_valodiaria, self.new_descricao,
                                    self.new_tipo_veiculo, self.codigo))
        self.conexao.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Veiculo alterado com sucesso!')
        msg.setWindowTitle('Alterar Veiculo')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class TelaLista(QMainWindow, PeqCliente, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnAlterar.clicked.connect(self.alterar_cliente)
        self.btnExcluir.clicked.connect(self.excluir_cliente)
        self.btnPesquisar.clicked.connect(self.pesquisar)
        self.pushButton.clicked.connect(self.pesquisar)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        texto = 'SELECT * FROM Cliente'
        self.cursor.execute(texto)
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            nome = linha[1]
            cpf = linha[2]
            endereco = linha[3]
            email = linha[4]
            telefone = linha[5]
            self.TabelaPesquisa.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            nome = QTableWidgetItem(nome)
            cpf = QTableWidgetItem(cpf)
            endereco = QTableWidgetItem(endereco)
            email = QTableWidgetItem(email)
            telefone = QTableWidgetItem(telefone)
            self.TabelaPesquisa.setItem(row, 0, cod)
            self.TabelaPesquisa.setItem(row, 1, nome)
            self.TabelaPesquisa.setItem(row, 2, cpf)
            self.TabelaPesquisa.setItem(row, 3, endereco)
            self.TabelaPesquisa.setItem(row, 4, email)
            self.TabelaPesquisa.setItem(row, 5, telefone)
            row += 1


    def alterar_cliente(self):
        linha = self.TabelaPesquisa.currentItem().row()
        self.cod = self.TabelaPesquisa.item(linha, 0).text()
        nome = self.TabelaPesquisa.item(linha, 1).text()
        cpf = self.TabelaPesquisa.item(linha, 2).text()
        endereco = self.TabelaPesquisa.item(linha, 3).text()
        email = self.TabelaPesquisa.item(linha, 4).text()
        telefone = self.TabelaPesquisa.item(linha, 5).text()
        self.mostra = AlteraCliente(self)
        self.mostra.codigo = self.cod
        self.mostra.inputNome.setText(nome)
        self.mostra.inputCPF.setText(cpf)
        self.mostra.inputEndereco.setText(endereco)
        self.mostra.inputEmail.setText(email)
        self.mostra.inputTelefone.setText(telefone)
        self.mostra.btnSalvar.clicked.connect(self.mostra.alterar)
        self.mostra.show()

    def excluir_cliente(self):
        linha = self.TabelaPesquisa.currentItem().row()
        cod = self.TabelaPesquisa.item(linha, 0).text()
        self.cursor.execute('DELETE FROM Cliente WHERE CodCliente=?', (cod,))
        self.conexao.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Cliente Excluído com Sucesso')
        msg.setWindowTitle('Excluir Cliente')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def exec_pesquisa(self, texto, nome):
        self.cursor.execute(texto, (f'%{nome}%',))
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            nome = linha[1]
            cpf = linha[2]
            endereco = linha[3]
            email = linha[4]
            telefone = linha[5]
            self.TabelaPesquisa.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            nome = QTableWidgetItem(nome)
            cpf = QTableWidgetItem(cpf)
            endereco = QTableWidgetItem(endereco)
            email = QTableWidgetItem(email)
            telefone = QTableWidgetItem(telefone)
            self.TabelaPesquisa.setItem(row, 0, cod)
            self.TabelaPesquisa.setItem(row, 1, nome)
            self.TabelaPesquisa.setItem(row, 2, cpf)
            self.TabelaPesquisa.setItem(row, 3, endereco)
            self.TabelaPesquisa.setItem(row, 4, email)
            self.TabelaPesquisa.setItem(row, 5, telefone)
            row += 1

    def pesquisar(self):
        atributo = self.ItemPesquisa.currentText().title().strip()
        if atributo == 'Nome':
            texto = 'SELECT * FROM Cliente WHERE Nome LIKE ?'
            nome = self.inputClientePesquisa.text()
            self.exec_pesquisa(texto, nome)
            self.inputClientePesquisa.setText('')
        elif atributo == 'CPF':
            texto = 'SELECT * FROM Cliente WHERE CPF LIKE ?'
            nome = self.inputClientePesquisa.text().title().strip()
            self.exec_pesquisa(texto, nome)
            self.inputClientePesquisa.setText('')
        elif atributo == 'Código':
            texto = 'SELECT * FROM Cliente WHERE CodCliente LIKE ?'
            nome = self.inputClientePesquisa.text().strip()
            self.exec_pesquisa(texto, nome)
            self.inputClientePesquisa.setText('')


class ListaVeiculo(QMainWindow, PeqVeiculo, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()
        self.btnAlterar.clicked.connect(self.alterar_veiculo)
        self.btnExcluir.clicked.connect(self.excluir_veiculo)
        self.btnPesquisar.clicked.connect(self.pesquisar_veiculo)
        self.btnAtualizar.clicked.connect(self.pesquisar_veiculo)

    def mostrar_veiculos(self):
        texto = 'SELECT * FROM Veiculo'
        self.cursor.execute(texto)
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            modelo = linha[1]
            marca = linha[2]
            ano = linha[3]
            placa = linha[4]
            kmatual = linha[5]
            alugado = linha[6]
            batido = linha[7]
            valordiaria = linha[8]
            tipoveic = linha[9]
            descricao = linha[10]
            self.tabelaVeiculos.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            modelo = QTableWidgetItem(modelo)
            marca = QTableWidgetItem(marca)
            ano = QTableWidgetItem(str(ano))
            placa = QTableWidgetItem(placa)
            kmatual = QTableWidgetItem(kmatual)
            alugado = QTableWidgetItem(str(alugado))
            batido = QTableWidgetItem(str(batido))
            valordiaria = QTableWidgetItem(str(valordiaria))
            tipoveic = QTableWidgetItem(tipoveic)
            descricao = QTableWidgetItem(descricao)
            self.tabelaVeiculos.setItem(row, 0, cod)
            self.tabelaVeiculos.setItem(row, 1, modelo)
            self.tabelaVeiculos.setItem(row, 2, marca)
            self.tabelaVeiculos.setItem(row, 3, ano)
            self.tabelaVeiculos.setItem(row, 4, placa)
            self.tabelaVeiculos.setItem(row, 5, kmatual)
            self.tabelaVeiculos.setItem(row, 6, alugado)
            self.tabelaVeiculos.setItem(row, 7, batido)
            self.tabelaVeiculos.setItem(row, 8, valordiaria)
            self.tabelaVeiculos.setItem(row, 9, descricao)
            self.tabelaVeiculos.setItem(row, 10, tipoveic)
            row += 1

    def alterar_veiculo(self):
        linha = self.tabelaVeiculos.currentItem().row()
        self.cod = self.tabelaVeiculos.item(linha, 0).text()
        modelo = self.tabelaVeiculos.item(linha, 1).text()
        marca = self.tabelaVeiculos.item(linha, 2).text()
        ano = self.tabelaVeiculos.item(linha, 3).text()
        placa = self.tabelaVeiculos.item(linha, 4).text()
        alugado = self.tabelaVeiculos.item(linha, 5).text()
        batido = self.tabelaVeiculos.item(linha, 6).text()
        kmatual = self.tabelaVeiculos.item(linha, 7).text()
        valordiaria = self.tabelaVeiculos.item(linha, 8).text()
        tipoveic = self.tabelaVeiculos.item(linha, 9).text()
        descricao = self.tabelaVeiculos.item(linha, 10).text()
        self.veiculo = AlteraVeiculo(self)
        self.veiculo.codigo = self.cod
        self.veiculo.inputModelo.setText(modelo)
        self.veiculo.inputMarca.setText(marca)
        self.veiculo.inputAno.setText(ano)
        self.veiculo.inputPlaca.setText(placa)
        self.veiculo.inputKmAtual.setText(kmatual)
        self.veiculo.inputValorDiaria.setText(valordiaria)
        self.veiculo.inputVeiculo.setText(tipoveic)
        self.veiculo.inputDescricao.setText(descricao)
        if alugado == 'Sim':
            self.veiculo.rbAlugado.setChecked(True)
            self.veiculo.rbDisponivel.setChecked(False)
        elif alugado == 'Não':
            self.veiculo.rbAlugado.setChecked(False)
            self.veiculo.rbDisponivel.setChecked(True)
        if batido == 'Sim':
            self.veiculo.rbBatido.setChecked(True)
            self.veiculo.rbPerfeitoEstado.setChecked(False)
        elif batido == 'Não':
            self.veiculo.rbBatido.setChecked(False)
            self.veiculo.rbPerfeitoEstado.setChecked(True)
        self.veiculo.show()

    def pesq_veiculo(self, texto, nome):
        self.cursor.execute(texto, (f'%{nome}%',))
        row = 0
        for linha in self.cursor.fetchall():
            cod = linha[0]
            modelo = linha[1]
            marca = linha[2]
            ano = linha[3]
            placa = linha[4]
            kmatual = linha[5]
            alugado = linha[6]
            batido = linha[7]
            valordiaria = linha[8]
            tipoveic = linha[9]
            descricao = linha[10]
            self.tabelaVeiculos.insertRow(row)
            cod = QTableWidgetItem(str(cod))
            modelo = QTableWidgetItem(modelo)
            marca = QTableWidgetItem(marca)
            ano = QTableWidgetItem(str(ano))
            placa = QTableWidgetItem(placa)
            kmatual = QTableWidgetItem(kmatual)
            alugado = QTableWidgetItem(str(alugado))
            batido = QTableWidgetItem(str(batido))
            valordiaria = QTableWidgetItem(str(valordiaria))
            tipoveic = QTableWidgetItem(tipoveic)
            descricao = QTableWidgetItem(descricao)
            self.tabelaVeiculos.setItem(row, 0, cod)
            self.tabelaVeiculos.setItem(row, 1, modelo)
            self.tabelaVeiculos.setItem(row, 2, marca)
            self.tabelaVeiculos.setItem(row, 3, ano)
            self.tabelaVeiculos.setItem(row, 4, placa)
            self.tabelaVeiculos.setItem(row, 5, kmatual)
            self.tabelaVeiculos.setItem(row, 6, alugado)
            self.tabelaVeiculos.setItem(row, 7, batido)
            self.tabelaVeiculos.setItem(row, 8, valordiaria)
            self.tabelaVeiculos.setItem(row, 9, descricao)
            self.tabelaVeiculos.setItem(row, 10, tipoveic)
            row += 1

    def pesquisar_veiculo(self):
        atributo = self.listaCodigo.currentText()
        if atributo == 'Código':
            nome = self.inputTipoCodigo.text()
            texto = 'SELECT * FROM Veiculo WHERE CodVeiculo LIKE ?'
            self.pesq_veiculo(texto, nome)
            self.inputTipoCodigo.setText('')
        elif atributo == 'Marca':
            nome = self.inputTipoCodigo.text()
            texto = 'SELECT * FROM Veiculo WHERE Marca LIKE ?'
            self.pesq_veiculo(texto, nome)
            self.inputTipoCodigo.setText('')
        elif atributo == 'Modelo':
            nome = self.inputTipoCodigo.text()
            texto = 'SELECT * FROM Veiculo WHERE Modelo LIKE ?'
            self.pesq_veiculo(texto, nome)
            self.inputTipoCodigo.setText('')
        elif atributo in 'AlugadoDisponível':
            nome = self.inputTipoCodigo.text()
            texto = 'SELECT * FROM Veiculo WHERE Alugado LIKE ?'
            self.pesq_veiculo(texto, nome)
            self.inputTipoCodigo.setText('')

    def excluir_veiculo(self):
        linha = self.tabelaVeiculos.currentItem().row()
        cod = self.tabelaVeiculos.item(linha, 0).text()
        self.cursor.execute('DELETE FROM Veiculo WHERE CodVeiculo=?', (cod,))
        self.conexao.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Veículo excluído com sucesso!')
        msg.setWindowTitle('Excluir Veículo')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class ListaAluguel(QMainWindow, PeqAluguel, BancoDados):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.datadevucao = None
        self.multa = None
        self.kmentrada = None
        self.btnPesquisar.clicked.connect(self.pesquisar_locado)
        self.btnAtualizar.clicked.connect(self.pesquisar_locado)
        self.btnDevolver.clicked.connect(self.devolucao)
        self.btnDevolver.clicked.connect(self.devolvendo)
        self.conexao = sqlite3.connect('RentCar.db')
        self.cursor = self.conexao.cursor()

    def exibir_lista_alugueis(self):
        texto = 'SELECT * FROM Aluguel'
        self.cursor.execute(texto)
        row = 0
        for linha in self.cursor.fetchall():
            codaluguel = linha[0]
            dataaluguel = linha[1]
            dataprazo = linha[2]
            datadevolucao = linha[3]
            valoraluguel = linha[4]
            valormulta = linha[5]
            kmentrada = linha[6]
            kmsaida = linha[7]
            nomecliente = linha[8]
            codveiculo = linha[9]
            nomeveiculo = linha[10]
            self.tabelaAlugueis.insertRow(row)
            codaluguel = QTableWidgetItem(str(codaluguel))
            dataaluguel = QTableWidgetItem(str(dataaluguel))
            dataprazo = QTableWidgetItem(str(dataprazo))
            datadevolucao = QTableWidgetItem(str(datadevolucao))
            valoraluguel = QTableWidgetItem(str(valoraluguel))
            valormulta = QTableWidgetItem(str(valormulta))
            kmentrada = QTableWidgetItem(str(kmentrada))
            kmsaida = QTableWidgetItem(str(kmsaida))
            nomecliente = QTableWidgetItem(nomecliente)
            nomeveiculo = QTableWidgetItem(nomeveiculo)
            codveiculo = QTableWidgetItem(str(codveiculo))
            self.tabelaAlugueis.setItem(row, 0, codaluguel)
            self.tabelaAlugueis.setItem(row, 1, nomecliente)
            self.tabelaAlugueis.setItem(row, 2, nomeveiculo)
            self.tabelaAlugueis.setItem(row, 3, dataaluguel)
            self.tabelaAlugueis.setItem(row, 4, dataprazo)
            self.tabelaAlugueis.setItem(row, 5, datadevolucao)
            self.tabelaAlugueis.setItem(row, 6, valoraluguel)
            self.tabelaAlugueis.setItem(row, 7, valormulta)
            self.tabelaAlugueis.setItem(row, 8, kmentrada)
            self.tabelaAlugueis.setItem(row, 9, kmsaida)
            self.tabelaAlugueis.setItem(row, 10, codveiculo)
            row += 1

    def exec_pesquisa_locado(self, texto, nome):
        self.cursor.execute(texto, (f'%{nome}%',))
        row = 0
        for linha in self.cursor.fetchall():
            codaluguel = linha[0]
            dataaluguel = linha[1]
            dataprazo = linha[2]
            datadevolucao = linha[3]
            valoraluguel = linha[4]
            valormulta = linha[5]
            kmentrada = linha[6]
            kmsaida = linha[7]
            nomecliente = linha[8]
            codveiculo = linha[9]
            nomeveiculo = linha[10]
            self.tabelaAlugueis.insertRow(row)
            codaluguel = QTableWidgetItem(str(codaluguel))
            dataaluguel = QTableWidgetItem(str(dataaluguel))
            dataprazo = QTableWidgetItem(str(dataprazo))
            datadevolucao = QTableWidgetItem(str(datadevolucao))
            valoraluguel = QTableWidgetItem(str(valoraluguel))
            valormulta = QTableWidgetItem(str(valormulta))
            kmentrada = QTableWidgetItem(str(kmentrada))
            kmsaida = QTableWidgetItem(str(kmsaida))
            nomecliente = QTableWidgetItem(nomecliente)
            nomeveiculo = QTableWidgetItem(nomeveiculo)
            codveiculo = QTableWidgetItem(str(codveiculo))
            self.tabelaAlugueis.setItem(row, 0, codaluguel)
            self.tabelaAlugueis.setItem(row, 1, nomecliente)
            self.tabelaAlugueis.setItem(row, 2, nomeveiculo)
            self.tabelaAlugueis.setItem(row, 3, dataaluguel)
            self.tabelaAlugueis.setItem(row, 4, dataprazo)
            self.tabelaAlugueis.setItem(row, 5, datadevolucao)
            self.tabelaAlugueis.setItem(row, 6, valoraluguel)
            self.tabelaAlugueis.setItem(row, 7, valormulta)
            self.tabelaAlugueis.setItem(row, 8, kmentrada)
            self.tabelaAlugueis.setItem(row, 9, kmsaida)
            self.tabelaAlugueis.setItem(row, 10, codveiculo)
            row += 1

    def pesquisar_locado(self):
        atributo = self.tipoPesquisa.currentText()
        if atributo == 'Código Aluguel':
            nome = self.inputTipoPesquisa.text()
            texto = 'SELECT * FROM Aluguel WHERE CodigoAlug LIKE ?'
            self.exec_pesquisa_locado(texto, nome)
            self.inputTipoPesquisa.setText('')
        elif atributo == 'Nome Cliente':
            nome = self.inputTipoPesquisa.text()
            texto = 'SELECT * FROM Aluguel WHERE NomeCliente LIKE ?'
            self.exec_pesquisa_locado(texto, nome)
            self.inputTipoPesquisa.setText('')

    def devolucao(self):
        linha = self.tabelaAlugueis.currentItem().row()
        codlocacao = self.tabelaAlugueis.item(linha, 0).text()
        self.codveicu = self.tabelaAlugueis.item(linha, 10).text()
        self.datadevucao = self.inputDataDevolucao.text().strip()
        self.multa = self.inputMulta.text().strip()
        self.kmentrada = self.inputKmEntrada.text().strip()
        self.salvar_dev_db(self.datadevucao, self.multa, self.kmentrada, codlocacao)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Veículo devolvido com sucesso!')
        msg.setWindowTitle('Devolução Veículo')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def devolvendo(self):
        new_km = self.inputKmEntrada.text()
        texto = 'UPDATE OR IGNORE Veiculo SET Alugado=? WHERE CodVeiculo=?'
        self.cursor.execute(texto, ('Não', self.codveicu))
        self.conexao.commit()
        texto = 'UPDATE OR IGNORE Veiculo SET KmAtual=? WHERE CodVeiculo=?'
        self.cursor.execute(texto, (new_km, self.codveicu))
        self.conexao.commit()


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = Main()
    app.show()
    qt.exec_()
