from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict

class CartListView(ListView):
    model = Item
    template_name = 'pages/cart.html'

class AddCartView(View): #View 

    def post(self, request): # postと定義すると、postのリクエストを受け取ることができる
        pass