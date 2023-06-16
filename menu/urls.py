from django.urls import path

from .views import (
    menu_builder,
    items_by_category,

    add_category,
    update_category,
    delete_category,

    add_fooditem,
    update_fooditem,
    delete_fooditem
)
urlpatterns = [
    path('menu-builder/', menu_builder, name='menu-builder'),
    path('items-by-category/<slug:category_slug>/', items_by_category, name='items-by-category'),

    path('add-category/', add_category, name='add-category'),
    path('update-category/<slug:category_slug>/', update_category, name='update-category'),
    path('delete-category/<slug:category_slug>/', delete_category, name='delete-category'),

    path('add-food-item/', add_fooditem, name='add-fooditem'),
    path('update-food-item/<slug:fooditem_slug>/', update_fooditem, name='update-fooditem'),
    path('add-food-item/<slug:fooditem_slug>/', delete_fooditem, name='delete-fooditem')
]
 