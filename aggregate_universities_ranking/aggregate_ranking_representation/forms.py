from django import forms

class SelectRaitingsNames(forms.Form):
    select_raitings_names_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=())
