from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from base.models import Item
import stripe

stripe.api_key = settings.STRIPE_API_SECRET_KEY

class PaySuccessView(TemplateView):
    template_name = 'pages/success.html'

    # 決済が完了するためカート情報を削除する
    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得し、注文確定に変更

        # カート情報削除
        del request.session('cart')

        return super().get(request, *args, **kwargs)