from rest_framework import serializers

from www_bank.models import *


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferHistory
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
