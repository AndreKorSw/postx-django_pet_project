from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class AddPostForm(forms.ModelForm):
    # title=forms.CharField(max_length=255)
    # slug=forms.SlugField(max_length=255)
    # user_name=forms.ModelChoiceField(queryset=)
    # content=forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}))
    # is_published = forms.BooleanField()
    # cat=forms.ModelChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model=Xforum
        fields=['title', 'slug','user_name', 'time_to_read', 'photo','content', "cat"]

        widgets={
            'user_name':forms.TextInput(attrs={'class':'form-control', 'value':"", "id":"notshow", "type":'hidden'}),
        }

class UserRegistrationForm(UserCreationForm):

    username=forms.CharField(label="Login", widget=forms.TextInput(attrs={'class':'form-input'}))
    email=forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields=("username", "email", "password1", "password2",)


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-input'}))


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={"class":'form-input'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2",)


class UserProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'web_site_url', 'twitter_url', 'instagram_url', 'vk_url', 'linkdn_url',)
        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            # 'profile_pic':forms.ImageField(attrs={'class':'form-control'}),
            'web_site_url':forms.TextInput(attrs={'class':'form-control'}),
            'twitter_url':forms.TextInput(attrs={'class':'form-control'}),
            'instagram_url':forms.TextInput(attrs={'class':'form-control'}),
            'vk_url':forms.TextInput(attrs={'class':'form-control'}),
            'linkdn_url':forms.TextInput(attrs={'class':'form-control'}),

        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields = ('body', 'comment_author',)

        widgets={'comment_author':forms.TextInput(attrs={'class':'form-control', 'value':"", "id":"notshow", "type":'hidden'}),}



class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model=Profile

        fields = ['bio', 'profile_pic', 'web_site_url', 'twitter_url', 'instagram_url', 'vk_url', 'linkdn_url']
        # fields  = ['username', 'first_name', 'last_name', 'email']
