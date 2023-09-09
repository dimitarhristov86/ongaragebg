from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Categorie


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Categorie
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def CategoryListView(request, cats):
    category_posts = Post.objects.filter(categories=int(cats)).order_by('-date_posted')
    return render(request, 'blog/categories_list.html', {'cats': cats, 'category_posts': category_posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        categories_menu = Categorie.objects.all()
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['categories_menu'] = categories_menu
        return context


class PostDetailView(DetailView):
    model = Post
    fields = ['title', 'content', 'categories', 'image']

    def get_context_data(self, *args, **kwargs):
        categories_menu = Categorie.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['categories_menu'] = categories_menu
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


