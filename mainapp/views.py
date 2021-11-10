from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket

def main(request):
    title = 'главная'
    
    products = Product.objects.all()[:4]
        
    context = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', context)    

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def products(request, pk=None, page=1):   
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)
    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }

            products = Product.objects.filter(is_active=True,\
                   category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, \
                   is_active=True, category__is_active=True).order_by('price')
        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)   

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', context)

    same_products = Product.objects.all()[3:5]
    
    context = {
        'title': title, 
        'links_menu': links_menu, 
        'same_products': same_products
    }
    
    return render(request, 'mainapp/products.html', context)

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
            
    if pk:
        if pk == '0':
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        
        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'basket': basket,
        }
        
        return render(request, 'mainapp/products_list.html', context)


def contacts(request):
    return render(request, 'mainapp/contacts.html')

def product(request, pk):
    title = 'продукты'
    
    context = {
        'title': title, 
        'links_menu': ProductCategory.objects.all(), 
        'product': get_object_or_404(Product, pk=pk), 
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', context)
