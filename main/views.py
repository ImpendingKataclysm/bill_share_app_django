from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse
from django.forms import formset_factory
from . import forms


class StartView(generic.FormView):
    template_name = 'main/index.html'
    form_class = forms.PartySizeForm

    def form_valid(self, form):
        party_size = form.cleaned_data['party_size']
        amount_due = form.cleaned_data['bill_amount']

        return redirect(
            reverse(
                'bill_share:generate_bill',
                kwargs={
                    'party_size': party_size,
                    'amount_due': amount_due,
                }
            )
        )


class GenerateBillView(View):
    template_name = 'main/generate_bill.html'

    def get(self, request, party_size, amount_due):
        PartyMemberFormSet = formset_factory(forms.PartyMemberForm, extra=party_size)
        formset = PartyMemberFormSet()

        return render(
            request,
            self.template_name,
            {
                'formset': formset,
                'amount_due': amount_due,
            }
        )

    def post(self, request, party_size, amount_due):
        PartyMemberFormSet = formset_factory(forms.PartyMemberForm, extra=party_size)
        formset = PartyMemberFormSet(request.POST)

        if formset.is_valid():
            amount_due = float(amount_due)
            for form in formset:
                days_spent = int(form.cleaned_data.get('days_spent', 0))
                share_amount = (days_spent / amount_due) * amount_due
                form.share_amount = share_amount

        return render(
            request,
            self.template_name,
            {
                'formset': formset,
                'amount_due': amount_due
            }
        )
