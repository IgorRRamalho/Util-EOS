/* SDES-4566 || INSERE CONTA, PARCELA E RETIFICACAO POS RECALCULO DE RATEIO REF. 01/2024 | 0006970885 - CONDOMINIO MANSAO VALE DO LUAR.
 				REF. CONTA 01/2024 |SEQ_ORIGINAL 118621189 | VALOR ORGINAL 171562.89 | NOVO VALOR 3213.66	|  REF. RATEIO 11/2023 */

DECLARE

  V_SIGLA  CHAR(20) := '';
  V_EXISTE INTEGER;
 
BEGIN
	
  SELECT SIGLA INTO V_SIGLA FROM EMPRESA WHERE ID_EMPRESA = '0001';

  IF V_SIGLA = 'DESO' THEN
    
    ----------------------------CANCELA CONTA MES 01-----------------------------
    --VERIFICA SITUACAO DA CONTA = 0 OU PAGA COM VALOR 0
    V_EXISTE := 0;
    SELECT COUNT(*)
      INTO V_EXISTE
      FROM CONTA C
     WHERE (C.SITUACAO_CT = 0 AND C.SEQ_ORIGINAL = 118621189)
        OR (C.SITUACAO_CT IN (1, 2, 3) AND C.VL_DO_MES = 0.00 AND
           C.SEQ_ORIGINAL = 118621189);
  
    IF V_EXISTE = 1 THEN
      UPDATE CONTA C
         SET C.SITUACAO_CT = 9,
             C.DATA_CANC   = SYSDATE 
       WHERE C.SEQ_ORIGINAL = 118621189
         AND C.MATRICULA = '0006970885'
         AND C.ANO_MES_CT = '202401';
    
      COMMIT;
    
      --------------------------------CANCELA PARCELA MES 01 --------------------
      V_EXISTE := 0;
      SELECT COUNT(*)
        INTO V_EXISTE
        FROM PARCELA P
       WHERE P.SIT_PARCELA = 11
       	 AND P.SERVICO = 9032
         AND P.SEQ_ORIGINAL = 118621189;
    
      IF V_EXISTE = 0 THEN
        UPDATE PARCELA P
           SET P.SIT_PARCELA = 11,
               P.DATA_BAIXA  = SYSDATE
         WHERE P.SEQ_ORIGINAL = 118621189
           AND P.MATRICULA = '0006970885'
           AND P.ANO_MES_PARCELA = '202401'
           AND P.SERVICO = 9032
           AND P.SIT_PARCELA = 1;
      
        COMMIT;
      END IF;
  
      -------------------------INSERINDO A CONTA NOVA MES 01--------------------------
      V_EXISTE := 0;
      SELECT COUNT(*)
        INTO V_EXISTE
        FROM CONTA C
       WHERE C.SEQ_IMP = 4566
         AND C.MATRICULA = '0006970885'
         AND C.ANO_MES_CT = '202401';
    
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
          (SEQ_CONTAS.NEXTVAL,                   --SEQ_ORIGINAL
           0,                                    --TIPO_CT
           '0006970885',                         --MATRICULA
           '01001020147001100000',               --LOCALIZACAO
           '202401',                             --ANO_MES_CT
           13,                                   --ID_CICLO
           0,                                    --SITUACAO_CT
           TO_DATE('04/01/24', 'DD/MM/RR'),      --DATA_FAT
           TO_DATE('15/02/24', 'DD/MM/RR'),      --DATA_VENC
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
           3213.66,                              --VL_SERVICO
           0,                                    --VL_COMERC
           0,                                    --VL_ICMS
           0,                                    --VL_MULTA
           0,                                    --VL_ICFRF
           0,                                    --VL_DESCONTO
           0,                                    --VL_JURO
           0,                                    --VL_TERCEIRO
           0,                                    --VL_CORRECAO_MONET
           0,                                    --VL_DEVOLUCAO
           3213.66,                              --VL_DO_MES
           NULL,                                 --DATA_CONTABIL
           0,                                    --VL_ASEP
           0,                                    --VL_ISS
           0,                                    --TIPO_PROC
           SYSDATE,						 	     --DATA_EMISSAO
           TO_DATE('01/01/24', 'DD/MM/RR'),      --ID_DATA
           2485293,                              --ID_CONTRATO
           0,                                    --JUDICE
           0100102,                              --LOCALIDADE
           0,                                    --VL_RECURSOS_HIDRICOS_AGUA
           0,                                    --VL_RECURSOS_HIDRICOS_ESG
           4566,                                 --SEQ_IMP
           TO_DATE('05/12/23', 'DD/MM/RR'),      --DATA_VENC_ORIGINAL
           NULL,                                 --NR_TAB
           0,                                    --VL_DESCONTO_RETIFICADO
           0,                                    --VL_DESCONTO_RES_SOCIAL
           0,                                    --VL_DESCONTO_PEQ_COMERCIO
           0,                                    --VL_ESGOTO_ALTERNATIVO
           0,                                    --VL_DESCONTO_LIG_ESTIMADA
           0,                                    --VL_DESCONTO_PP_CONCEDENTE
           1,                                    --CD_SIT_NEGATIVACAO
           1,                                    --QTD_IMPRESSAO
           3213.66,                              --VL_CB
           5);                                   --CLASSIF_IMOVEL
      
       COMMIT;
     END IF;
  
      --------------------------------INSERE PARCELA MES 01 --------------------------
 
      V_EXISTE := 0;
      SELECT COUNT(*)
        INTO V_EXISTE
        FROM PARCELA P
       WHERE P.SEQ_EXTRA = 4566
         AND P.MATRICULA = '0006970885'
         AND P.ANO_MES_PARCELA = '202401';
    
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
          (SEQ_FINANCIAMENTOS.NEXTVAL,        --ID_FINAN
           '0006970885',                      --MATRICULA
           '01001020147001100000',            --LOCALIZACAO
           9032,                              --SERVICO
           3,                                 --TIPO_PARCELA
           1,                                 --NRO_PARCELA
           3213.66,                           --VL_PARCELA
           0,                                 --VL_JURO
           0,                                 --VL_PARCELA_ICMS
           TO_DATE('04/01/24', 'DD/MM/RR'),   --DATA_FATURA
           1,                                 --SIT_PARCELA
           '202401',                          --ANO_MES_PARCELA
           NULL,                              --SEQ_ORIGINAL
           NULL,                              --DATA_BAIXA
           NULL,                              --DATA_CONTABIL
           3213.66,                           --AMORTIZACAO
           0,                                 --SALDO
           3,                                 --TIPO_COBRANCA
           NULL, 	                          --NRO_OS
           1,                                 --QTD_PARCELA
           13,                                --ID_CICLO
           SYSDATE -1,						  --DATA_ESPERA
           3213.66,                           --VL_TOTAL_PARC
           '202401',                          --ANO_MES_FAT
           0,                                 --VL_ENTRADA
           SYSDATE,							  --DATA_INCLUSAO
           2485293,                           --ID_CONTRATO
           0,                                 --VL_MULTA_CORRECAO
           0,                                 --VL_JUROS_CORRECAO
           NULL,                              --SEQ_IMPORTACAO
           0,                                 --VL_CONTA_RATEIO_AGUA
           0,                                 --VL_CONTA_RATEIO_ESG
           0,                                 --VL_CONTA_RATEIO_SERV
           NULL,                              --IDENT_PARC
           NULL,                              --IDENT_EXTRA
           NULL,                              --AUX
           0,                                 --VL_CONTA_RATEIO_ENCARGOS
           0,                                 --VL_ENTRADA_ORIGINAL
           3213.66,                           --VL_PARCELA_ORIGINAL
           TO_DATE('01/01/24', 'DD/MM/RR'),   --DATA_AUX
           4566,                              --SEQ_EXTRA
           NULL,                              --FLAG
           NULL);                             --ID_CENTRALIZADOR
      
        COMMIT;
      END IF;
  
      ---------------------------GERA RETIFICACAO MES 01 -----------------------------
      V_EXISTE := 0;
      SELECT COUNT(*)
        INTO V_EXISTE
        FROM RETIFICACAO R
       WHERE R.SEQ_IMP =  4566
         AND R.MATRICULA = '0006970885'
         AND R.ANO_MES_CT = '202401';
    
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
          ('0006970885',                         --MATRICULA
           '0100102',                            --LOCALIDADE
           '202401',                             --ANO_MES_CT
           118621189,                            --SEQ_ORIGEM_CANC
           NULL,                                 --SEQ_ORIGEM_EMIT
           0,                                    --CONSUMO_PEDIDO
           1264,                                 --CONSUMO_EMIT
           4936,                                 --CONSUMO_CANC
           171562.89,                            --VL_CANC
           3213.66,                              --VL_EMIT
           SYSDATE,  							 --DATA_PEDIDO
           SYSDATE,  							 --DATA_TARIFA
           SYSDATE,								 --DATA_EXECUCAO_RETIF
           NULL,                                 --MOTIVO_RETIF
           1,                                    --TIPO_RETIF
           0,                                    --ID_USUARIO
           '4566',                               --LAUDO_RETIF
           NULL,                                 --DATA_CONTABIL
           NULL,                                 --LEITURA_CORRIGIDA
           80,                                   --ID_MOTIVO_RETIFICA
           4566,                                 --SEQ_IMP
           0);                                   --VL_DESCONTO
      
        COMMIT;
      END IF;
  
      -------------------------CAPTURANDO O SEQ_ORIGINAL NOVO -----------------------
      FOR N IN (SELECT C.SEQ_ORIGINAL, C.MATRICULA, C.ANO_MES_CT, C.SEQ_IMP
                  FROM CONTA C
                 WHERE C.MATRICULA = '0006970885'
                   AND C.SEQ_IMP = 4566
                   AND C.ANO_MES_CT = '202401'
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
  
  
