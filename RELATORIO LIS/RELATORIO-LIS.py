import pandas as pd
import cx_Oracle
from openpyxl import load_workbook

# Configurações do banco de dados Oracle para cada consulta
db_configs = {
    'ATS': {
        'user': 'NETUNO_Consulta_PRD',
        'password': 'NETUNO_Eos2143',
        'dsn': 'netuno.eosconsultores.com.br/ATS',
    },
    'DESO': {
        'user': 'NETUNO_CONSULTA',
        'password': 'oDDanqeMNpwzaCSG',
        'dsn': '10.41.36.2/PDBEOS',
    },
    'CODAU': {
        'user': 'CODAU_CONSULTA',
        'password': 'q6eMDXqbuQIUKuQI',
        'dsn': '10.41.36.2/PDBEOS',
    },
}

# Função para executar a consulta e preencher o modelo Excel
def execute_query_and_fill_excel(query, template_filename, output_filename, db_config_key):
    # Conecta ao banco de dados Oracle usando a configuração específica
    connection = cx_Oracle.connect(**db_configs[db_config_key])

    try:
        # Executa a consulta SQL
        result = pd.read_sql_query(query, connection)

        # Carrega o modelo Excel
        wb = load_workbook(template_filename)

        # Seleciona a planilha ativa (assumindo que há apenas uma planilha)
        sheet = wb.active

        # Preenche o Excel com os dados da consulta
        for row in pd.DataFrame(result).itertuples(index=False, name=None):
            sheet.append(row)

        # Salva o resultado em um novo arquivo Excel
        wb.save(output_filename)

        print(f"Relatório gerado com sucesso: {output_filename}")

    finally:
        # Fecha a conexão com o banco de dados
        connection.close()

# Consultas SQL
ATS_CONSULTA = "SELECT * FROM CLIENTE WHERE ID_RUA = 640;"
CODAU_CONSULTA = "SELECT * FROM CLIENTE WHERE ID_RUA = 1454;"
DESO_CONSULTA = "SELECT * FROM CLIENTE WHERE ID_RUA = 17543;"


# Preenche o modelo Excel para cada consulta
execute_query_and_fill_excel(ATS_CONSULTA, 'modelo_excel/ATS-4825_Relatório_ligações_não_atualizadas_na_LIS_(01-2024).xlsx', 'relatorio_query1.xlsx', 'ATS')
execute_query_and_fill_excel(CODAU_CONSULTA, 'modelo_excel/SCOD-394_Relatório_ligações_não_atualizadas_na_LIS_(01-2024).xlsx', 'relatorio_query2.xlsx', 'CODAU')
execute_query_and_fill_excel(DESO_CONSULTA, 'modelo_excel/SDES-2802_Relatório_ligações_não_atualizadas_na_LIS_(01-2024).xlsx', 'relatorio_query3.xlsx', 'DESO')

