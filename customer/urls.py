from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="customer"),
    path('add-customer', views.add_customer, name='add-customer'),
    path('edit-customer/<int:id>', views.edit_customer, name='edit-customer'),
    path('delete-customer/<int:id>', views.delete_customer, name='delete-customer'),
    path('search-customer', csrf_exempt(views.search_customer), name='search-customer'),
    path('customer_summary', views.customer_summary, name='customer_summary')
]
