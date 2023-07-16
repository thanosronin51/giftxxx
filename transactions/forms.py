
from django import forms

from django import forms
from .models import *
from datetime import date

class SupportForm(forms.ModelForm):
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

    tickets = forms.ChoiceField(choices=SUPPORT_TICKETS, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Department'}))

    class Meta:
        model = SUPPORT
        fields = ['tickets', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['credit_facility', 'payment_tenure', 'reason', 'amount']
        widgets = {
            'credit_facility': forms.Select(attrs={'class': 'form-control'}),
            'payment_tenure': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class CardDetailsForm(forms.ModelForm):
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Card Number'}),
        error_messages={'required': 'Please enter your card number.'}
    )
    expiry_month = forms.ChoiceField(
        choices=[('', 'Month')] + [(str(month), str(month)) for month in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Please select the expiry month of your card.'}
    )

    expiry_year = forms.ChoiceField(
        choices=[('', 'Year')] + [(str(year), str(year)) for year in range(date.today().year, date.today().year + 10)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Please select the expiry year of your card.'}
    )

    cvv = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CVV'}),
        error_messages={'required': 'Please enter the CVV code.'}
    )
    card_owner = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Card Owner'}),
        error_messages={'required': 'Please enter the card owner name.'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card_type'].widget.attrs.update({'class': 'form-control custom-select card-type-select'})

    def as_card_type_field(self):
        card_type_field = self['card_type']
        card_type_field.field.widget = forms.Select(attrs={'class': 'form-control custom-select'})
        card_type_field.field.widget.choices = [('', 'Select Card Type')] + list(card_type_field.field.choices)[1:]
        return card_type_field

    class Meta:
        model = CardDetail
        fields = ('card_type', 'card_number', 'expiry_month', 'expiry_year', 'cvv', 'card_owner')


class CheckDepositForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    front_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        required=False
    )
    back_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        required=False
    )

    class Meta:
        model = CHECK_DEPOSIT
        fields = ['amount', 'front_image', 'back_image']

class PayBillsForm(forms.ModelForm):
    DAY_CHOICES = [(str(day), str(day)) for day in range(1, 32)]
    MONTH_CHOICES = [
        ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2022, 2032)]

    day = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = PayBills
        fields = ['address1', 'address2', 'city', 'state', 'zipcode', 'nickname', 'delivery_method', 'memo', 'account_number', 'amount']

        widgets = {
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address 1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter zipcode'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Payee name'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter memo'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number', 'pattern': '[0-9]*'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount', 'step': '0.01', 'min': '10.00'}),
        }

        labels = {
            'address1': 'Address 1',
            'address2': 'Address 2',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zipcode',
            'nickname': 'Nickname',
            'delivery_method': 'Delivery Method',
            'memo': 'Memo (Max 80 characters)',
            'account_number': 'Account Number',
            'amount': 'Amount',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.day = int(self.cleaned_data['day'])
        instance.month = int(self.cleaned_data['month'])
        instance.year = int(self.cleaned_data['year'])
        if commit:
            instance.save()
        return instance


class DepositForm(forms.ModelForm):
    class Meta:
        model = Diposit
        fields = ["amount"]

class WithdrawalForm(forms.ModelForm):
    BANK_CHOICE = [
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
    ]

    recipient_bank_name = forms.ChoiceField(
        choices=BANK_CHOICE,
        label='Recipient Bank Name',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Withdrawal
        fields = [
            'target',
            'bank_sort_code',
            'iban',
            'swift_code',
            'recipient_bank_name',
            'description',
            'account_number',
            'amount',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})






class WithdrawalInternationalForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, required=True)
    target_account_number = forms.CharField(max_length=20, required=True)
    target_bank_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Withdrawal_internationa
        fields = ["amount", "target_account_number", "target_bank_name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalInternationalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You cannot withdraw more than your available balance.'
            )

        return amount

    def clean_target_account_number(self):
        target_account_number = self.cleaned_data['target_account_number'].strip()
        return target_account_number

    def clean_target_bank_name(self):
        target_bank_name = self.cleaned_data['target_bank_name'].strip()
        return target_bank_name



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'proof_of_pay']

class CryptoWITHDRAWForm(forms.ModelForm):
    class Meta:
        model = CryptoWITHDRAW
        fields = ['payment_method', 'amount', 'recipient_address']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'recipient_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def has_error(self, field_name):
        return self[field_name].errors

    def get_error(self, field_name):
        return self[field_name].errors.as_text()


class Client_USDTerc20Form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField()



class Client_Trc20_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()

class Client_Bitcoin_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()


class Client_Ethereum_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()
