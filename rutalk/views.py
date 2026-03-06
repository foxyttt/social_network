from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Comment
from .forms import PostForm, CustomUserCreationForm, CommentForm

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rutalk:feed')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})

def feed(request):
    form = PostForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('rutalk:feed')

    followed_posts = Post.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by('-created_at')
    return render(
        request,
        'rutalk/feed.html',
        {'form': form, 'posts': followed_posts},
    )

def dashboard(request):
    return render(request, 'rutalk/dashboard.html')

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'rutalk/profile_list.html', {'profiles': profiles})

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, 'rutalk/profile.html', {'profile': profile})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('rutalk:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'rutalk/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
