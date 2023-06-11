from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin



menu=[
    {"title":"Home", 'url_name':'home'},
    {"title": "About", 'url_name': 'about'},
    {"title": "Post", 'url_name': 'add_article'},
    {"title": "Contacts", 'url_name': 'contacts'},

]
class DataMixin:
    paginate_by = 5
    def get_user_context(self, **kwargs):

        context = kwargs
        cats=Category.objects.all()
        context['cats']=cats
        context['menu'] = menu
        user_menu=menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected']=0

        return context


