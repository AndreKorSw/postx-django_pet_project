from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
# Create your views here.
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm


# def index(request):
#     cats=Category.objects.all()
#     posts=Xforum.objects.all()
#     context={
#         "posts":posts,
#         "title":'Home',
#         "menu":menu,
#         "cats": cats,
#         "cat_selected":0,
#     }
#     return render(request, "xforum/index.html", context=context)


menu=[
      {"title":"Home", 'url_name':'home'},
      {"title": "About", 'url_name': 'about'},
      {"title": "Post", 'url_name': 'add_article'},
      {"title": "Contacts", 'url_name': 'contacts'},
      # {"title":"Search", 'url_name': 'search-venues'},



]
def documents(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, "xforum/documents.html", context=context)

def faq(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, "xforum/FAQ.html", context=context)

def for_users(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, "xforum/for_users.html", context=context)

def for_authors(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, "xforum/for_authors.html", context=context)

def search_venues(request):
    cats=Category.objects.all()
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)
    if request.method == 'POST':
        searched=request.POST['searched']
        venues=Xforum.objects.filter(title__contains=searched)
    return render(request, 'xforum/search_venues.html', {'searched':searched, 'venues':venues,"menu":user_menu, "cats":cats,})


def likeview(request, slug):
    post=get_object_or_404(Xforum, id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('post', args=[str(slug)]))



class XforumHome(DataMixin,ListView):
    model = Xforum
    template_name = "xforum/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add your article")
        return dict(list(context.items()) + list(c_def.items()))


    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        # print(ordering)
        return ordering

    # def get_queryset(self):
    #     return Xforum.objects.filter(is_published=True)

def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context={
        "menu":user_menu,
    }
    return render(request, "xforum/about.html", context=context)

# def show_post(request, slug):
#     context = {
#         "slug": slug,
#     }
#     return render(request, "xforum/post.html", context=context)

class ShowPost(DataMixin, DetailView):
    model = Xforum
    template_name = 'xforum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    success_url=reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        liked=False
        staff=get_object_or_404(Xforum, slug=self.kwargs['post_slug'])
        if staff.likes.filter(id=self.request.user.id).exists():
            liked=True

        total_likes=staff.total_likes()
        context['total_likes']=total_likes
        context['liked']=liked
        c_def=self.get_user_context(title='smb Post')
        return dict(list(context.items()) + list(c_def.items()))

def contacts(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, 'xforum/contacts.html', context=context)
def news(request):
    context = {
        "menu": menu
    }
    return HttpResponse("news")

# def add_article(request):
#     if request.method == "POST":
#         form=AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 print(form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None,'Error while creating')
#     else:
#         form=AddPostForm()
#     context = {
#         "menu": menu,
#         'form':form,
#     }
#     return render(request, 'xforum/add_article.html', context=context)

class AddArticle(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'xforum/add_article.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Add your article")
        return dict(list(context.items()) + list(c_def.items()))


class UpdateArticle(UpdateView, DataMixin):
    model = Xforum
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('home')
    template_name = "xforum/update_article.html"
    fields = ["title", 'slug', 'time_to_read', 'photo', 'content', "cat"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Edit your article")
        return dict(list(context.items()) + list(c_def.items()))

class DeleteArticle(DeleteView, DataMixin):
    model=Xforum
    template_name = "xforum/delete_article.html"
    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Delete your article")
        return dict(list(context.items()) + list(c_def.items()))


class XforumCategories(DataMixin,ListView):
    model=Xforum
    template_name = "xforum/index.html"
    context_object_name = "posts"
    allow_empty = False # 404 если страница не найдена при выводе несуществуещих данных бд


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Category - " +str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))
    def get_queryset(self):
        return Xforum.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True)

#


# def show_category(request, cat_slug):
#
#     posts = Xforum.objects.filter(cat__slug=cat_slug)
#     context = {
#         "posts": posts,
#         "title": 'Home',
#         "menu": menu,
#         "cat_selected":cat_slug,
#     }
#
#     if len(posts)==0:
#         raise Http404
#     return render(request, "xforum/index.html", context=context)
class UserRegistration(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = "xforum/registration.html"
    success_url = reverse_lazy('create_profile')



    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('create_profile')



class LoginUser(DataMixin, LoginView):
    form_class = UserAuthenticationForm
    template_name = "xforum/login.html"
    # success_url = reverse_lazy('home')
    # login_url = redirect('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Log in")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)

    return redirect('login')


class UserEditView(UpdateView, DataMixin):
    model=Profile
    form_class=EditUserProfileForm
    template_name = 'xforum/edit_profile.html'
    success_url = reverse_lazy('home')



    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Edit userprof")
        return dict(list(context.items()) + list(c_def.items()))


    def get_object(self, queryset=None):
        return self.request.user

class PasswordsChangeView(PasswordChangeView,DataMixin):
    form_class = PasswordChangingForm
    template_name = 'xforum/change_password.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Changee password")
        return dict(list(context.items()) + list(c_def.items()))



class ShowUserProfile(DeleteView, DataMixin):
    model = Profile
    template_name = "xforum/show_profile.html"



    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        page_user=get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user']=page_user
        c_def=self.get_user_context(title="Profile")
        return dict(list(context.items()) + list(c_def.items()))



class CreateUserProfile(CreateView, DataMixin):
    model = Profile
    form_class = UserProfileCreationForm
    template_name = 'xforum/create_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Create profile")
        return dict(list(context.items()) + list(c_def.items()))

def show_anonuser_profile(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        "menu": user_menu,
    }
    return render(request, 'xforum/anonuser_profile.html', context=context )

class AddCommentView(CreateView, DataMixin):
    model = Comments
    template_name = "xforum/add_comment.html"
    form_class = AddCommentForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.article_id=self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Add comment")
        return dict(list(context.items()) + list(c_def.items()))



class DeleteCommentView(DeleteView,DataMixin):
    model = Comments
    template_name = "xforum/delete_comment.html"
    template_name_suffix = "_check_delete"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Delete comment")
        return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('страница не найдена')


