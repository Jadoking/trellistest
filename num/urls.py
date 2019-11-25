from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^num_to_english/$', views.NumToWordsView.as_view(), name='english'),
]
