from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import CommentForm, RegistrationUserForm


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
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.post = post_object
            new_comment.save()
            return HttpResponse("done")


def profile_detail(request, id):
    context = {}
    profile_object = Profile.objects.get(id=id)
    context["profile"] = profile_object
    user_posts = Post.objects.filter(creator=profile_object.user)
    context['user_posts'] = user_posts
    return render(request, "profile_detail.html", context)


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
    context = {"short": Short.objects.get(id=id)}
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


def user_posts(request, user_id):
    user = User.objects.get(id=user_id)
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


