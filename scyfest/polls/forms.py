from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from .models import Option, Poll, Vote

class VoteForm (ModelForm):
    class Meta:
        model = Vote
        fields = ('options',)
        widgets = {
            'options': CheckboxSelectMultiple()
        }

    def __init__(self, poll, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['options'].queryset = Option.objects.filter(poll=poll)
        self.fields['options'].label_from_instance = self.label_from_instance
        self.initial['poll']=poll
        self.instance.poll=poll

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.option_text