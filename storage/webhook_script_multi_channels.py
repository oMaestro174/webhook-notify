import os
import json
import requests
import docker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('config.json') as config_file:
    config = json.load(config_file)

def send_slack_notification(message, webhook_url):
    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}")

def send_telegram_message(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Telegram. Status code: {response.status_code}, Response: {response.text}")

def send_email(recipient, subject, message):
    smtp_server = config['email']['smtp_server']
    smtp_port = config['email']['smtp_port']
    smtp_user = config['email']['smtp_user']
    smtp_password = config['email']['smtp_password']
    
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

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

@app.route('/webhook/slack/<channel>', methods=['POST'])
def slack_webhook(channel):
    if channel in config['slack']:
        webhook_url = config['slack'][channel]
        data = request.json
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
        container_name = monitor.get('name', 'Não é um container')

        notification_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {local_datetime} ({location})\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {container_name}"
        )

        if container_name:
            restart_message = restart_container(container_name)
            notification_message += f"\n🚀 *Restart Container:* {restart_message}"

        send_slack_notification(notification_message, webhook_url)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Invalid Slack channel"}), 404

@app.route('/webhook/telegram/<channel>', methods=['POST'])
def telegram_webhook(channel):
    if channel in config['telegram']:
        token = config['telegram'][channel]['token']
        chat_id = config['telegram'][channel]['chat_id']
        data = request.json
        if not data:
            return jsonify({"error": "Invalid data format"}), 400
        
        monitor = data.get('monitor', {})
        heartbeat = data.get('heartbeat', {})
    
        monitor_name = monitor.get('name', 'Unknown')
        status = heartbeat.get('status', 'Unknown')
        status = 'up' if status == 1 else 'down' if status == 0 else status
        time = heartbeat.get('time', 'Unknown time')
        message = data.get('msg', 'No message provided')
        container_name = monitor.get('name', 'Não é um container')

        notification_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {time}\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {container_name}"
        )

        if container_name:
            restart_message = restart_container(container_name)
            notification_message += f"\n🚀 *Restart Container:* {restart_message}"

        send_telegram_message(notification_message, token, chat_id)
        return jsonify({"status": "success"}), 200
       
    else:
        return jsonify({"error": "Invalid Telegram channel"}), 404

@app.route('/webhook/email', methods=['POST'])
def webhook_email():
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
    container_name = monitor.get('name', 'Não é um container')

    formatted_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {local_datetime} ({location})\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {monitor_name}"
    )

    for recipient in config['email']['recipients']:
        send_email(recipient, f"Alerta do Monitor: {monitor_name}", formatted_message)

    return jsonify({"status": "success"}), 200

@app.route('/webhook/notify', methods=['POST'])
def webhook_notify():
    data = request.json
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
    container_name = monitor.get('name', 'Não é um container')

    notification_message = (
        f"📊 *Monitor:* {monitor_name}\n"
        f"🔔 *Status:* {status}\n"
        f"🕒 *Hora:* {local_datetime} ({location})\n"
        f"📋 *Mensagem:* {message}\n"
        f"📦 *Container:* {container_name}"
    )

    channels = data.get('channels', {})

    # Enviar para Slack
    slack_channels = channels.get('slack', [])
    for slack_channel in slack_channels:
        if slack_channel in config['slack']:
            send_slack_notification(notification_message, config['slack'][slack_channel])
    
    # Enviar para Telegram
    telegram_channels = channels.get('telegram', [])
    for telegram_channel in telegram_channels:
        if telegram_channel in config['telegram']:
            telegram_info = config['telegram'][telegram_channel]
            send_telegram_message(notification_message, telegram_info['token'], telegram_info['chat_id'])
    
    # Enviar por e-mail
    email_recipients = channels.get('email', [])
    for recipient in email_recipients:
        if recipient in config['email']['recipients']:
            send_email(recipient, f"Alerta do Monitor: {monitor_name}", notification_message)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
