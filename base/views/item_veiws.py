from django.shortcuts import render
from django.views.generic import ListView
from base.models import Item


class IndexListView(ListView):
    # 基本の項目
    model = Item # Itemの一覧を取得
    template_name = 'pages/index.html' # どのテンプレートを使用するか