menu = """

---------- BANCO PYTHON ----------
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f}\n"

        else:
            print("A operação falhou! o valor informado é invalido.")
    
    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor> limite

        excedeu_saques = numero_saques > LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! saldo insuficiente. ")

        elif excedeu_limite:
            print("Operação falhou! o valor do saque excede o limite. ")

        elif excedeu_saques:
            print("Operação falhou! você excedeu o numero máximo de saques")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! o valor informado é invalido.")

    elif opcao == "3":
        print("\n---------- EXTRATO ----------")
        print("Não foram realizados transações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("-----------------------------")

    elif opcao == "0":
        break

    else:
        print("Operação falhou, por favor selecione novamente a operação desejada.")

    


                      



