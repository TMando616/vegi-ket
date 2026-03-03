from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン必須を指定できる
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
    
# ログイン処理
# LoginViewというクラス名だと継承元と被る
class Login(LoginView):
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email') # この書き方はタプル
    success_url = '/account/' # 更新後も同じページ

    # 親のget_objectをoverride
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得（登録されていることが前提）
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture', 'city', 'address', 'address2', 'tel')
    success_url = '/profile/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得（登録されていることが前提）
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()