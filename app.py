## PARA RODAR USE NO TERMINAL: CD Envio-de-Emails-Automaticos ##
## python app.py ##

import os
from dotenv import load_dotenv
import json
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage
import mimetypes

# Carrega as informações do .env
load_dotenv()


# Atribui as informações do .env para as
remetente = os.getenv("remetente")
destinatario = os.getenv("destinatario")
senha_de_app = os.getenv("senha_de_app")

dias_antes = 2

# Função que configura o email
def enviar_email(nome, data_vencimento, caminho_arquivo=None):
    msg = EmailMessage()
    msg["Subject"] = f"Boleto {nome}"
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content(f"Olá, bom dia! \n\nGostaria de confirmar se está tudo ok para realização do pagamento da fatura {nome} vence em {data_vencimento.strftime('%d/%m/%Y')}.\n\nMuito obrigado!")
    # Testa se recebeu um arquivo para o anexo
    if caminho_arquivo:
        # Faz com que o código adivinhe o tipo do arquivo enviado (PDF, JPEG...)
        tipo_mime, _ = mimetypes.guess_type(caminho_arquivo)
        # Se não adivinhar irá retornar um tipo genérico
        if tipo_mime is None:
            tipo_mime = "application/octet-stream"
        # Separa o tipo e subtipo, quebrando o arquivo na primeira barra (image/PNG, image/JPEG, text/html)
        tipo, sub_tipo = tipo_mime.split("/", 1)

    # Lê o arquivo como "rb" (read binary), pois tudo que não é texto simples, como imagens, deve
    # ser lido como binário
        with open(caminho_arquivo, "rb") as f:
            msg.add_attachment(f.read(), maintype=tipo, subtype=sub_tipo, filename=caminho_arquivo.split("/")[-1])

    # Faz login e envia a mensagem
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha_de_app)
        smtp.send_message(msg)

# Calcula o vencimento
def calcular_vencimento(dia, mes):

    hoje = date.today()
    ano = hoje.year

    data = date(ano, mes, dia)

    return data

# Carrega o json
with open("faturas.json", "r", encoding="utf-8") as f:
    faturas = json.load(f)

hoje = date.today()

# A cada fatura no json faturas
for fatura in faturas:
    # Chama a função calcular vencimento
    vencimento = calcular_vencimento(fatura["dia"], fatura["mes"])
    # Calcula a data do email ser enviado
    data_notificacao = vencimento - timedelta(days=dias_antes)

    # Envia o email caso a data da notificação seja hoje
    if hoje == data_notificacao:
        caminho_arquivo = fatura.get("arquivo")
        enviar_email(fatura["nome"], vencimento, caminho_arquivo)
