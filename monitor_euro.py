import requests

# Credenciais e Configurações
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"
LIMITE_PRECO = 6.00  # Ajuste o valor máximo desejado

def obter_cotacao_euro():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    # 1ª Tentativa: AwesomeAPI com User-Agent
    try:
        url = "https://economia.awesomeapi.com.br/last/EUR-BRL"
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        return float(dados["EURBRL"]["bid"])
    except Exception as e:
        print(f"AwesomeAPI falhou ({e}), tentando API alternativa...")

    # 2ª Tentativa (Backup): ExchangeRate-API (Gratuita e sem limites de IP)
    try:
        url_alt = "https://open.er-api.com/v6/latest/EUR"
        resposta = requests.get(url_alt, headers=headers, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        return float(dados["rates"]["BRL"])
    except Exception as e:
        print(f"Erro ao obter cotação na API alternativa: {e}")
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
    else:
        print(f"Euro (R$ {cotacao:.2f}) está acima do limite configurado (R$ {LIMITE_PRECO:.2f}). Nenhuma mensagem enviada.")
