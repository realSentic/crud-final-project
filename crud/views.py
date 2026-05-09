from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Genders, Users, Admins
from .forms import RegisterForm, LoginForm


# Create your views here.


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        admin = form.save(commit=False)
        admin.password = make_password(form.cleaned_data['password'])
        admin.save()
        messages.success(request, 'Registration successful!')
        return redirect('login')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
    return render(request, 'signing/register.html', {'form': form})



def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        try:
            admin = Admins.objects.get(username=username)
            if check_password(password, admin.password):
                request.session['admin_id'] = admin.admin_id
                request.session['admin_username'] = admin.username
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        except Admins.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'signing/login.html', {'form': form})  # ← was missing form here

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard:

def dashboard(request):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        total_users = Users.objects.count()
    
        gender_stats = Users.objects.values('gender__gender').annotate(count=Count('gender'))

        ratios = []
        for stat in gender_stats:
            name = stat['gender__gender']
            count = stat['count']
            percentage = (count / total_users) * 100 if total_users > 0 else 0
            ratios.append({
                'name': name,
                'percentage': round(percentage, 1),
                'count': count
            })

        context = {
            'user_count': total_users,
            'gender_count': Genders.objects.count(),
            'newest_user': Users.objects.order_by('-pk').first(),
            'gender_ratios': ratios
        }

        return render(request, 'dashboard/Dashboard.html', context)
    
    except Exception as e:
        return HttpResponse(f"Error: {e}")

# Gender:

def gender_list(request):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        genders = Genders.objects.all()

        context = {
            'genders': genders
        }

        return render(request, 'gender/GenderList.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def add_gender(request):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('gender_add')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def update_gender(request, id):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        gender = Genders.objects.get(gender_id=id)

        if request.method == 'POST':
            gender.gender = request.POST.get('gender')
            gender.save()
            messages.success(request, 'Gender updated successfully!')
            return redirect('gender_list')
        else:
            return redirect('gender_list')
        
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def delete_gender(request, id):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        gender = Genders.objects.get(gender_id=id)

        if request.method == 'POST':
            gender.gender = request.POST.get('gender')
            gender.delete()
            messages.success(request, 'Gender deleted successfully!')
            return redirect('gender_list')
        else:
            return redirect('gender_list')
        
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

# Users:

def user_list(request):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        users = Users.objects.all()
        genders = Genders.objects.all() 
        paginator = Paginator(users, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'users': page_obj,
            'genders': genders, 
        }

        return render(request, 'user/UserList.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def add_user(request):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender_id = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                genders = Genders.objects.all()
                return render(request, 'user/AddUser.html', {'genders': genders})

            gender = Genders.objects.get(gender_id=gender_id)

            Users.objects.create(
                full_name=full_name,
                gender=gender,
                birth_date=birth_date,
                address=address,
                contact_number=contact_number,
                email=email,
                username=username,
                password=password,
                profile_picture=request.FILES.get('profile_picture')
            )

            messages.success(request, 'User added successfully!')
            return redirect('user_list')
        else:
            genders = Genders.objects.all()
            return render(request, 'user/AddUser.html', {'genders': genders})
    except IntegrityError:
        messages.error(request, 'Username already exists!')
        genders = Genders.objects.all()
        return render(request, 'user/AddUser.html', {'genders': genders})
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def update_user(request, id):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        user = Users.objects.get(user_id=id)

        if request.method == 'POST':
            user.full_name = request.POST.get('full_name')
            user.gender = Genders.objects.get(gender_id=request.POST.get('gender'))
            user.birth_date = request.POST.get('birth_date')
            user.address = request.POST.get('address')
            user.contact_number = request.POST.get('contact_number')
            user.email = request.POST.get('email')
            user.username = request.POST.get('username')

            if request.POST.get('remove_profile_picture') == '1':
                user.profile_picture = None
            elif request.FILES.get('profile_picture'):
                user.profile_picture = request.FILES.get('profile_picture')

            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            if old_password and new_password:
                if user.password == old_password:
                    user.password = new_password
                else:
                    messages.error(request, 'Old password is incorrect!')
                    return redirect('user_list')

            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_list')
        else:
            return redirect('user_list')
    except IntegrityError:
        messages.error(request, 'Username already exists!')
        return redirect('user_list')
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def delete_user(request, id):
    try:
        if not request.session.get('admin_id'):
            return redirect('login')
        
        user = Users.objects.get(user_id=id)

        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('user_list')
        else:
            return redirect('user_list')
        
    except Exception as e:
        return HttpResponse(f"Error: {e}")