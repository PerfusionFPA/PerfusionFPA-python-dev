from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from get_inputs.models import GetInputs
from . import views

urlpatterns = [ url(r'^$', ListView.as_view(queryset=GetInputs.objects.all().order_by("-date")[:25],
                                          template_name="get_inputs/list_inputs.html")),
                url(r'^(?P<pk>\d+)$', DetailView.as_view(model=GetInputs,
                                                         template_name='get_inputs/cur_input.html')),
                url(r'manual_input/', views.home, name='home'),
                ]

