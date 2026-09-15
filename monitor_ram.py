import psutil
import time

while True:
    memoria = psutil.virtual_memory()

    total = memoria.total / (1024 ** 3)
    usada = memoria.used / (1024 ** 3)
    disponivel = memoria.available / (1024 ** 3)
    percentual = memoria.percent

    print("===== MONITORAMENTO DA MEMÓRIA RAM =====")
    print(f"RAM Total: {total:.2f} GB")
    print(f"RAM Usada: {usada:.2f} GB")
    print(f"RAM Disponível: {disponivel:.2f} GB")
    print(f"Uso da RAM: {percentual}%")

    if percentual >= 90:
        print("ALERTA: Memória RAM muito alta!")
    elif percentual >= 80:
        print("ATENÇÃO: Uso elevado de memória.")
    else:
        print("Memória RAM normal.")

    print("----------------------------------------")

    time.sleep(5)