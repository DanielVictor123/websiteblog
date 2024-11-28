from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post  # Ensure you import your Post model
from django.shortcuts import get_object_or_404

# Create your views here.

#Home View
def home(request):
    recent_posts = Post.objects.order_by('-created_at')[:3]  # Get the 3 most recent posts
    return render(request, 'home.html', {'recent_posts': recent_posts})

# Registration view
ADMIN_USERNAMES = ['admin1', 'admin2']

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, prefix='user')
        admin_form = UserCreationForm(request.POST, prefix='admin')

        if 'user-username' in request.POST:
            if user_form.is_valid():
                user_form.save()
                return redirect('login')
        elif 'admin-username' in request.POST:
            if admin_form.is_valid() and request.POST['admin-username'] in ADMIN_USERNAMES:
                admin_form.save()
                return redirect('login')
    else:
        user_form = UserCreationForm(prefix='user')
        admin_form = UserCreationForm(prefix='admin')

    return render(request, 'registration/register.html', {'user_form': user_form, 'admin_form': admin_form})

# Login view
def login_view(request):
    if request.method == 'POST':
        user_form = AuthenticationForm(request, data=request.POST, prefix='user')
        admin_form = AuthenticationForm(request, data=request.POST, prefix='admin')

        if 'user-username' in request.POST:
            if user_form.is_valid():
                user = user_form.get_user()
                login(request, user)
                return redirect('blog_list')
        elif 'admin-username' in request.POST:
            if admin_form.is_valid():
                user = admin_form.get_user()
                login(request, user)
                return redirect('admin_dashboard')
    else:
        user_form = AuthenticationForm(request, prefix='user')
        admin_form = AuthenticationForm(request, prefix='admin')

    return render(request, 'registration/login.html', {'user_form': user_form, 'admin_form': admin_form})


# Logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to a homepage or another page


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
