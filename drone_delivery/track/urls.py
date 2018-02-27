from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_items, name='view_items'),
    path('<int:item_id>/', views.item_details, name='item_details'),
    path('deliver/<int:item_id>/', views.deliver, name='deliver'),
]
