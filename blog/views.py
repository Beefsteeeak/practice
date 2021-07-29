from blog.forms import RegisterForm

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView

from .forms import CommentForm, ContactForm, PostForm
from .models import Post
from .tasks import send_email as celery_send_email


class RegisterFormView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy('profile')
    success_message = "Profile was updated successfully"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['posts_count'] = self.get_object().post_set.count()
        return context


class UserPublicProfile(DetailView):
    model = User
    template_name = 'blog/public_profile.html'


@login_required
def post_creation(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            celery_send_email.delay(
                'Action',
                'New post was added',
                'noreply@example.com',
                ['admin@mail.com']
            )
            # send_mail(
            #     'Action',
            #     'New post was added',
            #     'noreply@example.com',
            #     ['admin@mail.com']
            # )
            messages.add_message(request, messages.SUCCESS, 'Post was successfully created')
            return redirect('blog:post-list')
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_create_form.html',
        context={
            "form": form,
        }
    )


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(blank=False)


def post_detail(request, pk):
    post_instance = Post.objects.prefetch_related('comment_set').get(pk=pk)

    comment_list = post_instance.comment_set.all()
    paginator = Paginator(comment_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = Post.objects.get(pk=pk)
            if request.user.is_authenticated:
                form.username = request.user.username
            form.save()
            celery_send_email.delay(
                'Action',
                'New comment was added',
                'noreply@example.com',
                'admin@mail.com'
            )
            # send_mail(
            #     'Action',
            #     'New comment was added',
            #     'noreply@example.com',
            #     'admin@mail.com'
            # )
            link = reverse('blog:post-detail', kwargs={"pk": pk})
            celery_send_email.delay(
                'Action',
                f'New comment was added {link}',
                'noreply@example.com',
                post_instance.user.email
            )
            # send_mail(
            #     'Action',
            #     f'New comment was added {link}',
            #     'noreply@example.com',
            #     post_instance.user.email
            # )
            return redirect('blog:post-list')
    else:
        form = CommentForm()

    return render(
        request,
        'blog/post_detail.html',
        context={
            "form": form,
            "post_instance": post_instance,
            'page_obj': page_obj,
        }
    )


@login_required
def post_user_list(request):
    post_list = Post.objects.filter(user=request.user)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/post_user_list.html',
        context={
            'post_list': post_list,
            'page_obj': page_obj,
        }
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            celery_send_email.delay(
                subject,
                text,
                email,
                'admin@mail.com'
            )
            # send_email(
            #     subject,
            #     text,
            #     email,
            #     'admin@mail.com'
            # )
            messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('blog:post-list')
    else:
        form = ContactForm()
    return render(
        request,
        'blog/contact.html',
        context={
            'form': form,
        }
    )
