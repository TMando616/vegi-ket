from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id

# Djangoが標準で装備しているUserモデルをカスタマイズする
# Userオブジェクトの追加フィールドがある場合など
# 実装方法はDjangoのドキュメント参照（https://docs.djangoproject.com/ja/3.2/topics/auth/customizing/#a-full-example）
class UserManager(BaseUserManager):

    # 一般ユーザー作成
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # スーパーユーザーの作成
    def create_superuser(self, username, email, password=None):

        # 上記で定義したcreate_userを実施
        user = self.create_user(
            username,
            email,
            password=password,
        )

        # 追加でis_adminを定義
        user.is_admin = True
        user.save(using=self._db)
        return user


# Userモデルの定義（基本的なUser機能を継承：AbstractBaseUser）
class User(AbstractBaseUser):

    # 連番ではなくランダム値としてcreate_idを使用する（item_models.pyで定義）
    id = models.CharField(default=create_id, primary_key=True, max_length=22)

    username = models.CharField(max_length=50, unique=True, blank=True, default='匿名')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # 必須項目の設定、今回はメールアドレスのみ
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user hace permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
# profileモデル
# Userとの切り分け：Userはコアな内容、Profileは任意の内容
class Profile(models.Model):
    # Userとの1対1の関係
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(default='', blank=True, max_length=50)

    # 注文の際は以下情報が必須になるので、チェック機能が必要
    zipcode = models.CharField(default='', blank=True, max_length=8)
    prefecture = models.CharField(default='', blank=True, max_length=50)
    city = models.CharField(default='', blank=True, max_length=50)
    address1 = models.CharField(default='', blank=True, max_length=50)
    address2 = models.CharField(default='', blank=True, max_length=50)
    tel = models.CharField(default='', blank=True, max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# OneToOneFieldを同時に作成
# @で始まるものが関数名の記述：デコレーター、関数実行前に処理が実行
# post_saveは保存されたタイミング（Userモデルが保存されたタイミング）
@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs): # **kwargsは可変長引数
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])