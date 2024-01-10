
------------------------------- Update Consumo 202301 -----------------------------
UPDATE CONSUMO C
    SET
        confat = 1,
        medconmed = 2,
        media_consumo_faturado = 3  
 WHERE
        c.matricula = '123'
        AND c.ano_mes_leitura = '202301';
COMMIT;

------------------------------- Update Consumo 202302 -----------------------------
UPDATE CONSUMO C
    SET
        confat = 12,
        medconmed = 44,
        media_consumo_faturado = 22  
 WHERE
        c.matricula = '123'
        AND c.ano_mes_leitura = '202302';
COMMIT;
