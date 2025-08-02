from abc import ABC, abstractmethod
from datetime import datetime


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def saldo_conta(self):
        return self._saldo

    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False

        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False

        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado.")
        return True

    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico

    @property
    def saldo(self):
        return self._saldo


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False

        if valor > self.limite:
            print("Valor excede o limite por saque.")
            return False

        if super().sacar(valor):
            self.numero_saques += 1
            return True

        return False


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print("Conta não pertence ao cliente.")

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


def localizar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


def exibir_extrato(conta):
    print("\n--------- EXTRATO ---------")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['tipo']} de R$ {transacao['valor']:.2f} em {transacao['data']}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("----------------------------\n")

    
# PROGRAMA PRINCIPAL


clientes = []
contas = []

def main():
    while True:
        opcao = input("""
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """).lower()

        if opcao == "d":
            cpf = input("CPF do cliente: ").replace(".", "").replace("-", "")
            cliente = localizar_cliente(cpf, clientes)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            valor = float(input("Valor do depósito: "))
            conta = cliente.contas[-1]
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF do cliente: ").replace(".", "").replace("-", "")
            cliente = localizar_cliente(cpf, clientes)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            valor = float(input("Valor do saque: "))
            conta = cliente.contas[-1]
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            cpf = input("CPF do cliente: ").replace(".", "").replace("-", "")
            cliente = localizar_cliente(cpf, clientes)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrada.")
                continue

            conta = cliente.contas[-1]
            exibir_extrato(conta)

        elif opcao == "nu":
            cpf = input("Informe o CPF (somente números): ").replace(".", "").replace("-", "")
            if localizar_cliente(cpf, clientes):
                print("Já existe um cliente com esse CPF.")
                continue

            nome = input("Nome completo: ")
            nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")

            cliente = PessoaFisica(nome, cpf, nascimento, endereco)
            clientes.append(cliente)
            print("Usuário criado com sucesso.")

        elif opcao == "nc":
            cpf = input("Informe o CPF do cliente: ").replace(".", "").replace("-", "")
            cliente = localizar_cliente(cpf, clientes)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            numero = len(contas) + 1
            conta = ContaCorrente(numero, cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print(f"Conta criada com sucesso. Número: {numero}")

        elif opcao == "lc":
            for conta in contas:
                print("="*30)
                print(f"Agência: {conta.agencia}")
                print(f"Conta: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")
                print("="*30)

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
