from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import GetInputsForm
from .models import GetInputs

from pprint import pprint

# Create your views here.
 
def home(request):
    title = 'Welcome'
    if request.method == 'POST':
        form = GetInputsForm(request.POST)
        if form.is_valid():
            cur_patient = request.POST.get('patient', '')
            cur_date = request.POST.get('date', '')
            cur_vol1_dcm_path = request.POST.get('vol1_dcm_path', '')
            cur_vol2_dcm_path = request.POST.get('vol2_dcm_path', '')
            cur_vol_seg_dcm_path = request.POST.get('vol_seg_dcm_path', '')
            get_inputs_obj = GetInputs(patient=cur_patient,
                                       date=cur_date,
                                       vol1_dcm_path=cur_vol1_dcm_path,
                                       vol2_dcm_path=cur_vol2_dcm_path,
                                       vol_seg_dcm_path=cur_vol_seg_dcm_path)
            get_inputs_obj.save()
            return HttpResponseRedirect('/')
                                       
    
        pprint(form)
    else:
        form = GetInputsForm()

    return render(request, "get_inputs/manual_input.html", {'form' : form})

