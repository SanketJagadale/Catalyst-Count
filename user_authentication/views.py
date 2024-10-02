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
#             login(request, user)
#             return redirect('home')
#         else:
#             return render(request, 'accounts/login.html', {'form': form})



from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from user_authentication.forms import SignUpForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import UserSerializer
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
                   
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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

class UserListView(APIView):
    """
    APIView for listing users, which can render HTML or return JSON.
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        # If the request accepts HTML (e.g., from a browser), return the HTML response
        if request.accepted_renderer.format == 'html':
            # Use `TemplateHTMLRenderer` for returning rendered templates
            return Response({'users': users}, template_name='account/user_list.html')
        
        # Otherwise, return JSON response
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data) 

class AddUserView(APIView):
    """
    APIView for adding a new user, with HTML form and API support.
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response(template_name='account/add_user.html')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'New user added')
            if request.accepted_renderer.format == 'html':
                return redirect('user_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If invalid data, return the form with errors for HTML or errors for API
        if request.accepted_renderer.format == 'html':
            return Response({'errors': serializer.errors}, template_name='account/add_user.html')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    """
    APIView for deleting a user, with HTML confirmation and API support.
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request, user_id, *args, **kwargs):
        # Fetch the user for the confirmation page
        user = get_object_or_404(User, id=user_id)
        # Render HTML confirmation page
        if request.accepted_renderer.format == 'html':
            return Response({'user': user}, template_name='account/user_list.html')
        # No API GET requests allowed for deletion
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, user_id, *args, **kwargs):
        # Delete the user via API or HTML form
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully!')
        # Redirect to user list after deletion if HTML
        if request.accepted_renderer.format == 'html':
            return redirect('user_list')
        # Return success message if API (JSON)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)