\# Agente de Monitoramento de Sistema

Agente em Python que coleta métricas de CPU, memória RAM e disco a cada 5 segundos, classifica o uso de cada recurso e envia os dados em JSON para uma API via HTTP.



\*\*Funcionalidades\*\*

\* Coleta de métricas do sistema com psutil.

\* Classificação de cada métrica em NORMAL, ATENCAO OU CRITICO.

\* Envio dos dados para uma API com requests (POST em JSON).

\* Continua rodando mesmo se uma coleta ou um envio falhar.

\* Funciona em Windows, Linux e macOS.



\*\*Requisitos\*\*

\* Python 3.8 ou superior e bibliotecas listadas no `requirements.txt`.



\## Instalação e Uso



```bash

git clone <url-do-repositorio>

cd <pasta-do-projeto>

pip install -r requirements.txt

```



Para iniciar o agente, execute `python main.py`. Para encerrar, pressione `Ctrl + C`.

Por padrão, o agente só exibe o JSON no terminal. Para enviar os dados a uma API, configure a variável `API\_URL` dentro do arquivo principal.



\## Configuração e Payload



\*\*Variáveis de Configuração\*\*

| Variável | Padrão | Descrição |

| :--- | :--- | :--- |

| `AGENTE\_ID` | "servidor-prod-01" | Identificador da máquina monitorada. |

| `INTERVALO\_COLETA` | 5 | Segundos entre cada coleta. |

| `API\_URL` | None | Endereço da API; `None` desativa o envio. |

| `TIMEOUT\_ENVIO` | 5 | Tempo máximo de espera pela resposta da API. |



\*\*Critérios de Status\*\*

| Métrica | ATENCAO a partir de | CRITICO a partir de |

| :--- | :--- | :--- |

| CPU | 50% | 80% |

| RAM | 80% | 90% |

| Disco | 80% | 90% |



\*\*Formato do JSON enviado\*\*

```json

{

&#x20; "agente\_id": "servidor-prod-01",

&#x20; "timestamp": "2026-09-23T23:29:16Z",

&#x20; "sistema\_operacional": "Linux",

&#x20; "metricas": {

&#x20;   "cpu": {

&#x20;     "uso\_porcentagem": 12.5,

&#x20;     "nucleos": 8,

&#x20;     "status": "NORMAL"

&#x20;   },

&#x20;   "memoria\_ram": {

&#x20;     "total\_gb": 15.87,

&#x20;     "em\_uso\_gb": 7.42,

&#x20;     "disponivel\_gb": 8.45,

&#x20;     "uso\_porcentagem": 46.8,

&#x20;     "status": "NORMAL"

&#x20;   },

&#x20;   "disco": {

&#x20;     "total\_gb": 476.94,

&#x20;     "em\_uso\_gb": 390.1,

&#x20;     "disponivel\_gb": 86.84,

&#x20;     "uso\_porcentagem": 81.8,

&#x20;     "status": "ATENCAO"

&#x20;   }

&#x20; }

}

```



\## Testes e Equipe



\*\*Testando o envio localmente\*\*

Para testar o envio sem um servidor real, crie um `servidor\_teste.py` com Flask:



```python

from flask import Flask, request



app = Flask(\_\_name\_\_)



@app.post("/metricas")

def receber():

&#x20;   dados = request.get\_json()

&#x20;   print(f"Recebido de {dados\['agente\_id']}: CPU {dados\['metricas']\['cpu']\['uso\_porcentagem']}%")

&#x20;   return {"ok": True}



if \_\_name\_\_ == '\_\_main\_\_':

&#x20;   app.run(port=8000)

```

Inicie o servidor Flask e, no agente, defina a `API\_URL` como `"http://localhost:8000/metricas"`.



\*\*Estrutura do projeto\*\*

\* `main.py` - Agente: coleta, classificação e envio.

\* `requirements.txt` - Dependências.

\* `README.md` - Documentação.



\*\*Equipe (Grupo 1)\*\*

| Integrante | Responsabilidade |

| :--- | :--- |

| \*\*Gabriel Zago\*\* | \*\*Estrutura base, payload JSON e integração\*\* |

| Fabrício | Coleta de CPU |

| Wesley | Coleta de RAM |

| Rafael | Coleta de disco |

