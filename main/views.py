from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse
from django.forms import formset_factory
from django.http import HttpResponseServerError
from . import forms
from .pdf_generator import generate_pdf


class StartView(generic.FormView):
    """
    Display the start page with a form that prompts the user to enter the size
    of the party sharing the bill as well as the total amount to split.
    """
    template_name = 'main/index.html'
    form_class = forms.PartySizeForm

    def form_valid(self, form):
        """
        Stores the party_size and bill_amount taken from the form and sends them
        to the page that will calculate each person's share.
        :param form: The form that takes the party_size and bill_amount
        :return: Redirect to the generate_bill page with the party_size and
        amount_due stored as context arguments.
        """
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
    """
    Display the generate_bill page with forms to enter the names of each party
    member as well as the number of days each person spent on the property. The
    number of forms corresponds to the party_size.
    """
    template_name = 'main/generate_bill.html'

    def get(self, request, party_size, amount_due):
        """
        Display party_size number of forms in which party members are prompted
        to enter their names and the number of days spent at the property.
        :param request: GET request
        :param party_size: Integer received from the party_size field in the
        PartySizeForm.
        :param amount_due: Float received from the bill_amount field in the
        PartySizeForm.
        :return: Render the forms on the generate_bill page.
        """
        party_member_form_set = formset_factory(forms.PartyMemberForm, extra=party_size)
        formset = party_member_form_set()

        return render(
            request,
            self.template_name,
            {
                'formset': formset,
                'amount_due': amount_due,
            }
        )

    def post(self, request, party_size, amount_due):
        """
        Validates the set of forms and calculates how much each party member owes
        towards the amount_due based on the party_size, the total_days_spent by
        all party members, and each party member's days_spent at the location.
        :param request: POST request
        :param party_size: Integer received from the party_size field in the
        PartySizeForm.
        :param amount_due: Float received from the bill_amount field in the
        PartySizeForm.
        :return: If forms are valid, redirect to the Results page to display how
        much each person owes, otherwise display an error message
        """
        party_member_form_set = formset_factory(
            forms.PartyMemberForm,
            extra=party_size
        )

        formset = party_member_form_set(request.POST)

        if formset.is_valid():
            amount_due = float(amount_due)
            total_days_spent = sum(int(form.cleaned_data.get('days_spent', 0)) for form in formset)
            party_members = []

            for form in formset:
                name = form.cleaned_data.get('name', '')
                days_spent = int(form.cleaned_data.get('days_spent', 0))
                share_amount = round((days_spent / total_days_spent) * amount_due, 2)
                form.share_amount = share_amount

                party_members.append({
                    'name': name,
                    'share_amount': share_amount,
                })

            self.request.session['party_members'] = party_members
            self.request.session['total_billing_amount'] = amount_due

            return redirect(reverse('bill_share:results'))

        return HttpResponseServerError('Form data is invalid.')


class ResultsView(generic.TemplateView):
    """
    Display each party member's name and how much they owe towards the total.
    Include a link to download a pdf of this data as well.
    """
    template_name = 'main/results.html'

    def get_context_data(self, **kwargs):
        """
        Store all party member data in the session along with the total amount
        due.
        :param kwargs:
        :return: A list of all stored party members (including their names and
        amounts owing) and the total amount due for the billing period.
        """
        context = super().get_context_data()
        party_members = self.request.session.get('party_members', [])
        total_billing_amount = self.request.session.get('total_billing_amount', 0)

        context['party_members'] = party_members
        context['total_billing_amount'] = total_billing_amount

        return context


class GeneratePDFView(View):
    def get(self, request):
        party_members = request.session.get('party_members', [])
        total_billing_amount = request.session.get('total_billing_amount', 0)

        pdf_response = generate_pdf(party_members, total_billing_amount)
        return pdf_response
