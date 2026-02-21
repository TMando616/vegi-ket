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
    
class PayCancelView(TemplateView):
    template_name = 'pages/cancel.html'

    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得

        # 在庫数と販売数をもとの状態に戻す

        # is_confirmedがFalseであれば削除（仮オーダー削除）

        return super().get(request, *args, **kwargs)

class PayWithStripe(View):# Viewの中でmethodレベルで実装可能（postなど）

    def post(self, request, *args, **kwargs): #今回はpostのみ、getなどではアクセスできない
        cart = request.session.get('cart', None)

        if cart is None or len(cart) == 0:
            # cartがない場合はルートへリダイレクト
            return redirect('/')
        
        line_items = []

        # cartがある前提
        for item_pk, quantity in cart['items'].items():
            item = Item.object.get(pk=item_pk) # pkでItemオブジェクトを取得

            # stripeの決済ページを作るメソッド
            line_item = create_line_item(
                item.price,
                item.name,
                quantity
            )
            line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            # customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items, # 画面に表示するものをここで渡す
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success', #成功時URL
            cancel_url=f'{settings.MY_URL}/pay/cancel', #キャンセル時URL
        )

        return redirect(checkout_session.url)