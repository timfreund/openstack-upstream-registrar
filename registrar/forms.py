from django import forms

__all__ = [
    'StaffRegistrationForm',
    'StudentRegistrationForm',
]

class StudentRegistrationForm(forms.Form):
    name = forms.CharField(required=True, max_length=128)
    email = forms.EmailField(required=True)
    organization = forms.CharField(required=False, max_length=128)
    title = forms.CharField(required=False, max_length=128)
    # areas_of_interest = forms.MultipleChoiceField(choices=['One choice', 'another choice'])
    # openstack_role = forms.MultipleChoiceField(choices=['Documentation Writer', 'Operator', 'Software Developer', 'Testing', 'Hardcoding is bad, mkay'])
    professional_experience = forms.CharField(widget=forms.widgets.Textarea)
    open_source_experience = forms.CharField(widget=forms.widgets.Textarea)
    training_goal = forms.CharField(widget=forms.widgets.Textarea)
    irc_nick = forms.CharField(required=False, max_length=128)
    # dietary_restrictions = forms.MultipleChoiceField(choices=['One choice', 'another choice'])
    
class StaffRegistrationForm(forms.Form):
    name = forms.CharField(required=True, max_length=128)
    email = forms.EmailField(required=True)
    organization = forms.CharField(required=False, max_length=128)
    title = forms.CharField(required=False, max_length=128)
    # areas_of_interest = forms.MultipleChoiceField(choices=['One choice', 'another choice'])
    irc_nick = forms.CharField(required=False, max_length=128)
    
