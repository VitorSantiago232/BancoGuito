import json
import time

debito_automatico_ativo = False

try:
    with open('dados_banco.json', 'r') as arquivo:
        clientes = json.load(arquivo)
except FileNotFoundError:
    clientes = []

def novo_cliente():
    razao_social = input("Digite a razão social do cliente: ")
    cnpj = input("Digite o CNPJ do cliente: ")
    tipo_conta = input("Digite o tipo de conta (comum ou plus): ")
    valor_inicial = float(input("Digite o valor inicial da conta: "))
    senha = input("Digite a senha do usuário: ")

    cliente = {
        "razao_social": razao_social,
        "cnpj": cnpj,
        "tipo_conta": tipo_conta,
        "saldo": valor_inicial,
        "senha": senha,
        "extrato": []
    }
    clientes.append(cliente)

    print("Cliente criado com sucesso!")

    with open('dados_banco.json', 'w') as arquivo:
        json.dump(clientes, arquivo)

def apaga_cliente():
    cnpj = input("Digite o CNPJ do cliente a ser apagado: ")

    for cliente in clientes:
        if cliente["cnpj"] == cnpj:
            clientes.remove(cliente)
            print(f"Cliente com CNPJ {cnpj} apagado com sucesso.")

            with open('dados_banco.json', 'w') as arquivo:
                json.dump(clientes, arquivo)
            return

    print(f"Cliente com CNPJ {cnpj} não encontrado.")

def listar_clientes():
    if len(clientes) == 0:
        print("Não há clientes cadastrados.")
    else:
        for cliente in clientes:
            print(f"Razão Social: {cliente['razao_social']}")
            print(f"CNPJ: {cliente['cnpj']}")
            print(f"Tipo de Conta: {cliente['tipo_conta']}")
            print(f"Saldo: R${cliente['saldo']:.2f}")
            print("-----")

def debito():
    cnpj = input("Digite o CNPJ do cliente: ")
    senha = input("Digite a senha do usuário: ")
    valor = float(input("Digite o valor a ser debitado: "))

    cliente = encontrar_cliente_por_cnpj(cnpj)

    if cliente is not None and cliente["senha"] == senha:
        if valor > 0:
            if cliente["tipo_conta"] == "comum" and cliente["saldo"] - valor >= -1000.00:
                taxa = valor * 0.05
                cliente["saldo"] -= (valor + taxa)
                descricao_transacao = f"Débito de R${valor:.2f} realizado com taxa de R${taxa:.2f}"
                cliente["extrato"].append(descricao_transacao)
                print(descricao_transacao)
            elif cliente["tipo_conta"] == "plus" and cliente["saldo"] - valor >= -5000.00:
                taxa = valor * 0.03
                cliente["saldo"] -= (valor + taxa)
                descricao_transacao = f"Débito de R${valor:.2f} realizado com taxa de R${taxa:.2f}"
                cliente["extrato"].append(descricao_transacao)
                print(descricao_transacao)
            else:
                print("Saldo insuficiente para realizar o débito.")
        else:
            print("Valor de débito inválido.")
    else:
        print("CNPJ ou senha incorretos.")

    with open('dados_banco.json', 'w') as arquivo:
        json.dump(clientes, arquivo)

def deposito():
    cnpj = input("Digite o CNPJ do cliente: ")
    valor = float(input("Digite o valor a ser depositado: "))

    cliente = encontrar_cliente_por_cnpj(cnpj)

    if cliente is not None:
        if valor > 0:
            cliente["saldo"] += valor
            descricao_transacao = f"Depósito de R${valor:.2f} realizado"
            cliente["extrato"].append(descricao_transacao)
            print(descricao_transacao)
        else:
            print("Valor de depósito inválido.")
    else:
        print("CNPJ não encontrado.")

    with open('dados_banco.json', 'w') as arquivo:
        json.dump(clientes, arquivo)

