from django.core.mail import send_mail
from django.conf import settings
import threading

def purchase_email(recipint_list=None):
  subject = "JRAT's E-Commerce"
  message = f"You have successfully purchased. Check Your Order Below Link.\nhttp://127.0.0.1:8000/account/profile/"
  from_email = getattr(settings, 'EMAIL_HOST_USER')
  recipint_list = [recipint_list]

  email = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipint_list)

  threading.Thread(
    target=email, args=(subject, message, from_email, recipint_list)
  ).start()

