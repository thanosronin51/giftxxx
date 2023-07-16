
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .models import *
from .forms import *
from django.db.models import Q
from django.utils import timezone

@login_required
def ticket(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            support_ticket = form.save(commit=False)
            support_ticket.user = request.user
            support_ticket.save()
            messages.success(request, 'Your support ticket has been submitted successfully.')
            return redirect('transactions:ticket')  # Redirect to the same page (ticket view)
    else:
        form = SupportForm()

    user = request.user
    ticketlist = SUPPORT.objects.filter(user=user).order_by('-id')    
    context = {
        'form': form,
        'ticketlist': ticketlist
    }
    return render(request, 'transactions/ticket.html', context)


@login_required
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = request.user
            loan_request.save()
            messages.success(request, 'Your loan request has been submitted. You will be notified within 24 hours.')
            return redirect('home')
    else:
        form = LoanRequestForm()
    context = {
        'title': 'Loan Request',
        'form': form,
    }
    return render(request, 'transactions/loan_request.html', context)

@login_required
def recent_loans(request):
    recent_loans = LoanRequest.objects.order_by()[:10]
    context = {'recent_loans': recent_loans}
    return render(request, 'transactions/loans.html', context)

@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


from django.db.models import F

@login_required
def withdrawal_view(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # Check if the withdrawal amount is greater than the account balance
            withdrawal_amount = withdrawal.amount
            account_balance = withdrawal.user.account.balance

            if withdrawal_amount > account_balance:
                # Insufficient balance, form submission is halted
                form.add_error('amount', 'Insufficient balance. You cannot withdraw more than your account balance.')
            else:
                # Deduct the withdrawal amount from the account balance using F() expression
                withdrawal.user.account.balance = F('balance') - withdrawal_amount
                withdrawal.user.account.save()

                withdrawal.save()
                return redirect('transactions:login_con')  # Redirect to a success page
    else:
        form = WithdrawalForm()
    
    return render(request, 'transactions/form.html', {'form': form})

@login_required
def login_con(request):
    return render(request, 'transactions/login_con.html')

def terms(request):
    return render(request, 'transactions/terms.html')
    
@login_required
def pay_bills(request):
    if request.method == 'POST':
        form = PayBillsForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user

            # Check if the bill amount is greater than the account balance
            bill_amount = bill.amount
            account_balance = bill.user.account.balance

            if bill_amount > account_balance:
                # Insufficient balance, form submission is halted
                form.add_error('amount', 'Insufficient balance. You cannot pay more than your account balance.')
            else:
                # Deduct the bill amount from the account balance using F() expression
                bill.user.account.balance = F('balance') - bill_amount
                bill.user.account.save()

                bill.save()

                # Add a success message with details
                message = f"Thank you, {request.user.username}! Your bill payment for {bill.nickname} has been successfully processed."
                messages.success(request, message)

                return redirect('transactions:bill_con')  # Replace 'bill_con' with the appropriate URL name for the success page
    else:
        form = PayBillsForm()

    context = {
        'form': form,
    }
    return render(request, 'transactions/pay_bills.html', context)


@login_required
def bill_success(request):
    payment = PayBills.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/bill_success.html', {'payment': payment})

@login_required
def bill_con(request):
    return render(request, 'transactions/bill_con.html')

@login_required
def manage_asset(request):
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    
    user = request.user
    cryptowithdrawals = CryptoWITHDRAW.objects.filter(user=user).order_by('-id')
    cryptowithdra = Payment.objects.filter(user=user).order_by('-id')

    context = {
        "user": user,
        "cryptowithdrawals": cryptowithdrawals,
        "cryptowithdra": cryptowithdra,
        "title": "ROYAL BANK"
    }

    return render(request, 'transactions/manage.html', context)



@login_required
def Withdrawal_international_view(request):
    if request.method == 'POST':
        form = WithdrawalInternationalForm(request.POST, user=request.user)

        if form.is_valid():
            withdrawal_international = form.save(commit=False)
            withdrawal_international.user = request.user
            withdrawal_international.target = form.cleaned_data['target_account_number']
            withdrawal_international.recipient_bank_name = form.cleaned_data['target_bank_name']
            withdrawal_international.account_number = form.cleaned_data['target_account_number']
            withdrawal_international.save()

            messages.success(request, 'Your international withdrawal request has been submitted.')
            return redirect('inter_confirm')

    else:
        form = WithdrawalInternationalForm(user=request.user)

    return render(request, 'transactions/inter_form.html', {'form': form})


@login_required
def card_details_upload(request):
    if request.method == 'POST':
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            card_details = form.save(commit=False)
            card_details.user = request.user
            card_details.save()
            messages.success(request, 'Card details uploaded successfully.')  # Add success message
            return redirect('home')
    else:
        form = CardDetailsForm()

    context = {'form': form}
    return render(request, 'transactions/card_upload.html', context)



@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('transactions:payment_success')  # add app name
    else:
        form = PaymentForm()
    return render(request, 'transactions/payment_form.html', {'form': form})


@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/payment_success.html', {'payment': payment})

def create_withdrawal(request):
    if request.method == 'POST':
        form = CryptoWITHDRAWForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # Check if the withdrawal amount exceeds the user's balance for the chosen cryptocurrency
            account = withdrawal.user.account

            if withdrawal.payment_method == 'BITCOIN' and withdrawal.amount > account.bitcoins:
                form.add_error('amount', 'Insufficient Bitcoin balance.')
            elif withdrawal.payment_method == 'ETHEREUM' and withdrawal.amount > account.ethereums:
                form.add_error('amount', 'Insufficient Ethereum balance.')
            elif withdrawal.payment_method == 'USDT_ERC20' and withdrawal.amount > account.usdt_erc20s:
                form.add_error('amount', 'Insufficient USDT ERC20 balance.')
            elif withdrawal.payment_method == 'USDT_TRC20' and withdrawal.amount > account.usdt_trc20s:
                form.add_error('amount', 'Insufficient USDT TRC20 balance.')
            elif withdrawal.payment_method == 'RIPPLE' and withdrawal.amount > account.ripples:
                form.add_error('amount', 'Insufficient Ripple balance.')
            elif withdrawal.payment_method == 'STELLAR' and withdrawal.amount > account.stellars:
                form.add_error('amount', 'Insufficient Stellar balance.')
            elif withdrawal.payment_method == 'LITECOIN' and withdrawal.amount > account.litecoins:
                form.add_error('amount', 'Insufficient Litecoin balance.')

            if not form.errors:
                withdrawal.save()
                withdrawal.update_balance()
                return redirect('transactions:crypto_success')  # Replace with your success URL
    else:
        form = CryptoWITHDRAWForm()
    
    return render(request, 'transactions/withdrawal_form.html', {'form': form})


@login_required
def crypto_success(request):
    payment = CryptoWITHDRAW.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/withdraw_success.html', {'payment': payment})

def recent_withdrawals(request):
    recent_withdrawals = Withdrawal.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_withdrawals': recent_withdrawals}
    return render(request, 'transactions/withdraw.html', context)



def recent_international_withdrawals(request):
    recent_international_withdrawals = Withdrawal_internationa.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_international_withdrawals': recent_international_withdrawals}
    return render(request, 'transactions/withdraw_international.html', context)



def recent_payments(request):
    recent_payments = Payment.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_payments': recent_payments}
    return render(request, 'transactions/payment.html', context)



@login_required
def transaction_history(request):
    user = request.user
    deposit_history = Diposit.objects.filter(user=user).order_by('-timestamp')
    withdrawal_history = Withdrawal.objects.filter(user=user).order_by('-timestamp')
    loan_request_history = LoanRequest.objects.filter(user=user).order_by('-requested_at')
    payment_history = Payment.objects.filter(user=user).order_by('-date')
    crypto_history = CryptoWITHDRAW.objects.filter(user=user).order_by('-date')

    pay_bills = PayBills.objects.filter(user=user).order_by('-timestamp')

    context = {
        'deposit_history': deposit_history,
        'withdrawal_history': withdrawal_history,
        'loan_request_history': loan_request_history,
        'payment_history': payment_history,
        'crypto_history': crypto_history,
    
        'pay_bills': pay_bills
    }

    return render(request, 'transactions/history.html', context)

def check_deposit(request):
    if request.method == 'POST':
        form = CheckDepositForm(request.POST, request.FILES)
        if form.is_valid():
            check_deposit = form.save(commit=False)
            check_deposit.user = request.user
            check_deposit.save()
            amount = check_deposit.amount

            messages.success(request, f"Check deposit of ${amount:.2f} successfully submitted! You will receive a notification about the transaction details.")
            return redirect('home')
    else:
        form = CheckDepositForm()
    return render(request, 'transactions/check_deposit.html', {'form': form})