import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

EMAIL_HOST_USER = 'NaSutkiCalendar@mail.ru'
EMAIL_HOST_PASSWORD = 'f2YnZ6LJ3QBfmktVd2SF'


def main():
    email = "teluridkadmiy@gmail.com"
    # if not User.objects.filter(email=email, is_active=True).exists():
    #     return Response({'error': 'Пользователь не зарегистрирован'}, status=401)
    # user = User.objects.get(email=email, is_active=True)
    password = ''
    for i in range(8):
        password += random.choice('*!&$#@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

    # user.set_password(password)
    # user.save()
    subject = 'НаСуткиКалендарь. Новый пароль'
    # message = 'Добрый день, %s!\nВаш новый пароль: %s' % (user.name, password)
    message = f'Добрый день, Господин!\nВаш новый пароль: {password}'

    # send_mail(subject, message, EMAIL_HOST_USER, [email])

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = email
    msg.attach(MIMEText(message))

    s = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    s.ehlo(EMAIL_HOST_USER)
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(EMAIL_HOST_USER, [email], msg.as_string())
    s.quit()

    # return Response({'success': 'Письмо с новым паролем отправлено на почту.'})
    return 'Письмо с новым паролем отправлено на почту.'


if __name__ == "__main__":
    main()
