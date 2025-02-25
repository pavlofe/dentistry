from flask import Flask, render_template, request
from mailjet_rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

# Mailjet client setup
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_message(subject, text='', additional=''):
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
                "Subject": subject,
                "TextPart": text,
                "HTMLPart": additional
            }
        ]
    }
    return mailjet.send.create(data=message)

testimonials = [
    {"text": "Чудова клініка! Прекрасні лікарі, все пояснили і зробили без болю!", "name": "Ольга"},
    {"text": "Мої зуби ніколи не були такими білими! Рекомендую!", "name": "Максим"},
    {"text": "Найкраща стоматологія, якою я коли-небудь користувався. Сервіс на високому рівні.", "name": "Анна"},
]

@app.route('/')
def index():
    return render_template('index.html', testimonials=testimonials)

@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app.route('/success', methods=['POST'])
def success():
    # Get the form data
    full_name = request.form['fullName']
    phone = request.form['phone']
    email = request.form['email']
    
    # Prepare the subject and body of the email
    subject = "Новий запис на консультацію"
    text = f"Ім'я: {full_name}\nТелефон: {phone}\nEmail: {email}"
    html = f"<h3>Запис на консультацію</h3><p><strong>Ім'я:</strong> {full_name}</p><p><strong>Телефон:</strong> {phone}</p><p><strong>Email:</strong> {email}</p>"

    # Send the email
    result = send_message(subject, text, html)

    # Check if the email was sent successfully
    if result.status_code == 200:
        return render_template('success.html')
    else:
        return render_template('error.html', error="Не вдалося надіслати повідомлення.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

