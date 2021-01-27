# Create your views here.
from math import floor

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from www_bank.forms import SignUpForm, TransferForm
from www_bank.models import *


@login_required(login_url='login')
def index(request):
    user = request.user
    accounts = Account.objects.filter(user_id=user)
    return render(request, 'index.html', {'accounts': accounts})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='login')
def get_account(request, account_id):
    user = request.user
    account = Account.objects.get(id=account_id, user_id=user)
    history = TransferHistory.objects.filter(account_id=account,
                                             is_accepted=True)
    unaccepted = TransferHistory.objects.filter(account_id=account,
                                                is_accepted=False)

    return render(request, 'account.html',
                  {'account': account, 'history': history,
                   'unaccepted': unaccepted})


@login_required(login_url='login')
def create_transaction(request):
    user = request.user
    data = {'accounts': Account.objects.filter(user_id=user)}
    if request.method == 'POST':
        form = TransferForm(request.POST, user_id=user)
        if form.is_valid():
            try:
                tr = form.save(commit=False)
                tr.value = floor(tr.value * 100) / 100
                tr.save()
                return redirect('/transaction/' + str(tr.id) + '/')
            except Exception as e:
                data['error'] = e
            # TransferHistory.send_money(account_id, tr.to_account_number,
            #                            tr.description, tr.value)
    else:
        form = TransferForm(user_id=user)
    data['form'] = form
    return render(request, 'create_transaction.html', data)


def _accepted_transaction(request, body):
    return render(request, 'transaction.html',
                  body)


def _unaccepted_transaction(request, body):
    return render(request, 'unaccepted_transaction.html',
                  body)


@login_required(login_url='login')
def show_transaction(request, transaction_id):
    body = {}
    try:
        transaction = TransferHistory.objects.get(id=transaction_id,
                                                  account_id__user_id=request.user)
    except:
        return redirect('/')
    if request.method == 'POST':
        if request.POST.get('is_ok') == 'Accept':
            try:
                transaction.send_money()
            except Exception as e:
                body['error'] = e
        elif request.POST.get('is_ok') == 'Delete':
            transaction.delete()
            return redirect('/')
    body['transaction'] = transaction
    if transaction.is_accepted:
        return _accepted_transaction(request, body)
    return _unaccepted_transaction(request, body)
