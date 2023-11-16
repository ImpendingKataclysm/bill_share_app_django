from django import forms


class PartySizeForm(forms.Form):
    party_size = forms.IntegerField(
        label='Party Size:',
        min_value=1,
        max_value=10,
        widget=forms.NumberInput({
            'class': 'form-control',
            'placeholder': 'Enter party size'
        })
    )

    bill_amount = forms.DecimalField(
        label='Total Amount Due:',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput({
            'class': 'form-control',
            'placeholder': 'Enter amount due'
        })
    )


class PartyMemberForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name:',
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Enter name'
        })
    )
    days_spent = forms.IntegerField(
        max_value=366,
        min_value=1,
        label='Days Spent:',
        widget=forms.NumberInput({
            'class': 'form-control',
            'placeholder': 'Enter days spent'
        })
    )
