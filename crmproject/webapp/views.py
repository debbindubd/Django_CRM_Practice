from django.shortcuts import render, redirect
from django.http import HttpResponse
from webapp.forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from webapp.models import Record

from django.contrib import messages

# Create your views here.

def home(request):
    # return HttpResponse("HEllow World")
    return render(request, 'webapp/index.html', {})

def register(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('my_login')

    diction = {'register_form': register_form}
    return render(request, 'webapp/register-page.html', context=diction)

# - Login a user 
def my_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request, data = request.POST)

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You have logged!')
                return redirect('dashboard')

    diction = {'login_form': login_form}
    return render(request, 'webapp/login-page.html', context=diction)


# -  Dashboard
@login_required(login_url='my_login')
def dashboard(request):
    my_records = Record.objects.all()

    diction = {'my_records': my_records}
    return render(request, 'webapp/dashboard.html', context=diction)


# - Create a record
@login_required(login_url='my_login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Record was created successfully!')
            return redirect('dashboard')
    return render(request, 'webapp/create-record.html', {'form':form})

# - Update a record 
@login_required(login_url='my_login')

def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your record Updated successfully!')
            return redirect('dashboard')
    return render(request, 'webapp/update-record.html', {'form':form})



# Read / view a single record
@login_required(login_url='my_login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    return render(request, 'webapp/view-record.html', {'record':all_records})


# Delete a record 
@login_required(login_url='my_login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, 'Record Deleted successfully!')
    return redirect('dashboard')

# Logout a user
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'You haved logged Out!')
    return redirect('my_login')
