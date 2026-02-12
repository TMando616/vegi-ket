from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict

class CartListView(ListView):
    model = Item #すべてのアイテムを返している→セッション情報などに即したアイテムにしたい
    template_name = 'pages/cart.html'


    # query_set：アイテムのそれぞれのオブジェクトのセットのこと
    # 今回の修正で選択されたカートのみ返すようにしている
    def get_queryset(self): # ListViewが持つメソッド名、同名でoverrideする
        cart = self.request.session.get('cart', None)

        if cart is None or len(cart) == 0: # cartがないか0この場合はリダイレクト
            return redirect('/')
        
        # 初期化処理
        self.qyeryset = []
        self.total = 0

        # cartの中にはitemsがある前提（OrderedDict形式）
        for item_pk, quantity in cart['items'].items(): # key:item_pk, value:quantity としてループ処理
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal

        self.tax_included_total = int(obj.total * (settings.TAX_RATE + 1))
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart

        return super().get_queryset()
    
    def get_contect_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = self.total
            context["tax\included_total"] = self.tax_included_total
        except Exception:
            pass
        return context


class AddCartView(View): #View method毎に処理を分けられる

    def post(self, request): # postと定義すると、postのリクエストを受け取ることができる
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', None)

        if cart is None or len(cart) == 0:
            items = OrderedDict() # インスタンスの作成(collection)、Orderedにしている理由は順序が必要であるため
            cart = {'items': items}

        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity

        request.session['cart'] = cart
        return redirect('/cart/')