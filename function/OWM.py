import requests
import time

def Roy(lat,lon):
	url = 'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&units=metric&lang=zh_tw&APPID=98b55c6ae6a6f811f7a9792d78202f45'
	try:
		reply = ''
		r = requests.get(url).json()
		if r['cod']==200:
			reply += ('最低溫:'+str(r['main']['temp_min'])+'\t'+'最高溫:'+str(r['main']['temp_max']))+'\n'
			reply += ('天氣狀況:'+r['weather'][0]['description'])+'\n'
			reply += ('日出:'+str(time.strftime("%H:%M:%S",time.localtime(r['sys']['sunrise']+28800‬)))+'\t'+'日落:'+str(time.strftime("%H:%M:%S",time.localtime(r['sys']['sunset']+28800‬))))+'\n'
		elif r['cod']=="404":
			reply += (r['message'])
	except:
		reply += ('ㄎㄎ沒連上，笑你......')
	return reply

