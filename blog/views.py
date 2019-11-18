from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import HttpResponse, redirect

from .forms import CommentForm
from django.urls import reverse_lazy, reverse

from .models import Post, Comments
from django.views.generic import (
    ListView, DetailView,
    DeleteView, UpdateView,
    CreateView
)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post  # template = 'post_detail.html', context = {'post': post(slug from url)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, **kwargs):
        post = self.get_object()
        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('comment_body')
                comment = Comments.objects.create(post=post, author=request.user, comment_body=content)
                comment.save()
                messages.success(request, f'Comment is Created')
                post1 = Post.objects.get(pk=post.pk)
                return redirect(post1)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # template = 'post_form.html', form = form}

    def form_valid(self, form):  # for_set_not_NULL_value
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']  # template = 'post_form.html' same view of createView, form = form}

    def form_valid(self, form):  # for_set_not_NULL_value
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class CommentCreateView(CreateView):
#     model = Comments
#     fields = ['comment_body']
#     template_name = 'blog/add_comments.html'
#
#     def form_valid(self, form):  # for_set_not_NULL_value
#         post = self.get_object()
#         form.instance.author = self.request.user
#         form.instance.post = post.pk
#         return super().form_valid(form)


