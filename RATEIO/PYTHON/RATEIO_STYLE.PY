import PySimpleGUI as sg

def recalculo_rateio(matricula):
    sg.theme('LightBlue2')  # Configura el tema de la interfaz gráfica

    # Diseño de la ventana de entrada de datos
    layout = [
        [sg.Text('Digite o número de meses para recálculo:'), sg.InputText(key='-NUM_MESES-')],
        [sg.Button('Ok')]
    ]

    # Crea la ventana
    window = sg.Window('Recálculo de Rateio', layout)

    # Event Loop para procesar eventos
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Ok':
            try:
                num_meses = int(values['-NUM_MESES-'])
                break
            except ValueError:
                sg.popup_error("Por favor, insira um número válido.")

    window.close()

    # Resto del código del recálculo de rateio
    referencias = []
    for i in range(num_meses):
        referencia = sg.popup_get_text(f"Digite a referência para o mês {i + 1}:")
        referencias.append(referencia.strip())

    # Resto del código...

# Resto del código...

# Menu
while True:
    print("\n==== Menu ====")
    print("1. Recálculo de Rateio")
    print("2. Update Consumo")
    print("3. Gerar Conta e outros")
    print("0. Sair")

    escolha = input("Escolha a opção (0-3): ")

    if escolha == '1':
        recalculo_rateio(22)
    # Resto del código...
