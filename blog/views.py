from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post

    # specify the listing template by default <app_name>/<model>_<viewtype>.html
    template_name = "blog/home.html"

    context_object_name = 'posts'  # context to pass to template
    ordering = ['-date_posted']  # order posts in descending

    # def get_queryset(self):
    #     print(self.request.user)
    #     queryset = super().get_queryset().filter(author=self.request.user)
    #     return queryset


class PostDetailView(DetailView):
    model = Post


# login required mixin is used to get the effect of login_required() decorator in class based componenets
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user  # adding author after form submit
        return super().form_valid(form)


# user passes test mixin automatically checks whether user is allowed to edit the entry
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

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

    success_url = '/'  # success url to redirect to after deletion

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True

        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
