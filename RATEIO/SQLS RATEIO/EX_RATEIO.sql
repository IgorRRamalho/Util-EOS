
SELECT
    c.ano_mes_leitura        ref,
    c.leitura,
    c.conmed,
    c.confat,
    c.medconmed              med_medida,
    c.media_consumo_faturado med_fat, --usada em caso de modo_fat M
    c.credito_consumo        cred_cons,
    c.ano_mes_base,
    c.credito_utilizado, --usado em caso de modo_fat != M
    c.modo_fat,
    c.id_conf, --alterar para 3 em caso de update na leitura
    c.sit_hd,--verificar alteração de HD para calculo incorreto de rateio
    c1.situacao_ct, -- verificar situacao 8
    c1.tipo_proc -- verificar se processamento 0 ou 6
FROM
    consumo c
    LEFT JOIN conta   c1 ON c.matricula = c1.matricula and c1.ano_mes_ct = c.ano_mes_leitura and c1.tipo_ct = 0
WHERE
    c.matricula = '0007276958'
ORDER BY
    c.ano_mes_leitura DESC;     

/* SDES-3662 || Calcula rateio e altera consumos */

DECLARE

    v_sigla  CHAR(20) := '';

    v_existe INTEGER;

BEGIN

    SELECT

        sigla

    INTO v_sigla

    FROM

        empresa

    WHERE

        id_empresa = '0001';
 
    IF v_sigla = 'DESO' THEN

  -- CLIENTE 0005643643 - NORCON/EDF GRAND PARC JARDINS
 
        UPDATE consumo c
        SET

            c.credito_consumo = 0

        WHERE

                c.matricula = '0005643643'

            AND c.ano_mes_leitura = '202305';
 
        COMMIT;

        UPDATE consumo c
        SET
            c.confat = 1631,
            c.medconmed = 940,
            c.media_consumo_faturado = 1356,
            c.credito_consumo = 0
        WHERE
            c.matricula = '0005643643'
            AND c.ano_mes_leitura = '202306';
        COMMIT;

        UPDATE consumo c

        SET

            c.confat = 1356,

            c.medconmed = 940,

            c.media_consumo_faturado = 1356,

            c.credito_consumo = 0

        WHERE

                c.matricula = '0005643643'

            AND c.ano_mes_leitura = '202307';
 
        COMMIT;

        UPDATE consumo c

        SET

            c.confat = 1676,

            c.credito_consumo = 1356,

            c.credito_utilizado = 1356,

            c.modo_fat = 'A'

        WHERE

                c.matricula = '0005643643'

            AND c.ano_mes_leitura = '202308';
 
        COMMIT;

        UPDATE consumo c

        SET

            c.medconmed = 1288,

            c.media_consumo_faturado = 1475,

            c.credito_consumo = 0,

            c.credito_utilizado = 0

        WHERE

                c.matricula = '0005643643'

            AND c.ano_mes_leitura = '202309';
 
        COMMIT;

-------------------------------recalculo de rateio -----------------------------

        DELETE ligacao_vinculada_consumo

        WHERE

                matricula_pai = '0005643643'

            AND ano_mes_leitura = '202306';
 
        COMMIT;

        p_rateio_fatura('202306', '0005643643',0,0);

        COMMIT;

        DELETE ligacao_vinculada_consumo

        WHERE

                matricula_pai = '0005643643'

            AND ano_mes_leitura = '202307';
 
        COMMIT;

        p_rateio_fatura('202307', '0005643643',0,0);

        COMMIT;

        DELETE ligacao_vinculada_consumo

        WHERE

                matricula_pai = '0005643643'

            AND ano_mes_leitura = '202308';
 
        COMMIT;

        p_rateio_fatura('202308', '0005643643',0,0);

        COMMIT;

        DELETE ligacao_vinculada_consumo

        WHERE

                matricula_pai = '0005643643'

            AND ano_mes_leitura = '202309';
 
        COMMIT;

        p_rateio_fatura('202309', '0005643643',0,0);

        COMMIT;
