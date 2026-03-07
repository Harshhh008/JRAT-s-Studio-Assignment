from django.contrib.auth.models import BaseUserManager
import logging

logger = logging.getLogger(__name__)

class CustomManager(BaseUserManager):
  """custom user manager for handling email authentication"""
  def create_user(self, email=None, password=None, **extra_fields):
    try:
      if not email:
        raise ValueError('Email must be required.')
      user = self.model(email=self.normalize_email(email), **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user
    except Exception as e:
      logger.exception(str(e))
  
  def create_superuser(self, email=None, password=None, **extra_fields):
    """custom superuser with extra_fields"""
    try:
      if not email:
        raise ValueError("Email must be required.")
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_active', True)
      extra_fields.setdefault('is_superuser', True)

      return self.create_user(email=email, password=password, **extra_fields)
      
    except Exception as e:
      logger.exception(str(e))