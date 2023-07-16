
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Diposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    BANK_CHOICE = (
        ('ABC International Bank Plc', 'ABC International Bank Plc'),
        ('Bank of America', 'Bank of America'),
        ('Citibank', 'Citibank'),
        ('JPMorgan Chase', 'JPMorgan Chase'),
        ('Wells Fargo', 'Wells Fargo'),
        ('Barclays', 'Barclays'),
        ('HSBC', 'HSBC'),
        ('Lloyds Banking Group', 'Lloyds Banking Group'),
        ('Royal Bank of Scotland', 'Royal Bank of Scotland'),
        ('Standard Chartered', 'Standard Chartered'),
        ('UBS', 'UBS'),
        ('Credit Suisse', 'Credit Suisse'),
        ('Deutsche Bank', 'Deutsche Bank'),
        ('Societe Generale', 'Societe Generale'),
        ('BNP Paribas', 'BNP Paribas'),
        ('ING Group', 'ING Group'),
        ('Rabobank', 'Rabobank'),
        ('Santander', 'Santander'),
        ('BBVA', 'BBVA'),
        ('CaixaBank', 'CaixaBank'),
        ('Itau Unibanco', 'Itau Unibanco'),
        ('Bradesco', 'Bradesco'),
        ('Bank of China', 'Bank of China'),
        ('Industrial and Commercial Bank of China', 'Industrial and Commercial Bank of China'),
        ('China Construction Bank', 'China Construction Bank'),
        ('Agricultural Bank of China', 'Agricultural Bank of China'),
        ('Bank of Communications', 'Bank of Communications'),
        ('Mitsubishi UFJ Financial Group', 'Mitsubishi UFJ Financial Group'),
        ('Sumitomo Mitsui Financial Group', 'Sumitomo Mitsui Financial Group'),
        ('Mizuho Financial Group', 'Mizuho Financial Group'),
        ('Nomura Holdings', 'Nomura Holdings'),
        ('Resona Holdings', 'Resona Holdings'),
        ('Sberbank', 'Sberbank'),
        ('VTB Bank', 'VTB Bank'),
        ('Gazprombank', 'Gazprombank'),
        ('Alfa-Bank', 'Alfa-Bank'),
        ('Promsvyazbank', 'Promsvyazbank'),
        ('Rosbank', 'Rosbank'),
        ('Korea Development Bank', 'Korea Development Bank'),
        ('KB Financial Group', 'KB Financial Group'),
        ('Shinhan Financial Group', 'Shinhan Financial Group'),
        ('Woori Financial Group', 'Woori Financial Group'),
        ('Hana Financial Group', 'Hana Financial Group'),
        ('NongHyup Financial Group', 'NongHyup Financial Group'),
        ('Bank Mandiri', 'Bank Mandiri'),
        ('Bank Central Asia', 'Bank Central Asia'),
        ('Bank Rakyat Indonesia', 'Bank Rakyat Indonesia'),
        ('Bank Negara Indonesia', 'Bank Negara Indonesia'),
        ('OCBC Bank', 'OCBC Bank'),
        ('DBS Bank', 'DBS Bank'),
        ('United Overseas Bank', 'United Overseas Bank'),
        ('Bangkok Bank', 'Bangkok Bank'),
        ('Siam Commercial Bank', 'Siam Commercial Bank'),
        ('Kasikornbank', 'Kasikornbank'),
        ('Krung Thai Bank', 'Krung Thai Bank'),
        ('TMB Bank', 'TMB Bank'),
        ('Standard Bank Group', 'Standard Bank Group'),
        ('FirstRand Bank', 'FirstRand Bank'),
        ('Nedbank', 'Nedbank'),
        ('Investec', 'Investec'),
        ('Capitec Bank', 'Capitec Bank'),
        ('Bank of Montreal', 'Bank of Montreal'),
        ('Toronto-Dominion Bank', 'Toronto-Dominion Bank'),
        ('Royal Bank of Canada', 'Royal Bank of Canada'),
        ('Scotiabank', 'Scotiabank'),
        ('National Australia Bank', 'National Australia Bank'),
        ('Australia and New Zealand Banking Group', 'Australia and New Zealand Banking Group'),
        ('Commonwealth Bank', 'Commonwealth Bank'),
        ('Westpac Banking Corporation', 'Westpac Banking Corporation'),
        ('National Bank of Australia', 'National Bank of Australia'),
        ('BNZ', 'BNZ'),
        ('ASB Bank', 'ASB Bank'),
        ('Kiwibank', 'Kiwibank'),
        ('Bank of New Zealand', 'Bank of New Zealand'),
        ('Banco Santander', 'Banco Santander'),
        ('BBVA', 'BBVA'),
        ('CaixaBank', 'CaixaBank'),
        ('Bankia', 'Bankia'),
        ('Banco Sabadell', 'Banco Sabadell'),
        ('ING Group', 'ING Group'),
        ('ABN AMRO', 'ABN AMRO'),
        ('Rabobank', 'Rabobank'),
        ('SNS Bank', 'SNS Bank'),
        ('Banco de Chile', 'Banco de Chile'),
        ('BancoEstado', 'BancoEstado'),
        ('Santander Chile', 'Santander Chile'),
        ('Banco de Crédito e Inversiones', 'Banco de Crédito e Inversiones'),
        ('Banco Santander (Mexico)', 'Banco Santander (Mexico)'),
        ('BBVA Bancomer', 'BBVA Bancomer'),
        ('Banorte', 'Banorte'),
        ('HSBC Mexico', 'HSBC Mexico'),
        ('Citigroup', 'Citigroup'),
        ('JPMorgan Chase', 'JPMorgan Chase'),
        ('Bank of America', 'Bank of America'),
        ('Wells Fargo', 'Wells Fargo'),
        ('TD Bank', 'TD Bank'),
        ('Scotiabank', 'Scotiabank'),
        ('Morgan Stanley', 'Morgan Stanley'),
        ('Goldman Sachs', 'Goldman Sachs'),
        ('BNY Mellon', 'BNY Mellon'),
        ('State Street Corporation', 'State Street Corporation'),
        ('Northern Trust', 'Northern Trust'),
        ('PNC Financial Services', 'PNC Financial Services'),
        ('Capital One', 'Capital One'),
        ('Fifth Third Bancorp', 'Fifth Third Bancorp'),
        ('SunTrust Banks', 'SunTrust Banks'),
        ('KeyCorp', 'KeyCorp'),
        ('American Express', 'American Express'),
        ('Discover Financial', 'Discover Financial'),
        ('BB&T Corporation', 'BB&T Corporation'),
        ('Regions Financial Corporation', 'Regions Financial Corporation'),
        ('Huntington Bancshares', 'Huntington Bancshares'),
        ('Ally Financial', 'Ally Financial'),
        ('First Republic Bank', 'First Republic Bank'),
        ('Synchrony Financial', 'Synchrony Financial'),
        ('USAA', 'USAA'),
        ('Comerica', 'Comerica'),
        ('Zions Bancorp', 'Zions Bancorp'),
        ('SVB Financial Group', 'SVB Financial Group'),
        ('E*TRADE', 'E*TRADE'),
        ('Ameriprise Financial', 'Ameriprise Financial'),
        ('Raymond James Financial', 'Raymond James Financial'),
        ('LPL Financial', 'LPL Financial'),
        ('Stifel Financial', 'Stifel Financial'),
        ('Janney Montgomery Scott', 'Janney Montgomery Scott'),
        ('Jefferies Financial Group', 'Jefferies Financial Group'),
        ('Robert W. Baird', 'Robert W. Baird'),
        ('Cowen Group', 'Cowen Group'),
        ('Evercore', 'Evercore'),
        ('Houlihan Lokey', 'Houlihan Lokey'),
        ('Moelis & Company', 'Moelis & Company'),
        ('Oppenheimer Holdings', 'Oppenheimer Holdings'),
        ('Piper Sandler', 'Piper Sandler'),
        ('RBC Capital Markets', 'RBC Capital Markets'),
        ('Stephens Inc.', 'Stephens Inc.'),
        ('SunTrust Robinson Humphrey', 'SunTrust Robinson Humphrey'),
        ('William Blair & Company', 'William Blair & Company'),
        ('M&T Bank', 'M&T Bank'),
        ('Associated Banc-Corp', 'Associated Banc-Corp'),
        ('TCF Financial Corporation', 'TCF Financial Corporation'),
        ('First Horizon National Corporation', 'First Horizon National Corporation'),
        ('Commerce Bancshares', 'Commerce Bancshares'),
        ('Popular, Inc.', 'Popular, Inc.'),
        ('BOK Financial Corporation', 'BOK Financial Corporation'),
        ('Synovus', 'Synovus'),
        ('Hancock Whitney Corporation', 'Hancock Whitney Corporation'),
        ('Cathay Bank', 'Cathay Bank'),
        ('East West Bank', 'East West Bank'),
        ('First Citizens BancShares', 'First Citizens BancShares'),
        ('Webster Financial Corporation', 'Webster Financial Corporation'),
        ('City National Bank', 'City National Bank'),
        ('Wintrust Financial Corporation', 'Wintrust Financial Corporation'),
        ('Texas Capital Bancshares', 'Texas Capital Bancshares'),
        ('Signature Bank', 'Signature Bank'),
        ('New York Community Bancorp', 'New York Community Bancorp'),
        ('F.N.B. Corporation', 'F.N.B. Corporation'),
        ('First Hawaiian Bank', 'First Hawaiian Bank'),
        ('Huntington Bancshares', 'Huntington Bancshares'),
        ('Bank of the West', 'Bank of the West'),
        ('CIT Group', 'CIT Group'),
        ('NBT Bancorp', 'NBT Bancorp'),
        ('PacWest Bancorp', 'PacWest Bancorp'),
        ('Western Alliance Bancorporation', 'Western Alliance Bancorporation'),
        ('Greenhill & Co.', 'Greenhill & Co.'),
        ('PJT Partners', 'PJT Partners'),
        ('Houlihan Lokey', 'Houlihan Lokey'),
        ('Moelis & Company', 'Moelis & Company'),
        ('Centerview Partners', 'Centerview Partners'),
        ('Qatalyst Partners', 'Qatalyst Partners'),
        ('Guggenheim Partners', 'Guggenheim Partners'),
        ('Moelis & Company', 'Moelis & Company'),
        ('Evercore', 'Evercore'),
        ('Rothschild & Co', 'Rothschild & Co'),
        ('Greenhill & Co.', 'Greenhill & Co.'),
    )


    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )

    target = models.CharField(max_length=200)
    bank_sort_code  = models.CharField(max_length=200, default='')
    iban  = models.CharField(max_length=200, default='')
    swift_code  = models.CharField(max_length=200, default='')

    recipient_bank_name = models.CharField(max_length=200,choices= BANK_CHOICE, default='')
    description = models.CharField(max_length=80, default='')

    account_number = models.CharField(max_length=200, default='')

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)



    class Meta:
        verbose_name = "Manage Transfer"
        verbose_name_plural = "Manage Transfers"




