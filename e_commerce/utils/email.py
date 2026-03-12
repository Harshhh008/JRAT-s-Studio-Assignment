from django.core.mail import send_mail
from django.conf import settings
import threading

def purchase_success_email(recipient_email=None):
  subject = "JRAT's E-Commerce"
  message = f"You have successfully purchased. Check Your Order Below Link.\nhttp://127.0.0.1:8000/account/profile/"
  from_email = getattr(settings, 'EMAIL_HOST_USER')
  recipient_list = [recipient_email]

  try:
    threading.Thread(
      target=send_mail, args=(subject, message, from_email, recipient_list)
    ).start()
  except Exception as e:
    pass

def send_reset_password_email(email,  reset_password_email_link):
  subject = "JRAT's E-Commerce reset password link"
  message = f"This is your reset password link using this you can change you password {reset_password_email_link}"
  from_email = getattr(settings, 'EMAIL_HOST_USER')
  recipient_list = [email]

  try:

    threading.Thread(
      target=send_mail, args=(subject, message, from_email, recipient_list)
    ).start()
  except Exception as e:
   pass
