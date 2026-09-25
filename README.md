# Agente de Monitoramento de Sistema

Agente em Python que coleta o uso de **CPU**, **memória RAM** e **disco** de uma máquina em intervalos regulares, classifica cada métrica em um status (`NORMAL`, `ATENCAO`, `CRITICO`) e envia os dados em JSON para uma máquina central.

A ideia é instalar o agente em vários notebooks que atuam como servidores, enquanto outra máquina recebe e acompanha as informações de todos eles.

---

## Funcionalidades

- Coleta de CPU, RAM e disco com `psutil`
- Classificação automática de status por métrica, com limites configuráveis
- Envio dos dados via HTTP POST (`requests`) para uma API central
- Identificação automática de cada máquina pelo nome (hostname)
- Compatível com Windows e Linux
- Tolerante a falhas: erro em uma métrica ou no envio não interrompe o agente

---

## Requisitos

- Python 3.8 ou superior
- Bibliotecas:
  - `psutil`
  - `requests`

---

## Instalação

```bash
# 1. Clone ou copie o projeto
git clone <url-do-repositorio>
cd monitor_sistema

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux
source venv/bin/activate

# 3. Instale as dependências
pip install psutil requests
```

---

## Configuração

As configurações ficam no topo do arquivo `monitor_sistema.py`:

| Variável           | Padrão                  | Descrição                                                        |
|--------------------|-------------------------|------------------------------------------------------------------|
| `AGENTE_ID`        | nome da máquina         | Identificador do agente enviado no JSON                          |
| `INTERVALO_COLETA` | `5`                     | Segundos entre uma coleta e outra                                |
| `API_URL`          | `None`                  | Endereço da API central. Com `None`, os dados só aparecem na tela |
| `TIMEOUT_ENVIO`    | `5`                     | Tempo máximo (s) de espera pela resposta da API                  |
| `DISCO_RAIZ`       | `/` ou `C:\`            | Partição monitorada (definida automaticamente pelo sistema)      |
| `LIMITES`          | ver tabela abaixo       | Percentuais de atenção e crítico de cada métrica                 |

### Limites de status

| Métrica       | ATENCAO a partir de | CRITICO a partir de |
|---------------|---------------------|---------------------|
| `cpu`         | 50%                 | 80%                 |
| `memoria_ram` | 80%                 | 90%                 |
| `disco`       | 80%                 | 90%                 |

Para alterar, edite o dicionário `LIMITES`:

```python
LIMITES = {
    "cpu":         (50, 80),
    "memoria_ram": (80, 90),
    "disco":       (80, 90),
}
```

---

## Execução

```bash
python monitor_sistema.py
```

Para enviar os dados para a máquina central, defina o endereço da API antes de executar:

```python
API_URL = "http://192.168.0.10:8000/metricas"
```

Para encerrar o agente, pressione **Ctrl+C**.

---

## Formato dos dados (contrato JSON)

Exemplo do payload enviado a cada coleta:

```json
{
  "agente_id": "NOTEBOOK-LAB-01",
  "timestamp": "2026-09-24T14:30:00Z",
  "sistema_operacional": "Windows",
  "metricas": {
    "cpu": {
      "uso_porcentagem": 23.5,
      "nucleos": 8,
      "status": "NORMAL"
    },
    "memoria_ram": {
      "total_gb": 15.87,
      "em_uso_gb": 9.12,
      "disponivel_gb": 6.75,
      "uso_porcentagem": 57.5,
      "status": "NORMAL"
    },
    "disco": {
      "total_gb": 476.34,
      "em_uso_gb": 402.10,
      "disponivel_gb": 74.24,
      "uso_porcentagem": 84.4,
      "status": "ATENCAO"
    }
  }
}
```

| Campo                 | Descrição                                          |
|-----------------------|----------------------------------------------------|
| `agente_id`           | Nome da máquina que enviou os dados                |
| `timestamp`           | Data e hora da coleta em UTC (formato ISO 8601)     |
| `sistema_operacional` | `Windows`, `Linux` ou `Darwin`                     |
| `metricas`            | Objeto com uma entrada para cada métrica coletada  |
| `status`              | `NORMAL`, `ATENCAO`, `CRITICO` ou `ERRO`           |

Se uma métrica falhar, ela é enviada assim, sem afetar as demais:

```json
"disco": { "status": "ERRO", "detalhe": "mensagem do erro" }
```

---

## Estrutura do código

```
monitor_sistema.py
├── Configurações gerais   → AGENTE_ID, intervalos, API_URL, LIMITES
├── Funções auxiliares     → classificar(), em_gb(), montar_armazenamento()
├── Coletores              → coletar_cpu(), coletar_ram(), coletar_disco()
├── COLETORES              → registro que liga cada chave do JSON à sua função
├── coletar_dados_sistema  → monta o payload completo
├── enviar_dados / exibir  → envio para a API e saída no terminal
└── main                   → laço principal de execução
```

---

## Como adicionar uma nova métrica

1. Crie a função de coleta:

   ```python
   def coletar_rede():
       r = psutil.net_io_counters()
       return {
           "enviado_gb": em_gb(r.bytes_sent),
           "recebido_gb": em_gb(r.bytes_recv),
       }
   ```

2. Registre em `COLETORES`:

   ```python
   COLETORES = {
       "cpu": coletar_cpu,
       "memoria_ram": coletar_ram,
       "disco": coletar_disco,
       "rede": coletar_rede,
   }
   ```

3. Se a métrica tiver status, adicione os limites em `LIMITES`.

---

## Equipe

| Integrante | Responsabilidade      |
|------------|-----------------------|
| Fabrício   | Coleta de CPU         |
| Wesley     | Coleta de memória RAM |
| Rafael     | Coleta de disco       |
