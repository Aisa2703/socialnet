from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *


def Homepage(request):
    context = {}

    profiles_list = Profile.objects.all()
    context["profiles"] = profiles_list

    posts_list = Post.objects.all()  # SELECT * FROM Post;
    context["posts"] = posts_list

    categories_list = Category.objects.all()
    context["categories"] = categories_list

    shorts_list = Short.objects.all()
    context["shorts"] = shorts_list

    return render(request, "home.html", context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context["post"] = post_object
    comment_form = CommentForm()
    context["comment_form"] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list
    if request.method == "GET":
        return render(request, "post_info.html", context)
    elif request.method == "POST":
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f"{request.user.username} liked your post with id {post_object.id}"
            )
            return redirect(post_detail, id=id)
        elif 'dislike' in request.POST:
            post_object.likes -= 1
            post_object.save()
            return redirect(post_detail, id=id)

        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()

                Notification.objects.create(
                    user=post_object.creator,
                    text=f"{request.user.username} added comment"
                )
                return HttpResponse("done")


def add_posts(request):
    posts_form = PostsForm()
    context = {'posts_form': posts_form}

    if request.method == "POST":
        posts_form = PostsForm(request.POST, request.FILES)
        if posts_form.is_valid():
            posts_object = posts_form.save(commit=False)
            posts_object.creator = request.user
            posts_object.save()
            return redirect(post_detail, id=posts_object.id)
        else:
            return HttpResponse("Not valid")

    return render(request, 'add_posts.html', context)


def profile_detail(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    context["profile"] = profile_object

    if request.method == "POST":
        Profile.subscribers.add(request.user)
        Profile.save()

    return render(request, "profile_detail.html", context)


def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse("Not valid")

    return render(request, 'add_profile.html', context)


def category_detail(request, id):
    context = {}
    category_object = Category.objects.get(id=id)
    context["category"] = category_object
    return render(request, "category_detail.html", context)


def category_list(request):
    context = {}
    category_info = Category.objects.all()
    context['category'] = category_info
    return render(request, 'category_lst.html', context)


def shorts(request):
    context = {
        'shorts_list': Short.objects.all()
    }
    return render(request, "shorts.html", context)


def short_info(request, id):
    short = Short.objects.get(id=id)
    short.views_qty += 1
    short.viewed_users.add(request.user)
    short.save()
    context = {"short": short}
    return render(request, "short_info.html", context)


# from django.contrib.auth.decorators import login_required
@login_required(login_url='/users/sign-in/')
def create_short(request):
    if request.method == "GET":
        return render(request, "short_form.html")
    elif request.method == "POST":
        new_short_object = Short(
            user=request.user,
            short_file=request.FILES["short_file_file"]
        )
        new_short_object.save()
        return redirect('shorts-info', id=new_short_object.id)


def update_short(request, id):
    short = Short.objects.get(id=id)
    if request.method == "POST":
        new_description = request.POST["description"]
        short.description = new_description
        short.save()
        return redirect(short_info, id=short.id)

    context = {'short': short}
    return render(request, 'update_short.html', context)


def short_file(request, id):
    short_file_object = Short.objects.get(id=id)
    return render(request, 'short_file.html', {'short': short_file_object})


def short_list(request):
    short_lst = Short.objects.all()
    return render(request, 'short_lst.html', {'short_lst': short_lst})


def add_saved(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        post_object = Post.objects.get(id=post_id)
        saved_post, created = SavedPost.objects.get_or_create(
            user=request.user
        )
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_posts/')


def remove_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post = SavedPost.objects.get(user=request.user)
        saved_post.post.remove(post_object)
        saved_post.save()
        return redirect('/saved_posts/')


def post_list(request):
    context = {}
    post_list = Post.objects.all()
    context['posts'] = post_list
    return render(request, 'post_list.html', context)


def saved_posts_list(request):
    posts = Post.objects.filter(saved_post__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_posts.html', context)


def user_posts(request, id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(creator=user)
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, 'user_posts.html', context)


def create_post(request):
    if request.method == "GET":
        return render(request, "create_post_form.html")
    elif request.method == "POST":
        data = request.POST  # dictionary with data from html-form
        # print(data)
        new_post = Post()
        new_post.name = data["post_name"]
        new_post.description = data["description"]
        new_post.photo = request.FILES["photo"]
        new_post.creator = request.user
        new_post.save()
        return HttpResponse("done")


def update_post(request, id):
    context = {}
    post_object = Post.objects.get(id=id)

    if request.user != post_object.creator:
        return HttpResponse("No access")

    if request.method == "POST":
        post_form = PostForm(
            data=request.POST,
            files=request.FILES,
            instance=post_object
        )
        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, "Not valid")
            context["post_form"] = post_form
            return render(request, 'update_post.html', context)

    post_form = PostForm(instance=post_object)
    context["post_form"] = post_form
    return render(request, 'update_post.html', context)


def delete_post(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.creator:
        return HttpResponse("No access")

    post.delete()
    return redirect(Homepage)


def search(request):
    return render(request, 'search.html')


def search_result(request):
    key_word = request.GET["key_word"]
    # posts = Post.objects.filter(name_icontains=key_word)
    posts = Post.objects.filter(
        Q(name_icontains=key_word) |
        Q(description_icontains=key_word)
    )
    context = {"posts": posts}
    return render(request, 'home.html', context)


def contacts(request):
    return HttpResponse("Our contacts!")


def about_us(request):
    return HttpResponse("About Us!")


def add_subscriber(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.add(request.user)
    profile.save()
    messages.success(request, "You have successfully subscribed!")

    new_notification = Notification(
        user=profile.user,
        text=f"User {request.user.username} subscribed to you!"
    )
    new_notification.save()
    return redirect(f'/profile/{profile.id}/')


def remove_follower(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.remove(request.user)
    profile.save()
    messages.warning(request, "You have successfully unsubscribed!")
    return redirect(f'/profile/{profile.id}/')


def register(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/')
    else:
        form = RegistrationUserForm()
    return render(request, 'registration.html', {'form': form})


def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user)
    for notification in notifications_list:
        notification.is_showed = True
    Notification.objects.bulk_update(notifications_list, ['is_showed'])
    context = {"notifications": notifications_list}
    return render(
        request=request,
        template_name='notifications.html',
        context=context,
    )


