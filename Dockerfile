# Use uma imagem base com Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo do diretório atual para o diretório de trabalho no container
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 5000


# Comando para rodar a aplicação

CMD ["python", "webhook.py"]

