from django import forms


class CalcForm(forms.Form):
    first = forms.IntegerField(label="Первое число", required=True)
    second = forms.IntegerField(label="Второе число", required=False)
