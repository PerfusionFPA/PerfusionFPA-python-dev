from django import forms
from .models import GetInputs

class GetInputsForm(forms.ModelForm):
    class Meta:
        model = GetInputs
        fields = [
            'patient',
            'date',
            'vol1_dcm_path',
            'vol2_dcm_path',
            'vol_seg_dcm_path',
            ]

    def clean(self):
        cleaned_data = super(GetInputsForm, self).clean()
        patient = cleaned_data.get('patient')
        date = cleaned_data.get('date')
        vol1_dcm_path = cleaned_data.get('vol1_dcm_path')
        vol2_dcm_path = cleaned_data.get('vol2_dcm_path')
        vol_seg_dcm_path = cleaned_data.get('vol_seg_dcm_path')
        
        
