from bs4 import BeautifulSoup
import requests

def star(n):
	global reply
	reply += ('★'*n + '☆'*(5-n))+'\n'


def astroScore(select):
	web = requests.get('https://m.click108.com.tw/astro/index.php?astroNum='+select)
	web2 = requests.get('http://astro.click108.com.tw/unit002/2019/my2019.php?aid='+str(int(select)-1))
	web.enconding = 'UTF-8'
	web2.enconding = 'UTF-8'
	global reply
	reply = ''
	soup = BeautifulSoup(web.text, "html.parser")
	soup2 = BeautifulSoup(web2.text, "html.parser")
	reply += '整體運勢 : ' + soup2.select('.score span')[0].text+'分\n'

	reply += ('整體運')
	star(int(soup.select('#astroDailyScore_all')[0]['style'][-6:-5:1]))
	reply += (soup.select('#astroDailyData_all')[0].text)+'\n'


	reply += ('事業運')
	star(int(soup.select('#astroDailyScore_career')[0]['style'][-6:-5:1]))
	reply += (soup.select('#astroDailyData_career')[0].text)+'\n'

	reply += ('財富運')
	star(int(soup.select('#astroDailyScore_money')[0]['style'][-6:-5:1]))
	reply += (soup.select('#astroDailyData_money')[0].text)+'\n'

	reply += ('開運小秘方')+'\n'
	reply += (soup.select('#astroDailyData_luckyNum')[0].text)
	return reply