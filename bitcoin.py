import ssl
import json

import websocket
import bitstamp.client

import credenciais


def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
    key=credenciais.KEY,
    secret=credenciais.SECRET)


def vender():
    trading_cliente = cliente()
    trading_cliente.sell_market_order(quantidade)


def comprar():
    trading_cliente = cliente()
    trading_cliente.buy_market_order(quantidade)


def ao_abrir(ws):
    print('conexão aberta')
    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""
    ws.send(json_subscribe)

def ao_fechar(ws):
    print('fechar')


def error(ws, erro):
    print('erro' + str(erro))


def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)
    print(cliente())
    if price > 9000:
        vender()
    elif price < 8000:
        comprar()
    else:
        print('Aguardar')



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                             on_open=ao_abrir,
                             on_close=ao_fechar,
                             on_error=error,
                             on_message=ao_receber_mensagem
                             )
    ws.run_forever(sslopt={'cert_regs':ssl.CERT_NONE})