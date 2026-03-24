from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Comment, Group, Membership
from .forms import PostForm, CustomUserCreationForm, CommentForm, GroupForm, ProfileForm

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
    groups = Group.objects.filter(
        memberships__user=request.user
    ).order_by('-created_at')
    return render(
        request,
        'rutalk/feed.html',
        {'groups': groups},
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
        form = CommentForm(request.POST, request.FILES)
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

def group_list(request):
    groups = Group.objects.all().order_by('-created_at')
    return render(request, 'rutalk/group_list.html', {'groups' : groups})

def group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    is_member = Membership.objects.filter(user=request.user, group=group).exists()
    posts = group.posts.all().order_by('-created_at')

    if request.method == 'POST' and is_member:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.group = group
            post.save()
            return redirect('rutalk:group', pk=group.pk)
    else:
        form = PostForm() if is_member else None

    return render(request, 'rutalk/group.html', {
        'group': group,
        'is_member': is_member,
        'posts': posts,
        'form': form,
    })

def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            Membership.objects.create(user=request.user, group=group)
            return redirect('rutalk:group', pk=group.pk)
    else:
        form = GroupForm()
    return render(request, 'rutalk/group_form.html', {'form': form})

def group_join(request, pk):
    group = get_object_or_404(Group, pk=pk)
    Membership.objects.get_or_create(user=request.user, group=group)
    return redirect('rutalk:group', pk=group.pk)

def group_leave(request, pk):
    group = get_object_or_404(Group, pk=pk)
    Membership.objects.filter(user=request.user, group=group).delete()
    return redirect('rutalk:feed')

def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('rutalk:profile', pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'rutalk/edit_profile.html', {'form': form})
