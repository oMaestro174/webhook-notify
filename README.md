# Notificador de Eventos com Reinicio de Container

Este projeto é um serviço web que monitora eventos e envia notificações para diferentes canais (Slack, Telegram e e-mail), além de reiniciar containers Docker quando necessário.

## Estrutura do Projeto

- `app.py`: Arquivo principal contendo a lógica do Flask para receber webhooks, enviar notificações e reiniciar containers.
- `config.json`: Arquivo de configuração contendo as informações dos canais (Slack, Telegram e e-mail).

## Pré-requisitos

- Python 3.8+
- Docker
- Flask
- Requests
- smtplib (para envio de e-mails)

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/oMaestro174/webhook-notify.git
    cd webhook-notify
    ```

2. Crie um ambiente virtual e instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3. Configure o `config.json` com suas informações de Slack, Telegram e e-mail.

## Configuração

### Estrutura do `config.json`

```json
{
    "telegram": {
        "alertasCetif": {
            "token": "SEU_TELEGRAM_BOT_TOKEN",
            "chat_id": "SEU_CHAT_ID"
        },
        "outroCanal": {
            "token": "SEU_OUTRO_TOKEN",
            "chat_id": "SEU_OUTRO_CHAT_ID"
        }
    },
    "slack": {
        "alertas": "https://hooks.slack.com/services/SEU/WEBHOOK/URL",
        "outroCanal": "https://hooks.slack.com/services/OUTRO/CANAL/WEBHOOK"
    },
    "email": {
        "smtp_server": "smtp.seudominio.com",
        "smtp_port": 587,
        "smtp_user": "seu_email@seudominio.com",
        "smtp_password": "sua_senha",
        "recipients": [
            "destinatario1@exemplo.com",
            "destinatario2@exemplo.com"
        ]
    }
}

