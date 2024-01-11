import pyperclip
import os

def limpar_tela():
    os.system('cls')  # Para sistemas Windows

def recalculo_rateio(matricula):
    limpar_tela()
    try:
        # Pedindo o número de meses para recálculo
        num_meses = int(input("Digite o número de meses para recálculo: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        return

    # Lista para armazenar as referências de cada mês
    referencias = []

    # Pedindo as referências para cada mês
    for i in range(num_meses):
        referencia = input(f"Digite a referência para o mês {i + 1}: ")
        referencias.append(referencia.strip())

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
    limpar_tela()
    print("Script SQL de Recálculo de Rateio gerado com sucesso. Consulte o arquivo RECALCULO_RATEIO.sql.")


def update_consumo(matricula):
    limpar_tela()
    try:
        # Pedindo o número de meses para update
        num_meses = int(input("Digite o número de meses para update: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        return

    # Lista para armazenar as referências de cada mês
    referencias = []

    # Pedindo as referências para cada mês
    for i in range(num_meses):
        referencia = input(f"Digite a referência para o mês {i + 1}: ")
        referencias.append(referencia.strip())

    # Perguntando ao usuário se as duas referências terão as mesmas colunas modificadas
    resposta_same_columns = 'N'  # Padrão para não perguntar se há apenas uma referência
    if num_meses > 1:
        resposta_same_columns = input("As referências terão as mesmas colunas modificadas? (S/N): ").upper()
        

    # Lista de colunas disponíveis para atualização
    colunas_disponiveis = ['confat', 'medconmed', 'media_consumo_faturado', 'credito_consumo', 'leitura', 'credito_utilizado', 'conmed']

    # Dicionário para armazenar os valores escolhidos pelo usuário
    colunas_valores = {}
    limpar_tela()
    if resposta_same_columns == 'S':
        # Se as referências tiverem as mesmas colunas modificadas, pergunte uma vez e use para todas
        print("\nEscolha as colunas a serem atualizadas:")
        for i, coluna in enumerate(colunas_disponiveis, start=1):
            print(f"{i}. {coluna}")

        resposta = input("Digite os números das colunas desejadas separados por vírgula (ou '0' para finalizar): ")

        if resposta == '0':
            return

        escolhas = resposta.split(',')
        escolhas_validas = all(escolha.isdigit() and 1 <= int(escolha) <= len(colunas_disponiveis) for escolha in escolhas)

        if not escolhas_validas:
            print("Escolha inválida. Digite os números correspondentes às colunas desejadas separados por vírgula.")
            return

        for referencia in referencias:
            limpar_tela()
            colunas_valores[referencia] = {}
            for escolha in escolhas:
                coluna_escolhida = colunas_disponiveis[int(escolha) - 1]
                valor = input(f"Digite o valor para a coluna {coluna_escolhida} na referência {referencia}: ")
                colunas_valores[referencia][coluna_escolhida] = valor.strip()
    else:
        # Se as referências tiverem colunas diferentes, pergunte para cada referência
        for referencia in referencias:
            limpar_tela()
            colunas_valores[referencia] = {}
            print(f"\nEscolha as colunas a serem atualizadas para a referência {referencia}:")
            for i, coluna in enumerate(colunas_disponiveis, start=1):
                print(f"{i}. {coluna}")

            resposta = input("Digite os números das colunas desejadas separados por vírgula (ou '0' para finalizar): ")
            limpar_tela()

            if resposta == '0':
                continue

            escolhas = resposta.split(',')
            escolhas_validas = all(escolha.isdigit() and 1 <= int(escolha) <= len(colunas_disponiveis) for escolha in escolhas)

            if escolhas_validas:
                for escolha in escolhas:
                    coluna_escolhida = colunas_disponiveis[int(escolha) - 1]
                    valor = input(f"Digite o valor para a coluna {coluna_escolhida} na referência {referencia}: ")
                    colunas_valores[referencia][coluna_escolhida] = valor.strip()
            else:
                print("Escolha inválida. Digite os números correspondentes às colunas desejadas separados por vírgula.")

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

    limpar_tela()
    print("Script SQL de Update Consumo gerado com sucesso. Consulte o arquivo UPDATE_CONSUMO.sql.")


def copiar_select_conta(matricula, referencia):  
    select_conta = f"""SELECT C.SEQ_ORIGINAL, C.DATA_FAT, C.DATA_VENC, C.LOCALIZACAO, C.ID_CICLO, C.ID_DATA,
                                   C.LOCALIDADE, C.DATA_VENC_ORIGINAL, C.ID_CONTRATO, C.VL_DO_MES 
                            FROM CONTA C
                          WHERE C.MATRICULA = '{matricula}'
                            AND C.ANO_MES_CT = '{referencia}'; """
    pyperclip.copy(select_conta)
    limpar_tela()
    print("SELECT DE CONTA COPIADO COM SUCESSO")


def gerar_conta(matricula):
    limpar_tela()
    try:
       # Pedindo os dados necessários para a geração de conta
        print("\n===================================")
        referencia = input("| Digite a referência da conta: ")
        copiar_select_conta(matricula, referencia)

        valor_conta = input("| Digite o Valor da Conta: ").strip()
        seq_original = input("| Digite o Seq Original: ").strip()
        seq_imp = input("| Digite o Número do Chamado: ").strip()
        data_fatura = input("| Digite a Data Fatura (DD/MM/RR): ").strip()
        data_vencimento = input("| Digite a Data Vencimento (DD/MM/RR): ").strip()
        localizacao = input("| Digite a LOCALIZACAO: ").strip()
        ciclo = input("| Digite o Ciclo: ").strip()
        id_data = input("| Digite o ID_DATA: ").strip()
        localidade = input("| Digite a Localidade: ").strip()
        data_vencimento_original = input("| Digite a Data Vencimento Original (DD/MM/RR): ").strip()
        contrato = input("| Digite o Contrato: ").strip()

        print("\n===================================")
        print("GERAÇÃO DE RETIFICAÇÃO INFOS")
        print("===================================")
        # Geração de Retificação
        valor_cance = input("| Digite o valor cancelado: ").strip()
        print("===================================")


    except ValueError:
        print("Por favor, insira valores válidos.")
        return

    # Gerando o script SQL para Geração de Conta
    script_sql_conta = f"""
--SDES-{seq_imp} ||  CANCELA E INSERE CONTA, PARCELA E RETIFICACAO POS RECALCULO DE RATEIO REF. {referencia}

DECLARE

  V_SIGLA  VARCHAR2(20) := '';
  V_EXISTE INTEGER;

BEGIN

  --VALIDACAO EMPRESA
  SELECT SIGLA INTO V_SIGLA FROM EMPRESA WHERE ID_EMPRESA = '0001';
  IF V_SIGLA = 'DESO' THEN

----------------------------CANCELA CONTA {referencia}-----------------------------
    
    --VERIFICA SITUACAO DA CONTA = 0 OU PAGA COM VALOR 0
    V_EXISTE := 0;
    SELECT COUNT(*)
      INTO V_EXISTE
      FROM CONTA C
     WHERE (C.SITUACAO_CT = 0 AND C.SEQ_ORIGINAL = {seq_original})
        OR (C.SITUACAO_CT IN (1, 2, 3) AND C.VL_DO_MES = 0.00 AND
           C.SEQ_ORIGINAL = {seq_original});
  
    IF V_EXISTE = 1 THEN
      UPDATE CONTA C
         SET C.SITUACAO_CT = 9,
             C.DATA_CANC   = SYSDATE
       WHERE C.SEQ_ORIGINAL =  {seq_original}
         AND C.MATRICULA = '{matricula}'
         AND C.ANO_MES_CT = '{referencia}';
      COMMIT;
     

 --------------------------------CANCELA PARCELA {referencia} --------------------
     V_EXISTE := 0;
    SELECT COUNT(*)
        INTO V_EXISTE
    FROM PARCELA P
    WHERE P.SIT_PARCELA = 11
    AND P.SEQ_ORIGINAL = {seq_original};

    IF V_EXISTE = 0 THEN
        UPDATE PARCELA P
            SET P.SIT_PARCELA = 11,
            P.DATA_BAIXA  = SYSDATE
        WHERE P.SEQ_ORIGINAL = {seq_original}
        AND P.MATRICULA = '{matricula}'
        AND P.ANO_MES_PARCELA = '{referencia}'
        AND P.SIT_PARCELA = 1;
  
        COMMIT;
    END IF;
-------------------------INSERINDO A CONTA NOVA {referencia}--------------------------
      
    V_EXISTE := 0;
    SELECT COUNT(*)
    INTO V_EXISTE
        FROM CONTA C
    WHERE C.SEQ_IMP = {seq_imp}
    AND C.MATRICULA = '{matricula}'
    AND C.ANO_MES_CT = '{referencia}';
    
    IF V_EXISTE = 0 THEN
        INSERT INTO CONTA
            (SEQ_ORIGINAL,
            TIPO_CT,
            MATRICULA,
            LOCALIZACAO,
            ANO_MES_CT,
            ID_CICLO,
            SITUACAO_CT,
            DATA_FAT,
            DATA_VENC,
            TIPO_ENTREGA,
            ID_CENTRALIZADOR,
            QTD_DEBITO,
            QTD_PAG,
            ID_MEN_MES,
            ID_AVISO,
            DATA_CANC,
            PGTO_PRAZO,
            PGTO_FORA,
            ANO_MES_FAT_MULTA,
            VL_AGUA,
            VL_ESGOTO,
            VL_SERVICO,
            VL_COMERC,
            VL_ICMS,
            VL_MULTA,
            VL_ICFRF,
            VL_DESCONTO,
            VL_JURO,
            VL_TERCEIRO,
            VL_CORRECAO_MONET,
            VL_DEVOLUCAO,
            VL_DO_MES,
            DATA_CONTABIL,
            VL_ASEP,
            VL_ISS,
            TIPO_PROC,
            DATA_EMISSAO,
            ID_DATA,
            ID_CONTRATO,
            JUDICE,
            LOCALIDADE,
            VL_RECURSOS_HIDRICOS_AGUA,
            VL_RECURSOS_HIDRICOS_ESG,
            SEQ_IMP,
            DATA_VENC_ORIGINAL,
            NR_TAB,
            VL_DESCONTO_RETIFICADO,
            VL_DESCONTO_RES_SOCIAL,
            VL_DESCONTO_PEQ_COMERCIO,
            VL_ESGOTO_ALTERNATIVO,
            VL_DESCONTO_LIG_ESTIMADA,
            VL_DESCONTO_PP_CONCEDENTE,
            CD_SIT_NEGATIVACAO,
            QTD_IMPRESSAO,
            VL_CB,
            CLASSIF_IMOVEL)
        VALUES
            (SEQ_CONTAS.NEXTVAL,                     --SEQ_ORIGINAL
            0,                                      --TIPO_CT
            '{matricula}',                          --MATRICULA
            '{localizacao}',                        --LOCALIZACAO
            '{referencia}',                             --ANO_MES_CT
            '{ciclo}',                                   --ID_CICLO
            0,                                      --SITUACAO_CT
            TO_DATE('{data_fatura}', 'DD/MM/RR'),      --DATA_FAT
            TO_DATE('{data_vencimento}', 'DD/MM/RR'),      --DATA_VENC
            0,                                    --TIPO_ENTREGA
            NULL,                                 --ID_CENTRALIZADOR
            0,                                    --QTD_DEBITO
            0,                                    --QTD_PAG
            0,                                    --ID_MEN_MES
            0,                                    --ID_AVISO
            NULL,                                 --DATA_CANC
            0,                                    --PGTO_PRAZO
            0,                                    --PGTO_FORA
            000000,                               --ANO_MES_FAT_MULTA
            0,                                    --VL_AGUA
            0,                                    --VL_ESGOTO
            {valor_conta},                                --VL_SERVICO  XXXX
            0,                                    --VL_COMERC
            0,                                    --VL_ICMS
            0,                                    --VL_MULTA
            0,                                    --VL_ICFRF
            0,                                    --VL_DESCONTO
            0,                                    --VL_JURO
            0,                                    --VL_TERCEIRO
            0,                                    --VL_CORRECAO_MONET
            0,                                    --VL_DEVOLUCAO
            {valor_conta},                                --VL_DO_MES XXXXX
            NULL,                                 --DATA_CONTABIL
            0,                                    --VL_ASEP
            0,                                    --VL_ISS
            0,                                    --TIPO_PROC
            SYSDATE,                              --DATA_EMISSAO
            TO_DATE('{id_data}', 'DD/MM/RR'),      --ID_DATA
            {contrato},                              --ID_CONTRATO
            0,                                    --JUDICE
            {localidade},                              --LOCALIDADE
            0,                                    --VL_RECURSOS_HIDRICOS_AGUA
            0,                                    --VL_RECURSOS_HIDRICOS_ESG
            {seq_imp},                                 --SEQ_IMP
            TO_DATE('{data_vencimento_original}', 'DD/MM/RR'),      --DATA_VENC_ORIGINAL
            NULL,                                 --NR_TAB
            0,                                    --VL_DESCONTO_RETIFICADO
            0,                                    --VL_DESCONTO_RES_SOCIAL
            0,                                    --VL_DESCONTO_PEQ_COMERCIO
            0,                                    --VL_ESGOTO_ALTERNATIVO
            0,                                    --VL_DESCONTO_LIG_ESTIMADA
            0,                                    --VL_DESCONTO_PP_CONCEDENTE
            1,                                    --CD_SIT_NEGATIVACAO
            1,                                    --QTD_IMPRESSAO
            {valor_conta},                                --VL_CB   xxxx
            5);                                   --CLASSIF_IMOVEL
        
        COMMIT;
    END IF;

--------------------------------INSERE PARCELA {referencia} --------------------------
 
      V_EXISTE := 0;
      SELECT COUNT(*)
        INTO V_EXISTE
        FROM PARCELA P
       WHERE P.SEQ_EXTRA = {seq_imp}
         AND P.MATRICULA = '{matricula}'
         AND P.ANO_MES_PARCELA = '{referencia}';
    
      IF V_EXISTE = 0 THEN
        INSERT INTO PARCELA
          (ID_FINAN,
           MATRICULA,
           LOCALIZACAO,
           SERVICO,
           TIPO_PARCELA,
           NRO_PARCELA,
           VL_PARCELA,
           VL_JURO,
           VL_PARCELA_ICMS,
           DATA_FATURA,
           SIT_PARCELA,
           ANO_MES_PARCELA,
           SEQ_ORIGINAL,
           DATA_BAIXA,
           DATA_CONTABIL,
           AMORTIZACAO,
           SALDO,
           TIPO_COBRANCA,
           NRO_OS,
           QTD_PARCELA,
           ID_CICLO,
           DATA_ESPERA,
           VL_TOTAL_PARC,
           ANO_MES_FAT,
           VL_ENTRADA,
           DATA_INCLUSAO,
           ID_CONTRATO,
           VL_MULTA_CORRECAO,
           VL_JUROS_CORRECAO,
           SEQ_IMPORTACAO,
           VL_CONTA_RATEIO_AGUA,
           VL_CONTA_RATEIO_ESG,
           VL_CONTA_RATEIO_SERV,
           IDENT_PARC,
           IDENT_EXTRA,
           AUX,
           VL_CONTA_RATEIO_ENCARGOS,
           VL_ENTRADA_ORIGINAL,
           VL_PARCELA_ORIGINAL,
           DATA_AUX,
           SEQ_EXTRA,
           FLAG,
           ID_CENTRALIZADOR)
        VALUES
          (SEQ_FINANCIAMENTOS.NEXTVAL,                  --ID_FINAN
           '{matricula}',                               --MATRICULA             XXX
           '{localizacao}',                             --LOCALIZACAO           XXX
           9032,                                        --SERVICO
           3,                                           --TIPO_PARCELA
           1,                                           --NRO_PARCELA
           {valor_conta},                               --VL_PARCELA            XXX
           0,                                           --VL_JURO
           0,                                           --VL_PARCELA_ICMS
           TO_DATE('{data_fatura}', 'DD/MM/RR'),        --DATA_FATURA           XXX
           1,                                           --SIT_PARCELA
           '{referencia}',                              --ANO_MES_PARCELA       XXX
           NULL,                                        --SEQ_ORIGINAL
           NULL,                                        --DATA_BAIXA
           NULL,                                        --DATA_CONTABIL
           {valor_conta},                               --AMORTIZACAO
           0,                                           --SALDO
           3,                                           --TIPO_COBRANCA
           NULL,                                        --NRO_OS                XXX
           1,                                           --QTD_PARCELA
           {ciclo},                                     --ID_CICLO
           SYSDATE - 1,                                 --DATA_ESPERA
           {valor_conta},                               --VL_TOTAL_PARC         XXX
           {referencia},                                --ANO_MES_FAT           XXX
           0,                                           --VL_ENTRADA
           SYSDATE,                                     --DATA_INCLUSAO	        XXX
           {contrato},                                  --ID_CONTRATO           XXX
           0,                                           --VL_MULTA_CORRECAO
           0,                                           --VL_JUROS_CORRECAO
           NULL,                                        --SEQ_IMPORTACAO
           0,                                           --VL_CONTA_RATEIO_AGUA
           0,                                           --VL_CONTA_RATEIO_ESG
           0,                                           --VL_CONTA_RATEIO_SERV
           NULL,                                        --IDENT_PARC
           NULL,                                        --IDENT_EXTRA
           NULL,                                        --AUX
           0,                                           --VL_CONTA_RATEIO_ENCARGOS
           0,                                           --VL_ENTRADA_ORIGINAL
           {valor_conta},                               --VL_PARCELA_ORIGINAL
           TO_DATE('{data_fatura}', 'DD/MM/RR'),        --DATA_AUX              XXX
           {seq_imp},                                   --SEQ_EXTRA             XXX
           NULL,                                        --FLAG
           NULL);                                       --ID_CENTRALIZADOR
      
        COMMIT;
      END IF;
  
  ---------------------------GERA RETIFICACAO {referencia} -----------------------------
  V_EXISTE := 0;
  SELECT COUNT(*)
    INTO V_EXISTE
    FROM RETIFICACAO R
   WHERE R.SEQ_IMP =  {seq_imp}
     AND R.MATRICULA = '{matricula}'
 AND R.ANO_MES_CT = '{referencia}';

  IF V_EXISTE = 0 THEN
    INSERT INTO RETIFICACAO
      (MATRICULA,
       LOCALIDADE,
       ANO_MES_CT,
       SEQ_ORIGEM_CANC,
       SEQ_ORIGEM_EMIT,
       CONSUMO_PEDIDO,
       CONSUMO_EMIT,
       CONSUMO_CANC,
       VL_CANC,
       VL_EMIT,
       DATA_PEDIDO,
       DATA_TARIFA,
       DATA_EXECUCAO_RETIF,
       MOTIVO_RETIF,
       TIPO_RETIF,
       ID_USUARIO,
       LAUDO_RETIF,
       DATA_CONTABIL,
       LEITURA_CORRIGIDA,
       ID_MOTIVO_RETIFICA,
       SEQ_IMP,
       VL_DESCONTO)
    VALUES 
       ('{matricula}',                          --MATRICULA	   XXX
        '{localidade}',                         --LOCALIDADE          XXX
        '{referencia}',                         --ANO_MES_CT          XXX
        {seq_original},                         --SEQ_ORIGEM_CANC     XXX
        NULL,                                   --SEQ_ORIGEM_EMIT
        386,                                    --CONSUMO_PEDIDO
        386,                                    --CONSUMO_EMIT
        NULL,                                   --CONSUMO_CANC
        {valor_cance},                          --VL_CANC
        {valor_conta},                          --VL_EMIT               XXX
        SYSDATE,                                --DATA_PEDIDO				
        SYSDATE,                                --DATA_TARIFA			 
        SYSDATE,                                --DATA_EXECUCAO_RETIF    
        NULL,                                   --MOTIVO_RETIF
        1,                                      --TIPO_RETIF
        0,                                      --ID_USUARIO
        '{seq_imp}',                            --LAUDO_RETIF       XXX
        NULL,                                   --DATA_CONTABIL
        NULL,                                   --LEITURA_CORRIGIDA
        80,                                     --ID_MOTIVO_RETIFICA
        {seq_imp},                              --SEQ_IMP           XXX
        0);                                     --VL_DESCONTO
      
        COMMIT;
      END IF;
  
-------------------------CAPTURANDO O SEQ_ORIGINAL NOVO -----------------------
  FOR N IN (SELECT C.SEQ_ORIGINAL, C.MATRICULA, C.ANO_MES_CT, C.SEQ_IMP
              FROM CONTA C
             WHERE C.MATRICULA = '{matricula}'
           AND C.SEQ_IMP = {seq_imp}
           AND C.ANO_MES_CT = '{referencia}'
                   AND C.SITUACAO_CT = 0) LOOP
        UPDATE PARCELA P
           SET P.SEQ_ORIGINAL = N.SEQ_ORIGINAL
         WHERE P.MATRICULA = N.MATRICULA
           AND P.ANO_MES_PARCELA = N.ANO_MES_CT
           AND P.SEQ_EXTRA = N.SEQ_IMP;
      
        UPDATE RETIFICACAO R
           SET R.SEQ_ORIGEM_EMIT = N.SEQ_ORIGINAL
         WHERE R.MATRICULA = N.MATRICULA
           AND R.ANO_MES_CT = N.ANO_MES_CT
           AND R.SEQ_IMP = N.SEQ_IMP;
      
        COMMIT;
      END LOOP;
  
      COMMIT;
    END IF;

  END IF;
END;
"""

    # Escrevendo o script SQL no arquivo 'GERACAO_CONTA.sql'
    with open('GERACAO_CONTA.sql', 'w') as file_conta:
        file_conta.write(script_sql_conta)
    limpar_tela()
    print("Script SQL de Geração de Conta gerado com sucesso. Consulte o arquivo GERACAO_CONTA.sql.")


# Solicitando informações ao usuário
matricula = input("Digite sua matrícula: ")
limpar_tela()
# Menu
while True:
    print("\n========== Menu || Mat:" + matricula +" ==========")
    print("1. Recálculo de Rateio")
    print("2. Update Consumo")
    print("3. Gerar Conta e outros")
    print("4. Select Conta")
    print("0. Sair")

    escolha = input("Escolha a opção (0-3): ")

    if escolha == '1':
        recalculo_rateio(matricula)
    elif escolha == '2':
        update_consumo(matricula)
    elif escolha == '3':
        gerar_conta(matricula)
    elif escolha == '4':
        referencia = input("Digite a referencia da conta: ")
        copiar_select_conta(matricula, referencia)
    elif escolha == '0':
        print("Programa encerrado.")
        break
    else:
        limpar_tela()
        print("Opção inválida. Tente novamente.")
