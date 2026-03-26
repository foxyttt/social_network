from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Group, Membership, ChannelMembership, Channel
from .forms import (
    PostForm, CustomUserCreationForm, CommentForm, GroupForm, ProfileForm, ChannelForm
)


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


@login_required
def feed(request):
    groups = Group.objects.filter(memberships__user=request.user).order_by('-created_at')
    channels = Channel.objects.filter(memberships__user=request.user).order_by('-created_at')
    return render(request, 'rutalk/feed.html', {'groups': groups, 'channels': channels})


def dashboard(request):
    return render(request, 'rutalk/dashboard.html')


@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'rutalk/profile_list.html', {'profiles': profiles})


@login_required
def profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        action = request.POST.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, 'rutalk/profile.html', {'profile': profile})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('rutalk:post_detail', pk=post.pk)

    target_group = getattr(post, 'group', None)
    is_channel = bool(getattr(target_group, 'is_channel', False)) if target_group else False

    if target_group:
        if is_channel:
            try:
                back_url = reverse('rutalk:channel_detail', args=[target_group.pk])
            except Exception:
                back_url = reverse('rutalk:group', args=[target_group.pk])
        else:
            back_url = reverse('rutalk:group', args=[target_group.pk])
    else:
        back_url = reverse('rutalk:feed')

    back_label = 'Назад'
    post_text = getattr(post, 'body', '')
    comment_items = [{'obj': comment, 'text': getattr(comment, 'body', '')} for comment in comments]

    context = {
        'post': post,
        'post_text': post_text,
        'comment_items': comment_items,
        'comment_form': comment_form,
        'back_url': back_url,
        'back_label': back_label,
    }
    return render(request, 'rutalk/post_detail.html', context)
def group_list(request):
    groups = Group.objects.all().order_by('-created_at')
    channels = Channel.objects.all().order_by('-created_at')
    return render(request, 'rutalk/group_list.html', {'groups': groups, 'channels': channels})


@login_required
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

    return render(request, 'rutalk/group.html', {'group': group, 'is_member': is_member, 'posts': posts, 'form': form})


@login_required
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


@login_required
def group_join(request, pk):
    group = get_object_or_404(Group, pk=pk)
    Membership.objects.get_or_create(user=request.user, group=group)
    return redirect('rutalk:group', pk=group.pk)


@login_required
def group_leave(request, pk):
    group = get_object_or_404(Group, pk=pk)
    Membership.objects.filter(user=request.user, group=group).delete()
    return redirect('rutalk:group_list')


@login_required
def channel_detail(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    is_member = ChannelMembership.objects.filter(user=request.user, channel=channel).exists()
    posts = channel.posts.all().order_by('-created_at')
    can_create_post = request.user == channel.owner

    if request.method == 'POST' and can_create_post:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.channel = channel
            post.save()
            return redirect('rutalk:channel_detail', pk=channel.pk)
    else:
        form = PostForm() if can_create_post else None

    return render(request, 'rutalk/channel_detail.html', {
        'channel': channel,
        'is_member': is_member,
        'posts': posts,
        'form': form,
        'can_create_post': can_create_post,
    })


@login_required
def channel_join(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    ChannelMembership.objects.get_or_create(user=request.user, channel=channel)
    return redirect('rutalk:channel_detail', pk=channel.pk)


@login_required
def channel_leave(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    ChannelMembership.objects.filter(user=request.user, channel=channel).delete()
    return redirect('rutalk:group_list')


@login_required
def channel_create(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.owner = request.user
            channel.save()
            ChannelMembership.objects.create(user=request.user, channel=channel)
            return redirect('rutalk:channel_detail', pk=channel.pk)
    else:
        form = ChannelForm()
    return render(request, 'rutalk/channel_form.html', {'form': form})


@login_required
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
