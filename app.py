from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import twder
from function.OWM import Roy
from function.astro import *

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
		userID = event.source.user_id
		line_bot_api.push_message(userID,StickerSendMessage(package_id='11537',sticker_id='52002745'))
		line_bot_api.push_message(userID,TextSendMessage(text='拿到你的ID'))
		message = TextSendMessage(text='hello: '+userID)
	elif send == '哈囉':
		message = TextSendMessage(text='good bye')
	elif send == 'Roy' or send == 'roy':
		message = TextSendMessage(text=send +'是笨蛋!')
	elif send == '日幣' or send == 'JPY':
		message = TextSendMessage(text='日幣匯率是'+twder.now('JPY')[3])
	elif send == '星座':
		message = TextSendMessage(text='選擇星座:[1]牡羊 [2]金牛 [3]雙子 [4]巨蟹 [5]獅子 [6]處女 [7]天秤 [8]天蠍 [9]射手 [10]摩羯 [11]水瓶 [12]雙魚')
	elif send == '遊戲':
		'''
		message = TemplateSendMessage(
			alt_text='Krunker.io\nhttps://krunker.io\nslither.io\nhttp://slither.io/\nSTARBLAST.IO\nhttps://starblast.io/',
			template=ButtonsTemplate(
				thumbnail_image_url='https://grizix.com/media/177/krunker-io.jpg',
				title='遊戲選擇',
				text='請選擇要玩的遊戲',
				actions=[
					URIAction(
						label='Krunker.io',
						uri='https://krunker.io'
					),
					URIAction(
						label='slither.io',
						uri='http://slither.io/'
					),
					URIAction(
						label='STARBLAST.IO',
						uri='https://starblast.io/'
					)
				]
			)
		)
		'''
		message = TemplateSendMessage(
			alt_text='Carousel template',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://grizix.com/media/177/krunker-io.jpg',
						title='Krunker.io',
						text='射擊遊戲',
						actions=[
							URIAction(
								label='開始遊玩',
								uri='https://krunker.io'
							)
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://grizix.com/media/177/krunker-io.jpg',
						title='Krunker.io',
						text='射擊遊戲',
						actions=[
							URIAction(
								label='開始遊玩',
								uri='https://krunker.io'
							)
						]
					)
				]
			)
		)
	if send.isdigit() and int(send) <= 12:
		message = TextSendMessage(text=astroScore(send))

	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
	lat = event.message.latitude
	lon = event.message.longitude
	message = TextSendMessage(text=Roy(lat,lon))
	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
	message = StickerSendMessage(package_id='11537',sticker_id='52002767')
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