def transferencia():
    cnpj_origem = input("Digite o CNPJ da conta de origem: ")
    senha_origem = input("Digite a senha da conta de origem: ")
    cnpj_destino = input("Digite o CNPJ da conta de destino: ")
    valor = float(input("Digite o valor a ser transferido: "))

    conta_origem = encontrar_cliente_por_cnpj(cnpj_origem)
    conta_destino = encontrar_cliente_por_cnpj(cnpj_destino)

    if conta_origem is not None and conta_origem["senha"] == senha_origem:
        if conta_destino is not None:
            if valor > 0 and conta_origem["saldo"] >= valor:
                if conta_origem["tipo_conta"] == "comum" and conta_origem["saldo"] - valor >= -1000.00:
                    conta_origem["saldo"] -= valor
                    conta_destino["saldo"] += valor
                    descricao_transacao_origem = f"Transferência para CNPJ {cnpj_destino} de R${valor:.2f}"
                    descricao_transacao_destino = f"Transferência de CNPJ {cnpj_origem} de R${valor:.2f}"
                    conta_origem["extrato"].append(descricao_transacao_origem)
                    conta_destino["extrato"].append(descricao_transacao_destino)
                    print(f"Transferência de R${valor:.2f} realizada com sucesso.")
                elif conta_origem["tipo_conta"] == "plus" and conta_origem["saldo"] - valor >= -5000.00:
                    conta_origem["saldo"] -= valor
                    conta_destino["saldo"] += valor
                    descricao_transacao_origem = f"Transferência para CNPJ {cnpj_destino} de R${valor:.2f}"
                    descricao_transacao_destino = f"Transferência de CNPJ {cnpj_origem} de R${valor:.2f}"
                    conta_origem["extrato"].append(descricao_transacao_origem)
                    conta_destino["extrato"].append(descricao_transacao_destino)
                    print(f"Transferência de R${valor:.2f} realizada com sucesso.")
                else:
                    print("Saldo insuficiente para realizar a transferência.")
            else:
                print("Valor de transferência inválido.")
        else:
            print("CNPJ de destino não encontrado.")
    else:
        print("CNPJ ou senha de origem incorretos.")

    with open('dados_banco.json', 'w') as arquivo:
        json.dump(clientes, arquivo)

def extrato():
    cnpj = input("Digite o CNPJ do cliente: ")
    senha = input("Digite a senha: ")

    cliente = encontrar_cliente_por_cnpj(cnpj)

    if cliente is not None and cliente["senha"] == senha:
        print(f"Extrato do cliente com CNPJ {cnpj}:")

        for transacao in cliente["extrato"]:
            print(transacao)
    else:
        print("CNPJ ou senha incorretos.")

def encontrar_cliente_por_cnpj(cnpj):
    for cliente in clientes:
        if cliente["cnpj"] == cnpj:
            return cliente
    return None

def ativar_debito_automatico():
    global debito_automatico_ativo
    debito_automatico_ativo = True

    cnpj = input("Digite o CNPJ do cliente:")
    cliente = encontrar_cliente_por_cnpj(cnpj)

    if cliente is not None:
        valor_debito = float(input("Digite o valor do débito automático:"))
        if valor_debito > 0:
            tempo_debito = int(input("Digite a duração do débito automático em segundos:"))
            if cliente["saldo"] - valor_debito >= 0:
                while debito_automatico_ativo and tempo_debito > 0:
                    time.sleep(1)
                    cliente["saldo"] -= valor_debito
                    descricao_transacao = f"Débito automático de R${valor_debito:.2f} realizado"
                    cliente["extrato"].append(descricao_transacao)
                    print(descricao_transacao)
                    tempo_debito -= 1
                debito_automatico_ativo = False

                with open('dados_banco.json', 'w') as arquivo:
                    json.dump(clientes, arquivo)
            else:
                print("Saldo insuficiente para realizar o débito automático.")
        else:
            print("Valor de débito automático inválido.")
    else:
        print("CNPJ não encontrado.")

def menu():
    print("Bem-vindo ao banco Guito!")
    while True:
        print("\nMenu de Opções:")
        print("1. Novo cliente")
        print("2. Apaga cliente")
        print("3. Listar clientes")
        print("4. Débito")
        print("5. Depósito")
        print("6. Extrato")
        print("7. Transferência entre contas")
        print("8. Ativar Débito Automático")
        print("9. Sair")

        opcao = input("Digite o número da opção desejada:")

        if opcao == '1':
            novo_cliente()
        elif opcao == '2':
            apaga_cliente()
        elif opcao == '3':
            listar_clientes()
        elif opcao == '4':
            debito()
        elif opcao == '5':
            deposito()
        elif opcao == '6':
            extrato()
        elif opcao == '7':
            transferencia()
        elif opcao == '8':
            ativar_debito_automatico()
        elif opcao == '9':
            print("Obrigado por utilizar os serviços do banco Guito.")
            sair()
        else:
            print("Opção inválida. Tente novamente.")

def sair():
    exit()

menu()
