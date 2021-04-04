from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Customer

import json
# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    customers = Customer.objects.filter(owner=request.user)
    get_company = []
    average_income = sum([i.income_int for i in customers])/len(customers) if len(customers) >= 1 else 0
    average_age = sum([i.age for i in customers])/len(customers) if len(customers) >= 1 else 0
    for cus in customers:
        if cus.company_name not in get_company:
            get_company.append(cus.company_name)
    context ={
        'customers': customers,
        'total_customers': len(customers),
        'average_income': "Rp{:,.2f}".format(average_income),
        'average_age': "{:,.1f}".format(average_age),
        'total_company': len(get_company)
    }
    return render(request, 'customer/index.html', context)


def search_customer(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        customers = Customer.objects.filter(
            first_name__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            middle_name__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            last_name__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            address__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            company_name__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            phone_number__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            gender__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            status__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            age__istartswith=search_str, owner=request.user) | Customer.objects.filter(
            income_int__istartswith=search_str, owner=request.user)
        data = customers.values()
        return JsonResponse(list(data), safe=False)



def add_customer(request):
    customers = Customer.objects.all()

    if request.method == 'POST': 
        Customer.objects.create(
            owner=request.user,
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            address=request.POST['address'],
            company_name=request.POST['company_name'],
            phone_number=request.POST['phone_number'],
            gender=request.POST['gender'],
            status=request.POST['status'],
            age=request.POST['age'],
            income_int=int(request.POST['income']) if request.POST['income'] else 0,
            income=int(request.POST['income']) if request.POST['income'] else 0,
            )
        messages.success(request, 'Customer save successfully.')
        return redirect('customer')

    return render(request, 'customer/add_customer.html')   

def edit_customer(request, id):
    customer = Customer.objects.get(pk=id)
    context ={
        'customer': customer,
        'values': customer,
    }
    if request.method == "GET":
        return render(request, 'customer/edit_customer.html', context)

    elif request.method == 'POST':      
        customer.first_name = request.POST['first_name']
        customer.middle_name = request.POST['middle_name']
        customer.last_name = request.POST['last_name']
        customer.address = request.POST['address']
        customer.company_name = request.POST['company_name']
        customer.phone_number = request.POST['phone_number']
        customer.gender = request.POST['gender']
        customer.status = request.POST['status']
        customer.age = request.POST['age']
        customer.income_int=int(request.POST['income']) if request.POST['income'] else 0
        customer.income = int(request.POST['income']) if request.POST['income'] else 0

        customer.save()
        
        messages.success(request, 'Customer update successfully.')
        return redirect('customer')

    return render(request, 'customer/edit_customer.html', context)

def delete_customer(request, id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    messages.success(request, 'Customer removed.')
    return redirect('customer')


def customer_summary(request):
    customers = Customer.objects.filter(owner=request.user)
    age_income_data = [['Age', 'Income']]
    gender_data = [['Gender', 'Total'],['Male', 0], ['Female', 0]]
    get_data_age_income ={}
    for customer in customers:
        if customer.age not in get_data_age_income:
            get_data_age_income[customer.age] = []
        get_data_age_income[customer.age].append(customer.income_int)

        if customer.gender == 'Male': 
            gender_data[1][1] += 1
        else:
            gender_data[2][1] += 1

    for key, value in get_data_age_income.items():
        average_income = sum(value)/len(value) if value else 0
        currency_string = "Rp{:,.2f}".format(average_income)
        data = [key, {'v': average_income, 'f': currency_string}]
        age_income_data.append(data)

    return JsonResponse({'age_income_data': age_income_data, 'gender_data': gender_data}, safe=False)

