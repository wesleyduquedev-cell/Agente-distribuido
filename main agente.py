# -=-=-=- IMPORTAÇÕES -=-=-=-
import time
import json
import platform
import psutil
import requests

# -=-=-=- CONFIGURAÇÕES BÁSICAS -=-=-=-
AGENTE_ID = "servidor-prod-01"
INTERVALO_COLETA = 5          # segundos entre coletas
API_URL = None                # ex.: "http://localhost:8000/metricas" (None = só exibe)
TIMEOUT_ENVIO = 5             # segundos
GB = 1024 ** 3


# -=-=-=- REGRA DE STATUS (padrão para todas as métricas) -=-=-=-
def classificar(percentual, limite_atencao, limite_critico):
    """Devolve um código fixo, fácil de tratar no servidor/dashboard."""
    if percentual >= limite_critico:
        return "CRITICO"
    if percentual >= limite_atencao:
        return "ATENCAO"
    return "NORMAL"


# -=-=-=- FUNÇÃO DE COLETA PRINCIPAL -=-=-=-
def coletar_dados_sistema():
    """
    Função central de coleta.
    A estrutura do JSON segue o contrato de comunicação definido para o projeto.
    """
    dados = {
        "agente_id": AGENTE_ID,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sistema_operacional": platform.system(),
        "metricas": {}
    }

    # -=-=-=- PARTE DO FABRÍCIO (CPU) -=-=-=-
    uso_cpu = psutil.cpu_percent(interval=1)
    dados["metricas"]["cpu"] = {
        "uso_porcentagem": uso_cpu,
        "nucleos": psutil.cpu_count(logical=True),
        "status": classificar(uso_cpu, 50, 80)
    }

    # -=-=-=- PARTE DO WESLEY (RAM) -=-=-=-
    memoria = psutil.virtual_memory()
    dados["metricas"]["memoria_ram"] = {
        "total_gb": round(memoria.total / GB, 2),
        "em_uso_gb": round(memoria.used / GB, 2),
        "disponivel_gb": round(memoria.available / GB, 2),
        "uso_porcentagem": memoria.percent,
        "status": classificar(memoria.percent, 80, 90)
    }

    # -=-=-=- PARTE DO RAFAEL (DISCO) -=-=-=-
    disco = psutil.disk_usage("/")
    dados["metricas"]["disco"] = {
        "total_gb": round(disco.total / GB, 2),
        "em_uso_gb": round(disco.used / GB, 2),
        "disponivel_gb": round(disco.free / GB, 2),
        "uso_porcentagem": disco.percent,
        "status": classificar(disco.percent, 80, 90)
    }

    return dados


# -=-=-=- ENVIO (REQUESTS) -=-=-=-
def enviar_dados(payload):
    """Envia o JSON para a API. Retorna True/False sem derrubar o agente."""
    try:
        resposta = requests.post(API_URL, json=payload, timeout=TIMEOUT_ENVIO)
        resposta.raise_for_status()
        return True
    except requests.RequestException as erro:
        print(f"Falha no envio: {erro}")
        return False


# -=-=-=- EXECUÇÃO PRINCIPAL -=-=-=-
def main():
    print(f"Iniciando Agente de Monitoramento: {AGENTE_ID}")
    print("Pressione Ctrl+C para interromper.\n")

    try:
        while True:
            inicio = time.time()
            try:
                payload = coletar_dados_sistema()
                print(f"[{payload['timestamp']}] Dados coletados:")
                print(json.dumps(payload, indent=2, ensure_ascii=False))

                if API_URL:
                    if enviar_dados(payload):
                        print("Enviado com sucesso.")
            except Exception as e:
                # um erro numa coleta não derruba o agente
                print(f"Erro na coleta: {e}")

            print("-" * 50)
            # desconta o tempo gasto (a CPU já espera 1s) para manter o intervalo real
            time.sleep(max(INTERVALO_COLETA - (time.time() - inicio), 0))

    except KeyboardInterrupt:
        print("\nAgente de monitoramento finalizado com sucesso.")


if __name__ == "__main__":
    main()
