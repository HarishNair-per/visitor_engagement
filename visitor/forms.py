from django import forms
from .models import Visitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['vis_name','vis_address','vis_mobile',
                  'vis_email', 'vis_reason',
                  'vis_met','vis_remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
