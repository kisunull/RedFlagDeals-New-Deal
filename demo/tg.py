import requests

def bot_sendtext(bot_message):
    bot_token = 'your_bot_token'
    bot_chatID = 'your_tg_chatID'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()

def bot_sendtext_channel(bot_message):
    bot_token = 'your_bot_token'
    bot_chatID = '@RedFlagHotDeals'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&disable_web_page_preview=true&text=' + bot_message

    response = requests.get(send_text)
    return response.json()
