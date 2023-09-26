from django.urls import path
from . import views

app_name = 'bill_share'

urlpatterns = [
    path('', views.StartView.as_view(), name='home'),
    path('generate_bill/<int:party_size>/<str:amount_due>/', views.GenerateBillView.as_view(), name='generate_bill'),
    path('results/', views.ResultsView.as_view(), name='results'),
]
