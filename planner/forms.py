from django import forms
from django.contrib.admin import widgets
from .models import Planner

class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = "__all__"
        
        widgets = {
            'plan_date': forms.widgets.DateInput(attrs={'type': 'date'}),
             "plan_time": widgets.AdminTimeWidget(attrs={'type': 'time'}),
             'plan_text': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
             
        }
    
   