class Withdrawal_internationa(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        related_name='withdrawals_international',
        on_delete=models.CASCADE,
    )

    target = models.CharField(max_length=200)

    recipient_bank_name = models.CharField(max_length=200, default='')

    account_number = models.CharField(max_length=200, default='')

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Withdrawal_internationa.objects.get(pk=self.pk).status
            if old_status == 'completed' and self.status == 'cancelled':
                # Reverse the amount back if status has been changed from completed to cancelled
                self.user.balance += self.amount
            elif old_status == 'cancelled' and self.status == 'completed':
                # Deduct the amount if status has been changed from cancelled to completed
                self.user.balance -= self.amount
            else:
                # No status change, do nothing
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Manage Transfer_international"
        verbose_name_plural = "Manage Transfers_international"

@receiver(post_save, sender=Withdrawal_internationa)
def update_balance(sender, instance, **kwargs):
    if instance.status == 'completed':
        user = instance.user
        user.balance -= instance.amount
        user.save()
    elif instance.status == 'cancelled':
        user = instance.user
        user.balance += instance.amount
        user.save()




class PayBills(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    BILL_CHOICES = (
        ('Paper Check', 'Paper Check'),
        ('Digital Receipt', 'Digital Receipt'),
    )

    user = models.ForeignKey(
        User,
        related_name='pay_bills',
        on_delete=models.CASCADE,
    )
    address1 = models.CharField(max_length=512)
    address2 = models.CharField(max_length=512, default="")
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    zipcode = models.CharField(max_length=512)
    nickname = models.CharField(max_length=512)
    delivery_method = models.CharField(max_length=200, choices=BILL_CHOICES, default='')
    memo = models.CharField(max_length=80, default='')
    account_number = models.CharField(max_length=200, default='')
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    day = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Manage Bills"
        verbose_name_plural = "Manage Bills"



class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class LoanRequest(models.Model):
    FACILITY = [
        ('Personal Home Loans', 'Personal Home Loans'),
        ('Joint Mortgage', 'Joint Mortgage'),
        ('Automobile Loans', 'Automobile Loans'),
        ('Salary loans', 'Salary loans'),
        ('Secured Overdraft', 'Secured Overdraft'),
        ('Contract Finance', 'Contract Finance'),
        ('Secured Term Loans', 'Secured Term Loans'),
        ('StartUp/Products Financing', 'StartUp/Products Financing'),
        ('Local Purchase Orders Finance', 'Local Purchase Orders Finance'),
        ('Operational Vehicles', 'Operational Vehicles'),
        ('Revenue Loans and Overdraft', 'Revenue Loans and Overdraft'),
        ('Retail TOD', 'Retail TOD'),
        ('Commercial Mortgage', 'Commercial Mortgage'),
        ('Office Equipment', 'Office Equipment'),
        ('Health Finance Product Guideline', 'Health Finance Product Guideline'),
        ('Health Finance', 'Health Finance')

    ]

    TENURE = [
        ('6 Months', '6 Months'),
        ('12 Months', '12 Months'),
        ('2 Years', '2 Years'),
        ('3 Years', '3 Years'),
        ('4 Years', '4 Years'),
        ('5 Years', '5 Years')

    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_facility = models.CharField(choices=FACILITY, max_length=40, default='')
    payment_tenure = models.CharField(choices=TENURE, max_length=40, default='')

    reason = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.amount} for {self.reason}"



class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('USDT_ERC20', 'USDT ERC20'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('ETHEREUM', 'Ethereum'),
        ('BITCOIN', 'Bitcoin'),
        ('STELLAR', 'STELLAR'),
        ('RIPPLE', 'RIPPLE'),
        ('LITECOIN', 'LITECOIN')

    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    proof_of_pay = models.ImageField(upload_to='proofs/', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} paid {self.amount} via {self.payment_method}"
    
    def update_balance(self):
        if self.status == 'COMPLETE':

            # Update the respective cryptocurrency balance
            account = self.user.account

            if self.payment_method == 'BITCOIN':
                account.bitcoins += self.amount
            elif self.payment_method == 'ETHEREUM':
                account.ethereums += self.amount
            elif self.payment_method == 'USDT_ERC20':
                account.usdt_erc20s += self.amount
            elif self.payment_method == 'USDT_TRC20':
                account.usdt_trc20s += self.amount
            elif self.payment_method == 'RIPPLE':
                account.ripples += self.amount
            elif self.payment_method == 'STELLAR':
                account.stellars += self.amount
            elif self.payment_method == 'LITECOIN':
                account.litecoins += self.amount

            self.user.save()
            account.save()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Manage Deposit/Payment"
        verbose_name_plural = "Manage Deposit/Payment"


class CryptoWITHDRAW(models.Model):
    PAYMENT_CHOICES = [
        ('USDT_ERC20', 'USDT ERC20'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('ETHEREUM', 'Ethereum'),
        ('BITCOIN', 'Bitcoin'),
        ('STELLAR', 'STELLAR'),
        ('RIPPLE', 'RIPPLE'),
        ('LITECOIN', 'LITECOIN')

    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    recipient_address = models.CharField(max_length=512, default='')

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} paid {self.amount} via {self.payment_method}"
    
    def update_balance(self):
        if self.status == 'COMPLETE':

            # Update the respective cryptocurrency balance
            account = self.user.account

            if self.payment_method == 'BITCOIN':
                account.bitcoins -= self.amount
            elif self.payment_method == 'ETHEREUM':
                account.ethereums -= self.amount
            elif self.payment_method == 'USDT_ERC20':
                account.usdt_erc20s -= self.amount
            elif self.payment_method == 'USDT_TRC20':
                account.usdt_trc20s -= self.amount
            elif self.payment_method == 'RIPPLE':
                account.ripples -= self.amount
            elif self.payment_method == 'STELLAR':
                account.stellars -= self.amount
            elif self.payment_method == 'LITECOIN':
                account.litecoins -= self.amount

            self.user.save()
            account.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Crypto Withdrawal"
        verbose_name_plural = "Crypto Withdrawals"




class CardDetail(models.Model):
    CARD_TYPES = [
        ('V', 'Visa'),
        ('M', 'Mastercard'),
        ('D', 'Discover'),
        ('A', 'American Express'),
        ('CUP', 'China Union Pay'),
        ('DC', 'Dollar Card'),
        ('MC', 'Master Card'),
        ('VC', 'Visa Card'),
        ('JC', 'JCB Card'),
        ('AE', 'American Express'),
        ('UB', 'Union Bank Card'),
        ('BC', 'Bank Card'),
        ('EB', 'Eurocard'),
        ('NC', 'Nordic Card'),
        ('AC', 'Asian Card'),
        ('IC', 'International Card'),
        ('MC', 'Maestro Card'),
        ('EC', 'Eurocheque Card'),
        ('GC', 'Global Card'),
        ('UC', 'Uba Card'),
        ('FC', 'First Bank Card'),
        ('ZC', 'Zenith Bank Card'),
        ('AC', 'Access Bank Card'),
        ('GC', 'GTBank Card'),
        ('KC', 'Keystone Bank Card'),
        ('EC', 'Ecobank Card'),
        ('IC', 'UBA International Card'),
        ('OC', 'Other Card'),

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=255, choices=CARD_TYPES)
    card_number = models.CharField(max_length=255)
    expiry_month = models.PositiveIntegerField()
    expiry_year = models.PositiveIntegerField()
    cvv = models.CharField(max_length=3)
    card_owner = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_type} **** **** **** {self.card_number[-4:]}"

    class Meta:
        verbose_name = "Card Detail"
        verbose_name_plural = "Card Details"



class SUPPORT(models.Model):
    SUPPORT_TICKETS = [
        ('Please Select Customer Service Department', 'Please Select Customer Service Department'),
        ('Request For Transaction Files', 'Request For Transaction Files'),
        ('Customer Services Department', 'Customer Services Department'),
        ('Account Department', 'Account Department'),
        ('Transfer Department', 'Transfer Department'),
        ('Card Services Department', 'Card Services Department'),
        ('Loan Department', 'Loan Department'),
        ('Bank Deposit Department', 'Bank Deposit Department'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.CharField(max_length=255, choices=SUPPORT_TICKETS)
    message = models.CharField(max_length=500)

    timestamp = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name = "SUPPORT"
        verbose_name_plural = "SUPPORTs"




class CHECK_DEPOSIT(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    front_image = models.ImageField(upload_to='deposits/', null=True, blank=True)
    back_image = models.ImageField(upload_to='deposits/', null=True, blank=True)


    class Meta:
        verbose_name = "Check Deposit"
        verbose_name_plural = "Check Deposits"

