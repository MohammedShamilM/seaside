from django.shortcuts import render
from .models import Wallet,Transaction
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='user_login')
def user_wallet(request):
    User = request.user
    wallet = Wallet.objects.get_or_create(user = User)
    wallet = Wallet.objects.get(user = User)
    credit_transactions = Transaction.objects.filter(wallet = wallet,transaction_type = 'credit').order_by('-created_at')
    debit_transactions = Transaction.objects.filter(wallet = wallet,transaction_type = 'debit').order_by('-created_at')


    return render(request,'wallet.html',{'wallet':wallet,'credit_transactions' : credit_transactions,'debit_transactions' : debit_transactions})