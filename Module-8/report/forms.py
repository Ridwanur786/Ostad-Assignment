from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['item_name', 'type', 'category', 'description', 'location', 'date', 'contact_info', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class SearchFilterForm(forms.Form):
    search = forms.CharField(required=False, label='Item Name')
    type = forms.ChoiceField(choices=[('', 'All')] + Report.REPORT_TYPES, required=False)
    category = forms.CharField(required=False)
    status = forms.ChoiceField(choices=[('', 'All')] + Report.STATUS_CHOICES, required=False)