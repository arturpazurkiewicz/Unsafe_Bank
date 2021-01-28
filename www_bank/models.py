import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, first_name, last_name, email, password,
                     isAdmin, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name, email,
                    password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, first_name, last_name, email,
                                 password, False, **extra_fields)

    def create_superuser(self, username, first_name, last_name, email,
                         password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, first_name, last_name, email,
                                 password, True, **extra_fields)


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.username + " :- " + self.email

    def save(self, *args, **kwargs):
        if self.id is None:
            super(User, self).save(*args, **kwargs)
            Account(user_id=self).save()
        else:
            super(User, self).save(*args, **kwargs)


class Account(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default="Main account")
    account_balance = models.FloatField(default=0.0)
    account_number = models.CharField(max_length=26, unique=True, blank=True)

    def __str__(self):
        return self.name + " : " + str(self.account_balance)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.account_number = str(random.randint(0, 10 ** 26 - 1)).zfill(
                26)
        super(Account, self).save(*args, **kwargs)


class TransferHistory(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    from_account_number = models.CharField(max_length=26, blank=True,
                                           null=True)
    to_account_number = models.CharField(max_length=26)
    account_balance = models.FloatField(blank=True, null=True)
    description = models.TextField(default="transfer")
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_accepted = models.BooleanField(default=False)
    message_to_admin = models.TextField(default="My message to admin")

    def __str__(self):
        return str(self.account_id_id) + " :- " + str(self.value)

    def display_my_safe_message(self):
        return mark_safe(self.message_to_admin)

    class Meta:
        ordering = ['-id']

    @staticmethod
    def get_money(to_account, from_account, description, value):
        if not (0.0 < value):
            raise Exception("Invalid value")
        try:
            account = Account.objects.get(account_number=to_account)
            TransferHistory(
                account_id=account,
                from_account_number=from_account,
                to_account_number=account.account_number,
                description=description,
                value=value,
                account_balance=account.account_balance,
                is_accepted=True
            ).save()
            account.account_balance += value
            account.save()
        except Exception as e:
            print(e)
            print("Brak konta")

    def send_money(self):
        if not (0.0 < -self.value <= self.account_id.account_balance):
            raise Exception("Lack of funds")
        self.account_id.account_balance += self.value
        self.account_id.save()
        self.is_accepted = True
        self.save()
        TransferHistory.get_money(self.to_account_number,
                                  self.account_id.account_number,
                                  self.description, -self.value)

    def save(self, *args, **kwargs):
        if self.id is None and not self.is_accepted:
            try:
                int(self.to_account_number)
            except ValueError:
                raise Exception("Invalid account number")
            self.from_account_number = self.account_id.account_number
            if not (0.0 < self.value <= self.account_id.account_balance):
                raise Exception("Invalid value")
            self.account_balance = self.account_id.account_balance
            self.value *= -1
            super(TransferHistory, self).save(*args, **kwargs)
        else:
            # check if is_accepted changed
            if self.id is not None and self.is_accepted == True and TransferHistory.objects.get(
                    id=self.id).is_accepted == False:
                super(TransferHistory, self).save(*args, **kwargs)
                TransferHistory.send_money(self)
            else:
                super(TransferHistory, self).save(*args, **kwargs)
