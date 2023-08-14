import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Функция для отправки email-уведомления
def send_email(subject, body):
    
    from_email = "your_email@example.com"
    to_email = "recipient@example.com"
    password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.example.com', 587)  # Замените на свой SMTP сервер
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


# URL страницы со списком умерших (например, август 2023 года)
url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%83%D0%BC%D0%B5%D1%80%D1%88%D0%B8%D1%85_%D0%B2_2023_%D0%B3%D0%BE%D0%B4%D1%83"

# Загружаем страницу и создаем объект BeautifulSoup для парсинга
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Находим первый пункт в списке (самый последний умерший)
ul_elements = soup.find_all('ul')
ul_elements_2 = ul_elements[1]

new_entry = ul_elements_2.find('li')

# Находим имя умершего
name = new_entry.find('a').get_text()

# Находим ссылку умершего на википедии
news_link = 'https://ru.wikipedia.org' + new_entry.find('a')['href']

# Находим первый абзац по ссылке конкретного умершего
person_response = requests.get(news_link)
person_soup = BeautifulSoup(person_response.content, 'html.parser')
person_div = person_soup.find('div', id='mw-content-text')
bold_element = person_div.find('p')
person_info = bold_element.get_text()

# Отправляем email-уведомление с информацией о новом пункте в списке
email_subject = "Новый пункт в списке умерших"
email_body = person_info + "\n\nСсылка на страницу: " + news_link
send_email(email_subject, email_body)
