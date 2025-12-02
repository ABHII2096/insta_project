from django.shortcuts import render,redirect, get_object_or_404 
from .forms import PostForm
from .models import Post14 , Comment
from .forms import CommentForm
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from Myapp.models import Post14 as Post, Follow
from .models import profile as ProfileModel
from django.contrib.auth import authenticate, login

 




def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'Myapp/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'Myapp/register.html')
        
        # Create user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'Myapp/register.html')




def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Myapp/login.html', {'error': 'Invalid credentials'})

    return render(request, 'Myapp/login.html')



@login_required
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

 
    posts = Post14.objects.all().order_by('-created_at').prefetch_related('comments', 'likes')

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'Myapp/index.html', context)



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'likes': post.total_likes()})
    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post14, id=post_id)

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)

    return redirect('home')


@login_required
def profile(request):
    user_profile = request.user
    posts = Post.objects.filter(user=user_profile)
    followers_count = Follow.objects.filter(following=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()

    if request.method == 'POST':
        user_profile.username = request.POST.get('username')
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.profile.bio = request.POST.get('bio')
        if 'profile_pic' in request.FILES:
            user_profile.profile.profile_pic = request.FILES['profile_pic']
        user_profile.save()
        user_profile.profile.save()
        return redirect('profile')

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'Myapp/profile.html', context)


def delete_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('home')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Message sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "Myapp/contactus.html", {"form": form})

@login_required
def profile_view(request, username=None):

    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    # FIXED: get the actual object, not a queryset
    user_profile = ProfileModel.objects.filter(user=user_obj).first()

    posts = Post14.objects.filter(user=user_obj).order_by('-id')

    followers_count = Follow.objects.filter(following=user_obj).count()
    following_count = Follow.objects.filter(follower=user_obj).count()

    is_following = False
    if request.user != user_obj:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    context = {
        'user_obj': user_obj,
        'profile': user_profile,   # fixed
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'Myapp/profile_view.html', context)


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

    if not created:
        follow_obj.delete()  

    return redirect('profile_view', username=username)


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)
    # Save report
    Report.objects.create(user=request.user, post=post)
    return redirect('home')
