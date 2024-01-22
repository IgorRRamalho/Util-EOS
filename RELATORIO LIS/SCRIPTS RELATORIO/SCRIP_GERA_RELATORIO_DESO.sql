SELECT C.ANO_MES_LEITURA "REFERÊNCIA", C.ID_CICLO CICLO, C.ROTA, C.PAGINA, TRUNC(C.DATA_LEITURA) DATA_LEITURA, C.MATRICULA, 
       '9-Enviado para simultanea' AS MODO_FAT, 
       Case C.ID_CONF when 0 then '0-Leitura nao Coletada'
                    when 1 then '1-Leitura nao Informada' 
                    when 2 then '2-Leitura Fora da Faixa nao confirmada'
                    when 3 then '3-Leitura Normal'    
                    when 4 then '4-Leitura Fora de Faixa Confirmada'   
                    when 5 then '5-Leitura Retificada Dentro da Faixa' 
                    when 6 then '6-Leitura Retificada Fora de Faixa' 
                    when 9 then '9-Nao Medido'
                    ELSE 'DESCONHECIDO'
       end ID_CONF,       
       CASE C.SIT_AGUA WHEN 1 THEN 'ATIVO' WHEN 2 THEN 'CORTADO POR DEBITO' WHEN 3 THEN 'CORTADO A PEDIDO' WHEN 4 THEN 'SUPRIMIDO' WHEN 5 THEN 'FACTIVEL' WHEN 6 THEN 'POTENCIAL' WHEN 9 THEN 'EXCLUIDO' ELSE 'DESCONHECIDO' END SITUACAO_AGUA,
       CASE C.SIT_ESGOTO WHEN 1 THEN 'ATIVO' WHEN 2 THEN 'CORTADO POR DEBITO' WHEN 3 THEN 'CORTADO A PEDIDO' WHEN 4 THEN 'SUPRIMIDO' WHEN 5 THEN 'FACTIVEL' WHEN 6 THEN 'POTENCIAL' WHEN 9 THEN 'EXCLUIDO' ELSE 'DESCONHECIDO' END SITUACAO_ESGOTO,
       CA.INDICEA, 
       Case CA.SITUACAO when 0 then '0-Gerado'
                    when 1 then '1-Exportado' 
                    when 2 then '2-Importado'
                    when 3 then '3-Processado com sucesso'    
                    when 4 then '4-Programado'   
                    when 5 then '5-Processado com erro'
                    ELSE 'DESCONHECIDO'
       end SITUACAO_CA       
  FROM PRD_DESO_NETUNO.CONSUMO C
  LEFT JOIN PRD_DESO_NETUNO.CONTROLE_ARQUIVO CA ON CA.ANO_MES = C.ANO_MES_LEITURA AND CA.ID_CICLO = C.ID_CICLO AND CA.ROTA = C.ROTA AND CA.PAGINA = C.PAGINA 
 WHERE C.MODO_FAT='9' AND 
       C.ANO_MES_LEITURA>='202312' AND
       (C.SIT_AGUA<4 OR C.SIT_ESGOTO=1) AND
       TRUNC(C.DATA_LEITURA) < TRUNC(SYSDATE) AND 
       C.PAGINA>0
 ORDER BY C.ANO_MES_LEITURA DESC, C.ID_CICLO, C.ROTA, C.PAGINA;
