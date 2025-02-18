from mailjet_rest import Client
import os

api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
def sendMesage(Subject, text='', additional=''):
	message = {
	'Messages': [
					{
						"From": {
								"Email": "fedakpavlo70@gmail.com",
								"Name": "Me"
						},
						"To": [
								{
								"Email": "fedakpavlo70@gmail.com",
								"Name": "You"
								}
						],
						"Subject": Subject,
						"TextPart": text,
						"HTMLPart": additional
					}
			]
	}
	return message

message = sendMesage('Тест повідомлення', 'Перевірка успішна✅')

result = mailjet.send.create(data=message)
print (result.json())