from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from mainapp.models import Product, ProductCategory
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DetailView


class UsersListView(ListView):
    model = ShopUser
    context_object_name = 'objects'
    template_name = 'adminapp/users.html'


class UserCreate(CreateView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    fields = ['avatar', 'age']
   

def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES,\
                                                        instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',\
                                                args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)
    
    context = {'title': title, 'update_form': edit_form}
    
    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    title = 'пользователи/удаление'
    
    user = get_object_or_404(ShopUser, pk=pk)
    
    if request.method == 'POST':
        #user.delete()
        #вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    context = {'title': title, 'user_to_delete': user}
    
    return render(request, 'adminapp/user_delete.html', context)



def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


def category_create(request):
    pass


def category_update(request, pk):
    pass


def category_delete(request, pk):
    pass


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})
    
    context = {'title': title, 
               'update_form': product_form, 
               'category': category
    }
    
    return render(request, 'adminapp/product_update.html', context)
      




def product_read(request, pk):
    title = 'продукт/подробнее'    
    product = get_object_or_404(Product, pk=pk)
    context = {'title': title, 'object': product,}
    
    return render(request, 'adminapp/product_read.html', context)





def product_update(request, pk):
    title = 'продукт/редактирование'
       
    edit_product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,\
                                                  instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update',\
                                                 args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    
    context = {'title': title, 
               'update_form': edit_form, 
               'category': edit_product.category 
    }
    
    return render(request, 'adminapp/product_update.html', context)
    
    



def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products',\
                                             args=[product.category.pk]))

    context = {'title': title, 'product_to_delete': product}
    
    return render(request, 'adminapp/product_delete.html', context)

