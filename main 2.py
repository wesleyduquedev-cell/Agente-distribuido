
#modulo CPU

import time
import argparse
from datetime import datetime

import psutil


# Limiares de classificação (em % de uso de CPU)
LIMITE_NORMAL = 50.0    # abaixo disso -> NORMAL
LIMITE_MODERADO = 80.0  # entre LIMITE_NORMAL e este valor -> MODERADO
                        # acima deste valor -> ALTO


def classificar_uso(percentual: float) -> str:
    """Retorna a classificação textual do uso de CPU."""
    if percentual < LIMITE_NORMAL:
        return "NORMAL"
    elif percentual < LIMITE_MODERADO:
        return "MODERADO"
    else:
        return "ALTO"


def monitorar(intervalo: float = 2.0, por_nucleo: bool = False):
    """
    Monitora o uso da CPU continuamente.

    Args:
        intervalo: tempo em segundos entre cada leitura.
        por_nucleo: se True, exibe também o uso individual de cada núcleo.
    """
    print("Monitor de CPU iniciado. Pressione Ctrl+C para encerrar.\n")
    print(f"{'Horário':<10} {'Uso (%)':<10} {'Status':<10}")
    print("-" * 32)

    try:
        while True:
            uso_total = psutil.cpu_percent(interval=intervalo)
            status = classificar_uso(uso_total)
            horario = datetime.now().strftime("%H:%M:%S")

            print(f"{horario:<10} {uso_total:<10.1f} {status:<10}")

            if por_nucleo:
                uso_nucleos = psutil.cpu_percent(interval=None, percpu=True)
                nucleos_str = " | ".join(
                    f"Núcleo {i}: {v:.1f}%" for i, v in enumerate(uso_nucleos)
                )
                print(f"   {nucleos_str}")

    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário.")


def main():
    parser = argparse.ArgumentParser(
        description="Monitora o uso da CPU e classifica como NORMAL, MODERADO ou ALTO."
    )
    parser.add_argument(
        "-i", "--intervalo",
        type=float,
        default=2.0,
        help="Intervalo entre leituras, em segundos (padrão: 2.0)"
    )
    parser.add_argument(
        "-n", "--nucleos",
        action="store_true",
        help="Exibe também o uso individual de cada núcleo da CPU"
    )
    args = parser.parse_args()

    monitorar(intervalo=args.intervalo, por_nucleo=args.nucleos)


if __name__ == "__main__":
    main()
