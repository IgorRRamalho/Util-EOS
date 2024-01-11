import tkinter as tk
from tkinter import simpledialog, messagebox

def update_consumo(matricula):
    num_meses = simpledialog.askinteger("Update Consumo", "Digite o número de meses para update:")

    referencias = []
    for i in range(num_meses):
        referencia = simpledialog.askstring("Update Consumo", f"Digite a referência para o mês {i + 1}:")
        referencias.append(referencia)

    colunas_disponiveis = ['confat', 'medconmed', 'media_consumo_faturado', 'credito_consumo']

    colunas_valores = {}
    for referencia in referencias:
        colunas_valores[referencia] = {}

        root_colunas = tk.Tk()
        root_colunas.title(f"Escolha de Colunas e Valores - Referência: {referencia}")

        def salvar_colunas_selecionadas():
            nonlocal colunas_valores
            colunas_valores[referencia] = {}
            for coluna, entry in zip(colunas_disponiveis, entry_boxes):
                valor = entry.get()
                colunas_valores[referencia][coluna] = valor
            root_colunas.destroy()

        entry_boxes = []
        for coluna in colunas_disponiveis:
            tk.Label(root_colunas, text=f"Valor para {coluna}").pack()
            entry = tk.Entry(root_colunas)
            entry_boxes.append(entry)
            entry.pack()

        tk.Button(root_colunas, text="Salvar", command=salvar_colunas_selecionadas).pack()

        root_colunas.mainloop()

    script_sql_consumo = ""
    for referencia, valores in colunas_valores.items():
        script_sql_consumo += f"""
------------------------------- Update Consumo {referencia} -----------------------------
UPDATE CONSUMO C
    SET
"""
        for coluna, valor in valores.items():
            script_sql_consumo += f"        {coluna} = {valor},\n"
        script_sql_consumo += f"""    WHERE
        c.matricula = '{matricula}'
        AND c.ano_mes_leitura = '{referencia}';
COMMIT;
"""

    with open('UPDATE_CONSUMO.sql', 'w') as file_consumo:
        file_consumo.write(script_sql_consumo)

    messagebox.showinfo("Update Consumo", "Script SQL de Update Consumo gerado com sucesso. Consulte o arquivo UPDATE_CONSUMO.sql.")

# Função para exibir o menu
def exibir_menu(matricula):
    while True:
        escolha = simpledialog.askinteger("Menu", "1. Recálculo de Rateio\n2. Update Consumo\n0. Sair\n\nEscolha a opção (0-2):")

        if escolha == 1:
            recalculo_rateio(matricula)
        elif escolha == 2:
            update_consumo(matricula)
        elif escolha == 0:
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Solicitando informações ao usuário
matricula = simpledialog.askstring("Informações", "Digite sua matrícula:")

# Criando a janela principal
root = tk.Tk()
root.withdraw()  # Ocultando a janela principal

# Exibindo o menu
exibir_menu(matricula)

# Iniciando o loop da interface gráfica
root.mainloop()
