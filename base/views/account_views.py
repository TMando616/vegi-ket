from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from base.models import Profile
from base.forms import UserCreationForm

# 新規登録画面
class SignUpView(CreateView):
    form_class = UserCreationForm

    # 新規登録作成後のURL
    success_url = '/login/'
    template_name = 'pages/login_signup.html'

    # 親のCreaeViewのOverride
    def form_valid(self, form):
        return super().form_valid(form)