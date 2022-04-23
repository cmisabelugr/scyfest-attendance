from email.policy import default
from django import forms

from .models import Ticket

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["name", "has_tui", "from_college", "checkedin", "active", ]

class TicketPureForm(forms.Form):
    name = forms.CharField()
    has_tui = forms.BooleanField(initial=True, required=False)
    from_college = forms.BooleanField(initial=False, required=False)
    checkedin = forms.BooleanField(initial=True, required=False)
    active = forms.BooleanField(initial=True, required=False)
    profile_picture = forms.ImageField(required=False)


