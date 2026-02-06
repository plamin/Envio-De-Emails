# Envio-De-Emails

Este projeto é um script em Python que envia automaticamente emails de lembrete sobre o vencimento de faturas/boletos, com a opção de anexar o arquivo da fatura.
O envio acontece 2 dias antes do vencimento, de forma totalmente automática.

## Funcionalidades

📅 Calcula automaticamente a data de vencimento das faturas

⏰ Envia emails 2 dias antes do vencimento

📎 Permite anexar arquivos (PDF, imagens, etc.)

🔐 Usa variáveis de ambiente para proteger credenciais

📄 Lê as faturas a partir de um arquivo faturas.json

## Tecnologias

Python 3

smtplib

email.message

python-dotenv

JSON
