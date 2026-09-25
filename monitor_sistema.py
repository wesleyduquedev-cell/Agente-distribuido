# -=-=-=- IMPORTAÇÕES -=-=-=-
import json
import os
import platform
import socket
import time

import psutil
import requests


# -=-=-=- CONFIGURAÇÕES GERAIS -=-=-=-
AGENTE_ID = socket.gethostname()   # cada notebook se identifica pelo próprio nome
INTERVALO_COLETA = 5               # segundos entre coletas
API_URL = None                     # ex.: "http://192.168.0.10:8000/metricas" (None = só exibe)
TIMEOUT_ENVIO = 5                  # segundos
DISCO_RAIZ = os.path.abspath(os.sep)  # "/" no Linux, "C:\\" no Windows
GB = 1024 ** 3

# Limites de status centralizados: (atenção, crítico) em %
LIMITES = {
    "cpu":         (50, 80),
    "memoria_ram": (80, 90),
    "disco":       (80, 90),
}


# -=-=-=- FUNÇÕES AUXILIARES -=-=-=-
def classificar(percentual, metrica):
    """Devolve NORMAL / ATENCAO / CRITICO com base nos LIMITES da métrica."""
    atencao, critico = LIMITES[metrica]
    if percentual >= critico:
        return "CRITICO"
    if percentual >= atencao:
        return "ATENCAO"
    return "NORMAL"


def em_gb(valor_bytes):
    """Converte bytes para GB com 2 casas decimais."""
    return round(valor_bytes / GB, 2)


def montar_armazenamento(metrica, total, usado, livre, percentual):
    """Estrutura padrão para RAM e disco (mesmos campos nas duas)."""
    return {
        "total_gb": em_gb(total),
        "em_uso_gb": em_gb(usado),
        "disponivel_gb": em_gb(livre),
        "uso_porcentagem": percentual,
        "status": classificar(percentual, metrica),
    }


# -=-=-=- COLETORES (um por integrante) -=-=-=-
def coletar_cpu():
    """Parte do Fabrício."""
    uso = psutil.cpu_percent(interval=1)
    return {
        "uso_porcentagem": uso,
        "nucleos": psutil.cpu_count(logical=True),
        "status": classificar(uso, "cpu"),
    }


def coletar_ram():
    """Parte do Wesley."""
    m = psutil.virtual_memory()
    return montar_armazenamento("memoria_ram", m.total, m.used, m.available, m.percent)


def coletar_disco():
    """Parte do Rafael."""
    d = psutil.disk_usage(DISCO_RAIZ)
    return montar_armazenamento("disco", d.total, d.used, d.free, d.percent)


# Registro dos coletores: chave no JSON -> função
COLETORES = {
    "cpu": coletar_cpu,
    "memoria_ram": coletar_ram,
    "disco": coletar_disco,
}


# -=-=-=- MONTAGEM DO PAYLOAD -=-=-=-
def coletar_dados_sistema():
    """Monta o JSON conforme o contrato de comunicação do projeto."""
    metricas = {}
    for nome, coletor in COLETORES.items():
        try:
            metricas[nome] = coletor()
        except Exception as erro:
            # uma métrica com falha não derruba as outras
            metricas[nome] = {"status": "ERRO", "detalhe": str(erro)}

    return {
        "agente_id": AGENTE_ID,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sistema_operacional": platform.system(),
        "metricas": metricas,
    }


# -=-=-=- ENVIO -=-=-=-
def enviar_dados(payload):
    """Envia o JSON para a API. Retorna True/False sem derrubar o agente."""
    try:
        resposta = requests.post(API_URL, json=payload, timeout=TIMEOUT_ENVIO)
        resposta.raise_for_status()
        return True
    except requests.RequestException as erro:
        print(f"Falha no envio: {erro}")
        return False


def exibir(payload):
    print(f"[{payload['timestamp']}] Dados coletados:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# -=-=-=- EXECUÇÃO PRINCIPAL -=-=-=-
def main():
    print(f"Iniciando Agente de Monitoramento: {AGENTE_ID}")
    print("Pressione Ctrl+C para interromper.\n")

    try:
        while True:
            inicio = time.time()

            payload = coletar_dados_sistema()
            exibir(payload)

            if API_URL and enviar_dados(payload):
                print("Enviado com sucesso.")

            print("-" * 50)
            # desconta o tempo gasto (a CPU já espera 1s) para manter o intervalo real
            time.sleep(max(INTERVALO_COLETA - (time.time() - inicio), 0))

    except KeyboardInterrupt:
        print("\nAgente de monitoramento finalizado com sucesso.")


if __name__ == "__main__":
    main()
