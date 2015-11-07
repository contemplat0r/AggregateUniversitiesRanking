from django import forms

class SelectRankingsNamesAndYear(forms.Form):
    select_rankings_names_field = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=())
    select_year_field = forms.ChoiceField(widget=forms.Select, choices=())
