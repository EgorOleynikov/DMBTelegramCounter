import requests
import datetime
import configparser

class Delta:
	def __init__(self, months, days):
		self.m = months
		self.d = days

config = configparser.ConfigParser()
config.read('config.ini')
chatId = config['TELEGRAM']['chatId']
TOKEN = config['TELEGRAM']['TOKEN']
exec('DMB = ' + config['TELEGRAM']['DMB'])
now = datetime.datetime.now()
demobilization = datetime.datetime(DMB[2],DMB[1],DMB[0] + 1)
delta = demobilization - now
deltaM = demobilization.month - now.month
monthsHArr = [1,3,5,7,8,10,12]
print(delta.days)
delta = Delta([], delta.days)
print(deltaM)
daysInTotal = 0

def howManyDaysInM(currentMonth):
	days = 0
	if currentMonth in monthsHArr:
		days += 31

	elif currentMonth == 0:
		days = 0

	elif currentMonth == 2:
		days += 28

	else:
		days += 30

	return days

for monthN in range(deltaM):
	currentMonth = demobilization.month - monthN
	daysInTotal += howManyDaysInM(currentMonth)

delta.m = [deltaM, delta.d - daysInTotal]

if delta.m[1] < 0:
	daysInM = howManyDaysInM(delta.m[0])
	delta.m[0] -= 1
	delta.m[1] += daysInM + 1

print(delta.m)

# дней
enda = "%D0%B4%D0%BD%D0%B5%D0%B9"
# дня
endb = "%D0%B4%D0%BD%D1%8F"
# день
endc = "%D0%B4%D0%B5%D0%BD%D1%8C"
# месяцев
endMa = '%D0%BC%D0%B5%D1%81%D1%8F%D1%86%D0%B5%D0%B2'
# месяца
endMb = '%D0%BC%D0%B5%D1%81%D1%8F%D1%86%D0%B0'
# месяц
endMc = '%D0%BC%D0%B5%D1%81%D1%8F%D1%86'

# day/month ending
def ending(x, num):
	ending = ""
	if x == "d":
		if num % 100 in range(5,21):
			ending = enda
		elif num % 10 == 1:
			ending = endc
		elif num % 10 in [2,3,4]:
			ending = endb
		else:
			ending = enda

	elif x == "m":
		if num in [2,3,4]:
			ending = endMb
		elif num == 1:
			ending = endMc
		else:
			ending = endMa

	return ending


def request(method):
    url = 'https://api.telegram.org/bot{}/{}'.format(TOKEN, method)
    response = requests.get(url)
    response_json = response.json()
    print(response_json)
    return response_json

if 'pinId' in config['TELEGRAM']:
	pinId = config['TELEGRAM']['pinId']
	request("editMessageText?chat_id={}&message_id={}&text=%F0%9F%91%89 +{}+{}+{}+{}+ %F0%9F%91%88".format(chatId, pinId, delta.m[0], ending("m", delta.m[0]), delta.m[1], ending("d", delta.m[1])))

else:
	method = "sendMessage?chat_id={}&text=%F0%9F%91%89 +{}+{}+{}+{}+ %F0%9F%91%88".format(chatId,delta.m[0], ending("m", delta.m[0]), delta.m[1], ending("d", delta.m[1]))
	messageId = request(method)['result']['message_id']
	config.set("TELEGRAM", "pinId", str(messageId))
	request("pinChatMessage?chat_id={} &message_id={}".format(chatId, messageId))
	with open('config.ini', 'w+') as file:
		config.write(file)

# The API endpoint
method = "sendMessage?chat_id={}&text=%D0%94%D0%BE+%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%89%D0%B5%D0%BD%D0%B8%D1%8F+%D1%81%D1%82%D0%B0%D1%80%D0%B5%D0%B9%D1%88%D0%B8%D0%BD%D1%8B+%D0%BF%D0%B8%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE+%D0%BA%D0%BB%D0%B0%D0%BD%D0%B0+%D0%B8+%D0%B4%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D0%BE%D1%87%D1%82%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE+%D0%B1%D1%80%D0%B0%D1%82%D0%B0+%D0%B1%D1%80%D0%B0%D1%82%D1%81%D1%82%D0%B2%D0%B0+%D0%B4%D0%B5%D0%B4+%D0%B8%D0%BD%D1%81%D0%B0%D0%B9%D0%B4%D0%BE%D0%B2+%D0%BE%D1%81%D1%82%D0%B0%D0%BB%D0%BE%D1%81%D1%8C+{}+{}".format (chatId, delta.d, ending("d", delta.d))

print(request(method))
