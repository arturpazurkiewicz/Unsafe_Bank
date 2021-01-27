from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.utils import ErrorList

from www_bank.models import TransferHistory, Account


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=64, help_text='Login',
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Login'}))
    email = forms.EmailField(max_length=254, help_text='Valid e-mail address',
                             widget=forms.TextInput
                             (attrs={'placeholder': 'E-mail'}))
    first_name = forms.CharField(max_length=64, help_text="First name",
                                 widget=forms.TextInput
                                 (attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=128, help_text="Last name",
                                required=False, widget=forms.TextInput
        (attrs={'placeholder': 'Last name'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')


class TransferForm(ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None,
                 use_required_attribute=None, renderer=None, user_id=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class,
                         label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.fields['account_id'].queryset = Account.objects.filter(
            user_id=user_id)

    account_id = forms.ModelChoiceField(queryset=None, required=True,
                                        help_text='Select account')
    to_account_number = forms.CharField(required=True,
                                        help_text='Receiver account number',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'autocomplete': 'off',
                                                   'pattern': '[0-9]{26}',
                                                   'placeholder': 'Receiver account number',
                                                   'size': 30}))

    description = forms.CharField(max_length=256, help_text="Description",
                                  required=False, widget=forms.TextInput
        (attrs={'placeholder': 'Description'}))
    value = forms.FloatField(help_text="Value", min_value=0.01,
                             widget=forms.NumberInput
                             (attrs={'placeholder': 'Value', 'step': '0.01'}))

    class Meta:
        model = TransferHistory
        fields = ('account_id', 'to_account_number', 'description', 'value')
