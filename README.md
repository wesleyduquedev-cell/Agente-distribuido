# Agente de Monitoramento de Sistema

Agente em Python que coleta métricas de CPU, memória RAM e disco a cada 5 segundos, classifica o uso de cada recurso e envia os dados em JSON para uma API via HTTP.

**Funcionalidades**
* Coleta de métricas do sistema com psutil.
* Classificação de cada métrica em NORMAL, ATENCAO OU CRITICO.
* Envio dos dados para uma API com requests (POST em JSON).
* Continua rodando mesmo se uma coleta ou um envio falhar.
* Funciona em Windows, Linux e macOS.

**Requisitos**
* Python 3.8 ou superior e bibliotecas listadas no `requirements.txt`.

## Instalação e Uso

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
pip install -r requirements.txt
```

Para iniciar o agente, execute `python main.py`. Para encerrar, pressione `Ctrl + C`.
Por padrão, o agente só exibe o JSON no terminal. Para enviar os dados a uma API, configure a variável `API_URL` dentro do arquivo principal.

## Configuração e Payload

**Variáveis de Configuração**
| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `AGENTE_ID` | "servidor-prod-01" | Identificador da máquina monitorada. |
| `INTERVALO_COLETA` | 5 | Segundos entre cada coleta. |
| `API_URL` | None | Endereço da API; `None` desativa o envio. |
| `TIMEOUT_ENVIO` | 5 | Tempo máximo de espera pela resposta da API. |

**Critérios de Status**
| Métrica | ATENCAO a partir de | CRITICO a partir de |
| :--- | :--- | :--- |
| CPU | 50% | 80% |
| RAM | 80% | 90% |
| Disco | 80% | 90% |

**Formato do JSON enviado**
```json
{
  "agente_id": "servidor-prod-01",
  "timestamp": "2026-09-23T23:29:16Z",
  "sistema_operacional": "Linux",
  "metricas": {
    "cpu": {
      "uso_porcentagem": 12.5,
      "nucleos": 8,
      "status": "NORMAL"
    },
    "memoria_ram": {
      "total_gb": 15.87,
      "em_uso_gb": 7.42,
      "disponivel_gb": 8.45,
      "uso_porcentagem": 46.8,
      "status": "NORMAL"
    },
    "disco": {
      "total_gb": 476.94,
      "em_uso_gb": 390.1,
      "disponivel_gb": 86.84,
      "uso_porcentagem": 81.8,
      "status": "ATENCAO"
    }
  }
}
```

## Testes e Equipe

**Testando o envio localmente**
Para testar o envio sem um servidor real, crie um `servidor_teste.py` com Flask:

```python
from flask import Flask, request

app = Flask(__name__)

@app.post("/metricas")
def receber():
    dados = request.get_json()
    print(f"Recebido de {dados['agente_id']}: CPU {dados['metricas']['cpu']['uso_porcentagem']}%")
    return {"ok": True}

if __name__ == "__main__":
    app.run(port=8000)
```
Inicie o servidor Flask e, no agente, defina a `API_URL` como `"http://localhost:8000/metricas"`.

**Estrutura do projeto**
* `main.py` - Agente: coleta, classificação e envio.
* `requirements.txt` - Dependências.
* `README.md` - Documentação.

**Equipe (Grupo 1)**
| Integrante | Responsabilidade |
| :--- | :--- |
| **Gabriel Zago** | **Estrutura base, payload JSON e integração** |
| Fabrício | Coleta de CPU |
| Wesley | Coleta de RAM |
| Rafael | Coleta de disco |
