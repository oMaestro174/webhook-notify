import os
import json
import requests
import docker
from flask import Flask, request, jsonify

app = Flask(__name__)

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'
TELEGRAM_TOKEN = '7021232339:AAE5EZuHcdZQm1Ux780-bcPWTIPIIcD9WtA'
TELEGRAM_CHAT_ID = '1723744302'

def send_slack_notification(message):
    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Telegram. Status code: {response.status_code}, Response: {response.text}")

def restart_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.restart()
        return f"Container {container_name} restarted successfully."
    except docker.errors.NotFound:
        return f"Container {container_name} not found."
    except Exception as e:
        return str(e)

#rota para testar e notificar apenas
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    print(json.dumps(data, indent=4))  # Log the received JSON

    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    
    monitor = data.get('monitor', {})
    heartbeat = data.get('heartbeat', {})
    
    monitor_name = monitor.get('name', 'Unknown')
    status = heartbeat.get('status', 'Unknown')
    status = 'up' if status == 1 else 'down' if status == 0 else status
    #local_datetime = heartbeat.get('localDateTime', 'Unknown time')
    #location = heartbeat.get('timezone', 'Unknown location')
    message = data.get('msg', 'No message provided')
    #url = data.get('url', '')
    #container_name = monitor.get('monitor', {}).get('container_name', '')
    container_name = monitor.get('name', 'Não é um container')
    time = heartbeat.get('time','hora desconhecida')
    formatted_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {time}\n"
        #f"📋 *Mensagem:* {message} at {url}\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {monitor_name}"
    )

    #if container_name:
    #    restart_message = restart_container(container_name)
    #    formatted_message += f"\n🚀 *Restart Container:* {restart_message}"



    send_slack_notification(formatted_message)
    send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200

#rota para testar, notificar e retartar
@app.route('/notify_restart', methods=['POST'])
def notify_restart():
    data = request.json
    print(json.dumps(data, indent=4))  # Log the received JSON

    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    
    monitor = data.get('monitor', {})
    heartbeat = data.get('heartbeat', {})
    
    monitor_name = monitor.get('name', 'Unknown')
    status = heartbeat.get('status', 'Unknown')
    status = 'up' if status == 1 else 'down' if status == 0 else status
    #local_datetime = heartbeat.get('localDateTime', 'Unknown time')
    #location = heartbeat.get('timezone', 'Unknown location')
    message = data.get('msg', 'No message provided')
    #url = data.get('url', '')
    #container_name = monitor.get('monitor', {}).get('container_name', '')
    container_name = monitor.get('name', 'Não é um container')
    time = heartbeat.get('time','hora desconhecida')
    formatted_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {time}\n"
        #f"📋 *Mensagem:* {message} at {url}\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {monitor_name}"
    )

    if container_name:
        restart_message = restart_container(container_name)
        formatted_message += f"\n🚀 *Restart Container:* {restart_message}"



    send_slack_notification(formatted_message)
    send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200

@app.route('/slack_restart', methods=['POST'])
def slack_restart():
    data = request.json
    print(json.dumps(data, indent=4))  # Log the received JSON

    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    
    monitor = data.get('monitor', {})
    heartbeat = data.get('heartbeat', {})
    
    monitor_name = monitor.get('name', 'Unknown')
    status = heartbeat.get('status', 'Unknown')
    status = 'up' if status == 1 else 'down' if status == 0 else status
    local_datetime = heartbeat.get('localDateTime', 'Unknown time')
    location = heartbeat.get('timezone', 'Unknown location')
    message = data.get('msg', 'No message provided')
    #url = data.get('url', '')
    #container_name = monitor.get('monitor', {}).get('container_name', '')
    container_name = monitor.get('name', 'Não é um container')
    #time = heartbeat.get('time','hora desconhecida')
    formatted_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {local_datetime} ({location})\n"
        #f"📋 *Mensagem:* {message} at {url}\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {monitor_name}"
    )

    if container_name:
        restart_message = restart_container(container_name)
        formatted_message += f"\n🚀 *Restart Container:* {restart_message}"



    send_slack_notification(formatted_message)
    #send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200


@app.route('/telegram_restart', methods=['POST'])
def telegram_restart():
    data = request.json
    print(json.dumps(data, indent=4))  # Log the received JSON

    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    
    monitor = data.get('monitor', {})
    heartbeat = data.get('heartbeat', {})
    
    monitor_name = monitor.get('name', 'Unknown')
    status = heartbeat.get('status', 'Unknown')
    status = 'up' if status == 1 else 'down' if status == 0 else status
    #local_datetime = heartbeat.get('localDateTime', 'Unknown time')
    #location = heartbeat.get('timezone', 'Unknown location')
    message = data.get('msg', 'No message provided')
    #url = data.get('url', '')
    #container_name = monitor.get('monitor', {}).get('container_name', '')
    container_name = monitor.get('name', 'Não é um container')
    time = heartbeat.get('time','hora desconhecida')
    formatted_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {time}\n"
        #f"📋 *Mensagem:* {message} at {url}\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {monitor_name}"
    )

    if container_name:
        restart_message = restart_container(container_name)
        formatted_message += f"\n🚀 *Restart Container:* {restart_message}"



    #send_slack_notification(formatted_message)
    send_telegram_message(formatted_message)
    return jsonify({"status": "success"}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
