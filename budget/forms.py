from django import forms


class ExpenseForm(forms.Form):
    date = forms.DateField()
    description = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()
    user = forms.CharField()
