-------------------------inserindo a conta nova mes 09--------------------------

    INSERT INTO conta
    (seq_original,
        tipo_ct,
        matricula,
        localizacao,
        ano_mes_ct,
        id_ciclo,
        situacao_ct,
        data_fat,
        data_venc,
        tipo_entrega,
        id_centralizador,
        qtd_debito,
        qtd_pag,
        id_men_mes,
        id_aviso,
        data_canc,
        pgto_prazo,
        pgto_fora,
        ano_mes_fat_multa,
        vl_agua,
        vl_esgoto,
        vl_servico,
        vl_comerc,
        vl_icms,
        vl_multa,
        vl_icfrf,
        vl_desconto,
        vl_juro,
        vl_terceiro,
        vl_correcao_monet,
        vl_devolucao,
        vl_do_mes,
        data_contabil,
        vl_asep,
        vl_iss,
        tipo_proc,
        data_emissao,
        id_data,
        id_contrato,
        judice,
        localidade,
        vl_recursos_hidricos_agua,
        vl_recursos_hidricos_esg,
        seq_imp,
        data_venc_original,
        nr_tab,
        vl_desconto_retificado,
        vl_desconto_res_social,
        vl_desconto_peq_comercio,
        vl_esgoto_alternativo,
        vl_desconto_lig_estimada,
        vl_desconto_pp_concedente,
        cd_sit_negativacao,
        qtd_impressao,
        vl_cb,
        classif_imovel)
VALUES      
    (   seq_contas.NEXTVAL,
        '0',
        'XXXXXXXXXX', -- AQUI ENTRARA A MATRICULA RECEBIDA NO COMEÇO DO PROGRAMA
        'XXXXXXXX', -- AQUI DEVE SER RECEBIDO A LOCALIZAÇÃO DO USUARIO
        '202309', -- AQUI DEVE SER RECEBIDA A REFERENCIA DA CONTA NOVA
        '13', -- AQUI DEVE SER RECEBIDO O CICLO 
        '0', 
        To_date('04/09/23', 'DD/MM/RR'), -- AQUI DEVE SER RECEBIDO A DATA DA FATURA
        To_date('12/09/23', 'DD/MM/RR'), -- AQUI DEVE SER RECEBIDO A DATA DE VENCIMENTO
        '0',
        NULL,
        '0',
        '0',
        '22',
        '0',
        NULL,
        '0',
        '0',
        '000000', --  
        '0',
        '0',
        1637.14, -- 
        '0',
        '0',
        '0',
        '0',
        '0',
        '0',
        '0',
        '0',
        '0',
        1637.14,
        NULL,
        '0',
        '0',
        '2',
        To_date('26/09/2023', 'dd/mm/yyyy'), 
        To_date('01/09/23', 'DD/MM/RR'), --
        'XXXX', -- NUMERO DO CHAMADO
        '0',
        '0100102',
        '0',
        '0',
        3662,
        To_date('12/09/23', 'DD/MM/RR'),
        NULL,
        '0',
        '0',
        '0',
        '0',
        '0',
        '0',
        '1',
        '1',
        1637.14,
        '5' );

    COMMIT;

--------------------------------insere parcela mes 09 --------------------------
INSERT INTO parcela
            (id_finan,
             matricula,
             localizacao,
             servico,
             tipo_parcela,
             nro_parcela,
             vl_parcela,
             vl_juro,
             vl_parcela_icms,
             data_fatura,
             sit_parcela,
             ano_mes_parcela,
             seq_original,
             data_baixa,
             data_contabil,
             amortizacao,
             saldo,
             tipo_cobranca,
             nro_os,
             qtd_parcela,
             id_ciclo,
             data_espera,
             vl_total_parc,
             ano_mes_fat,
             vl_entrada,
             data_inclusao,
             id_contrato,
             vl_multa_correcao,
             vl_juros_correcao,
             seq_importacao,
             vl_conta_rateio_agua,
             vl_conta_rateio_esg,
             vl_conta_rateio_serv,
             ident_parc,
             ident_extra,
             aux,
             vl_conta_rateio_encargos,
             vl_entrada_original,
             vl_parcela_original,
             data_aux,
             seq_extra,
             flag,
             id_centralizador)
VALUES      ( seq_financiamentos.NEXTVAL,
             '0005643643',
             '01001020146121000000',
             '9032',
             '3',
             '1',
             1637.14,
             '0',
             '0',
             To_date('05/09/23', 'DD/MM/RR'),
             '1',
             '202309',
             '115994754',
             NULL,
             NULL,
             1637.14,
             '0',
             '3',
             '0',
             '1',
             '13',
             To_date('01/09/23', 'DD/MM/RR'),
             1637.14,
             '202309',
             '0',
             To_date('26/09/2023', 'dd/mm/yyyy'),
             '99657',
             '0',
             '0',
             NULL,
             '0',
             '0',
             '0',
             NULL,
             NULL,
             NULL,
             '0',
             '0',
             1637.14,
             To_date('02/09/23', 'DD/MM/RR'),
             3662,
             NULL,
             NULL );

COMMIT; 

---------------------------gera retificacao mes 08 -----------------------------
 
         INSERT INTO retificacao (

                    matricula,

                    localidade,

                    ano_mes_ct,

                    seq_origem_canc,

                    seq_origem_emit,

                    consumo_pedido,

                    consumo_emit,

                    consumo_canc,

                    vl_canc,

                    vl_emit,

                    data_pedido,

                    data_tarifa,

                    data_execucao_retif,

                    motivo_retif,

                    tipo_retif,

                    id_usuario,

                    laudo_retif,

                    data_contabil,

                    leitura_corrigida,

                    id_motivo_retifica,

                    seq_imp,

                    vl_desconto

                ) VALUES (

                    '0005643643',

                    '0100102',

                    '202309',

                    '115994754',

                    NULL,

                    NULL,

                    '1700',

                    '1676',

                    '0,00',

                    1637.14,

                    TO_DATE('26/09/2023', 'dd/mm/yyyy'),

                    TO_DATE('26/09/2023', 'dd/mm/yyyy'),

                    TO_DATE('26/09/2023', 'dd/mm/yyyy'),

                    NULL,

                    '1',

                    '0',

                    '3662',

                    NULL,

                    NULL,

                    '80',

                    '3662',

                    '0'

                );
 
                COMMIT;

 
-------------------------capturando o seq_original novo -----------------------

            FOR n IN (

                SELECT

                    c.seq_original,

                    c.matricula,

                    c.ano_mes_ct,

                    c.seq_imp

                FROM

                    conta c

                WHERE

                        c.matricula = '0005643643'

                    AND c.seq_imp = 3662

                    AND c.ano_mes_ct = '202309'

                    AND c.situacao_ct = 0

            ) LOOP

                UPDATE parcela p

                SET

                    p.seq_original = n.seq_original

                WHERE

                        p.matricula = n.matricula

                    AND p.ano_mes_parcela = n.ano_mes_ct

                    AND p.seq_extra = n.seq_imp;
 
                UPDATE retificacao r

                SET

                    r.seq_origem_emit = n.seq_original

                WHERE

                        r.matricula = n.matricula

                    AND r.ano_mes_ct = n.ano_mes_ct

                    AND r.seq_imp = n.seq_imp;
 
                COMMIT;

            END LOOP;
 
            COMMIT;

        END IF;

END;
