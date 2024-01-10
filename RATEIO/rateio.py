def recalculo_rateio(matricula):
    # Pedindo o número de meses para recálculo
    num_meses = int(input("Digite o número de meses para recálculo: "))

    # Lista para armazenar as referências de cada mês
    referencias = []
    
    # Pedindo as referências para cada mês
    for i in range(num_meses):
        referencia = input(f"Digite a referência para o mês {i + 1}: ")
        referencias.append(referencia)

    # Gerando o script SQL para Recálculo de Rateio
    script_sql_rateio = ""
    for referencia in referencias:
        script_sql_rateio += f"""
------------------------------- Recalculo de Rateio {referencia} -----------------------------
DELETE ligacao_vinculada_consumo
    WHERE
        matricula_pai = '{matricula}'
        AND ano_mes_leitura = '{referencia}';
COMMIT;
p_rateio_fatura('{referencia}', '{matricula}', 0, 0);
COMMIT;
"""

    # Escrevendo o script SQL no arquivo 'RECALCULO_RATEIO.sql'
    with open('RECALCULO_RATEIO.sql', 'w') as file_rateio:
        file_rateio.write(script_sql_rateio)

    print("Script SQL de Recálculo de Rateio gerado com sucesso. Consulte o arquivo RECALCULO_RATEIO.sql.")

def update_consumo(matricula):
    # Pedindo o número de meses para update
    num_meses = int(input("Digite o número de meses para update: "))

    # Lista para armazenar as referências de cada mês
    referencias = []
    
    # Pedindo as referências para cada mês
    for i in range(num_meses):
        referencia = input(f"Digite a referência para o mês {i + 1}: ")
        referencias.append(referencia)

    # Dicionário para armazenar as colunas e valores escolhidos pelo usuário
    colunas_valores = {}
    
    # Pedindo as colunas a serem atualizadas e seus valores para cada mês
    for referencia in referencias:
        colunas_valores[referencia] = {}
        print(f"\nEscolha as colunas a serem atualizadas para a referência {referencia}:")
        for coluna in ['confat', 'medconmed', 'media_consumo_faturado', 'credito_consumo']:
            resposta = input(f"Você deseja atualizar a coluna {coluna}? (S/N): ")
            if resposta.upper() == 'S':
                valor = input(f"Digite o valor para a coluna {coluna}: ")
                colunas_valores[referencia][coluna] = valor

    # Gerando o script SQL para Update Consumo
    script_sql_consumo = ""
    for referencia, valores in colunas_valores.items():
        script_sql_consumo += f"""
------------------------------- Update Consumo {referencia} -----------------------------
UPDATE CONSUMO C
    SET
"""
        for coluna, valor in valores.items():
            script_sql_consumo += f"        {coluna} = {valor},\n"
        # Removendo a última vírgula e quebra de linha
        script_sql_consumo = script_sql_consumo.rstrip(',\n')
        script_sql_consumo += f"""  \n WHERE
        c.matricula = '{matricula}'
        AND c.ano_mes_leitura = '{referencia}';
COMMIT;
"""

    # Escrevendo o script SQL no arquivo 'UPDATE_CONSUMO.sql'
    with open('UPDATE_CONSUMO.sql', 'w') as file_consumo:
        file_consumo.write(script_sql_consumo)

    print("Script SQL de Update Consumo gerado com sucesso. Consulte o arquivo UPDATE_CONSUMO.sql.")

# Solicitando informações ao usuário
matricula = input("Digite sua matrícula: ")

# Menu
while True:
    print("\n==== Menu ====")
    print("1. Recálculo de Rateio")
    print("2. Update Consumo")
    print("0. Sair")

    escolha = input("Escolha a opção (0-2): ")

    if escolha == '1':
        recalculo_rateio(matricula)
    elif escolha == '2':
        update_consumo(matricula)
    elif escolha == '0':
        print("Programa encerrado.")
        break
    else:
        print("Opção inválida. Tente novamente.")
