from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import twder
app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('qc7rFGFZlKYZQeLoF0vj3pPAvQTMNc33oHEunILObOgqqADF+NLuduHU3pp9XeAC4QJ38mXSZ/YlPHoEeHNUKG9fCWPQ7SalRHleeCnqkZOW+pmg7t81hCJubjMzewdItDlAwfGJd+ozUQJ2gSCRqwdB04t89/1O/w1cDnyilFU=N')
# 設定你的Channel Secret
handler = WebhookHandler('ae1e148a0874ea3c18024b303e9c90f3')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	send = event.message.text
	if send == '你好':
		message = TextSendMessage(text='hello')
	elif send == '哈囉':
		message = TextSendMessage(text='good bye')
	elif send == 'Roy':
		message = TextSendMessage(text=send +'是笨蛋!')
	elif send == '日幣' or send == 'JPY' or send == 'roy':
		message = TextSendMessage(text='日幣匯率是'+twder.now('JPY')[3])
	else:
		message = TextSendMessage(text=event.message.text)
	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
	lat = event.message.latitude
	lon = event.message.longitude
	message = TextSendMessage(text='經緯度是 :'+str(lon)+','+str(lat))
	line_bot_api.reply_message(event.reply_token, message)
'''
print(twder.now('JPY')[3])
你好>hello
哈囉>good bye
其他>回傳一樣
'''

'''
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
	message = TextSendMessage(text='我是佩佩豬機器人')
	line_bot_api.reply_message(event.reply_token, message)
'''

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
