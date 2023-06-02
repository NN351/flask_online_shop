from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from src.apps.product.serializers import * 
from src.apps.product.models import *




class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []  # Add your desired permission classes for read-only actions
        else:
            permission_classes = [IsAuthenticated]  # Add your desired permission classes for other actions (e.g., create, update, delete)

        return [permission() for permission in permission_classes]
    




from django.views.generic import TemplateView, ListView, DetailView


class IndexView(TemplateView):
    template_name = "index.html"


class ProductListView(ListView):
    template_name="product_list.html"
    model = Product
    queryset = Product.objects.filter(is_active=True)
    context_object_name = "products"


    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get("subcategory_slug")

        if subcategory_slug:
            products = Product.objects.filter(category__slug=subcategory_slug, is_active=True)
        elif category_slug:
            products = Product.objects.filter(category__parent__slug=category_slug, is_active=True)
        else:
            products = Product.objects.filter(is_active=True)
        return products



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    queryset = Product.objects.filter(is_active=True)
    context_object_name = "product"