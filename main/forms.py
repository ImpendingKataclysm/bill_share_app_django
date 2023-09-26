from django import forms


class PartySizeForm(forms.Form):
    party_size = forms.IntegerField(
        label='Party Size',
        min_value=1,
        max_value=10,
    )

    bill_amount = forms.DecimalField(
        label='Total Amount Due:',
        max_digits=10,
        decimal_places=2,
    )


class PartyMemberForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name'
    )
    days_spent = forms.IntegerField(
        max_value=366,
        min_value=1,
        label='Days Spent'
    )
