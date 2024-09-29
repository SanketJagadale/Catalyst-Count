# import sys
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from django.contrib.auth import login
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from .serializers import SignUpSerializer

# class AuthenticateViewSet(viewsets.ModelViewSet):
#     def register(self,request):
#         try:
#             username = request.data['username']
#             if User.objects.filter(username=username).exists():
#                 raise serializers.ValidationError({'msg': 'Username already exists!'})
#             serializer = SignUpSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.save()
#                 # Log in the user after successful signup
#                 login(request, user)
#                 # Redirect to the home page or another desired page
#                 return redirect('home')
#             else:
#                 # If form is invalid, re-render the form with errors
#                 return render(request, 'account/signup.html', {'serializer': serializer.errors})
#             return render(request, 'account/signup.html', {'serializer': serializer.data})
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             line_no = exc_tb.tb_lineno
#             filename = exc_tb.tb_frame.f_code.co_filename
#             err_msg = f"Exception occurred at line {line_no} in file {filename}: {e}"
#             # print("Exception Error\n",err_msg)
#             return render(request, 'account/signup.html', {'error': err_msg})

#     def login(self,request):
#         pass

# class SignUpView(APIView):
#     def get(self, request):
#         # Render the form on GET request
#         form = SignUpSerializer()
#         return render(request, 'accounts/login.html', {'form': form})

#     def post(self, request):
#         form = SignUpSerializer(data=request.data)
#         if form.is_valid():
#             user = form.save()
#             # Log in the user after successful signup
#             login(request, user)
#             # Redirect to the home page or another desired page
#             return redirect('home')
#         else:
#             # If form is invalid, re-render the form with errors
#             return render(request, 'accounts/login.html', {'form': form})



from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from user_authentication.forms import SignUpForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()   

            # Add user to the 'Customers' group
            customers_group, created = Group.objects.get_or_create(name='Customers')
            user.groups.add(customers_group)
                   
            login(request, user)
            return redirect('home')
    else:
        form=SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')

    
@login_required
def signout(request):
    logout(request)
    return redirect('login')