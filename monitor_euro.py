import requests

# Credenciais e Configurações
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"
LIMITE_PRECO = 5.80  # Ajuste o valor máximo desejado

def obter_cotacao_euro():
    url = "https://economia.awesomeapi.com.br/last/EUR-BRL"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        return float(dados["EURBRL"]["bid"])
    except Exception as e:
        print(f"Erro ao obter cotação: {e}")
        return None

def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar no Telegram: {e}")

# Execução única
cotacao = obter_cotacao_euro()

if cotacao is not None:
    print(f"Cotação verificada: R$ {cotacao:.2f}")
    if cotacao <= LIMITE_PRECO:
        mensagem = (
            f"🚨 *Alerta de Cotação do Euro!* 💶\n\n"
            f"O Euro baixou!\n"
            f"**Cotação Atual:** R$ {cotacao:.2f}\n"
            f"**Seu Limite:** R$ {LIMITE_PRECO:.2f}"
        )
        enviar_mensagem_telegram(mensagem)