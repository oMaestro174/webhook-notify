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
```

# Uso
## Inicializar o Servidor
1. Inicie o servidor Flask:

```bash
python app.py
```

2. O servidor estará disponível em http://0.0.0.0:5000.

# Endpoints
- Slack: /webhook/slack/<channel>
- Telegram: /webhook/telegram/<channel>
- Email: /webhook/email

Exemplko de payload

```json
{
    "monitor": {
        "name": "Nome do Monitor"
    },
    "heartbeat": {
        "status": 1,
        "localDateTime": "2023-05-26T12:34:56",
        "timezone": "America/Sao_Paulo"
    },
    "msg": "Mensagem de teste"
}

```

# Contribuição
1. Faça um fork do projeto.
2. Crie uma branch para sua feature (git checkout -b feature/fooBar).
3. Faça commit das suas alterações (git commit -am 'Add some fooBar').
4. Faça push para a branch (git push origin feature/fooBar).
5. Crie um novo Pull Request.

# Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.