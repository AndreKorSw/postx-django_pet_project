from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("", XforumHome.as_view(), name="home"),
    path("about/", about, name="about"),
    path("post/<slug:post_slug>", ShowPost.as_view(), name="post"),
    path("contacts/", contacts, name="contacts"),
    path("add_article/", AddArticle.as_view(), name="add_article"),
    path("category/<slug:cat_slug>", XforumCategories.as_view(), name="category"),
    path("registration/", UserRegistration.as_view(), name='register'),
    path("login/", LoginUser.as_view(), name='login'),
    path("logout/", logout_user, name='logout'),
    path('update_article/edit/<slug:slug>', UpdateArticle.as_view(), name='update_article'),
    path('search_venues/', search_venues, name='search-venues'),
    path('delete_article/<slug:slug>/remove', DeleteArticle.as_view(), name='delete_article'),
    path('like/<slug:slug>', likeview, name='like_post'),
    path('edit_profile/<int:pk>/', UserEditView.as_view(), name='edit_profile'),
    path('<int:pk>/password/', PasswordsChangeView.as_view(), name="change_password"),
    path("<int:pk>/show_profile/", ShowUserProfile.as_view(), name="show_profile"),
    path('create_profile/', CreateUserProfile.as_view(), name='create_profile'),
    path('anon_user_profile/', show_anonuser_profile, name='anon_user_profile'),
    path('add_comment/<int:pk>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:pk>/del_comment/',DeleteCommentView.as_view(), name='delete_comment'),
    path('for_users/', for_users, name='for_users'),
    path('for_authors/', for_authors, name='for_authors'),
    path('FAQ/', faq, name='faq'),
    path('documents/', documents, name='documents'),

]

