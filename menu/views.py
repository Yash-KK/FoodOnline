from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from MultiVendor.helper import (
    get_vendor
)
#MODEL
from .models import (
    Category,
    FoodItem
)

#FORMS
from .forms import (
    CategoryForm,
    FoodItemForm
)

# Create your views here.

@login_required(login_url='login')
def menu_builder(request):
    vendor = get_vendor(request)['get_vendor']
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories
    }
    return render(request, 'menu/menuBuilder.html', context)
 
@login_required(login_url='login')
def items_by_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    fooditems = FoodItem.objects.filter(category=category)
    context = {
        'fooditems': fooditems,
        'category': category
    }

    return render(request, 'menu/itemsByCategory.html', context)

# CATEGORY
@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = get_vendor(request)['get_vendor']
            instance.save()
            messages.success(request, 'new category added')
            return redirect('menu-builder')
        else:
            messages.error(request, 'checkout errors')
            print(form.errors)


    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'menu/category/add.html', context)

@login_required(login_url='login')
def update_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'updated the form')
            return redirect('menu-builder')
        else:
            messages.error(request, 'checkout errors')
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'menu/category/update.html', context)

@login_required(login_url='login')
def delete_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    category.delete()
    messages.success(request, 'category deleted')
    return redirect('menu-builder')


# FOOD ITEM
@login_required(login_url='login')
def add_fooditem(request):   
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = get_vendor(request)['get_vendor']
            instance.save()
            messages.success(request, 'food item added')
            return redirect('items-by-category', category_slug =instance.category.slug)
        else:
            messages.error(request, 'checkout errors')
            print(form.errors)

    else:
        form = FoodItemForm()
    
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request)['get_vendor'])

    context = {
        'form': form
    } 
    return render(request, 'menu/food/add.html', context)


@login_required(login_url='login')
def update_fooditem(request, fooditem_slug):
    fooditem = FoodItem.objects.get(slug=fooditem_slug)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'food item updated!')
            return redirect('items-by-category', category_slug=instance.category.slug)
        else:
            messages.error(request, 'checkout errors')
            print(form.errors)
    else:
        form = FoodItemForm(instance=fooditem)
    form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request)['get_vendor'])

    context = {
        'form': form,
        'fooditem': fooditem
    }
    return render(request, 'menu/food/update.html', context)


@login_required(login_url='login')
def delete_fooditem(request, fooditem_slug):
    fooditem = FoodItem.objects.get(slug=fooditem_slug)
    category_slug = fooditem.category.slug
    fooditem.delete()

    messages.success(request, 'deleted food item')
    return redirect('items-by-category', category_slug=category_slug)
