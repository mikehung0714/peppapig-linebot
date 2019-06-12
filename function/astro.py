from bs4 import BeautifulSoup
import requests

def star(n):
	reply += ('★'*n + '☆'*(5-n))+'\n'


def astroScore(select):
	web = requests.get('https://m.click108.com.tw/astro/index.php?astroNum='+select)
	web.enconding = 'UTF-8'
	reply = ''
	soup = BeautifulSoup(web.text, "html.parser")
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