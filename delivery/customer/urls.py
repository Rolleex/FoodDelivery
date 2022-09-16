from django.urls import path
from .views import *

urlpatterns = [

    path('', Menu.as_view(), name='home'),
    path('menu/search', MenuSearch.as_view(), name='search'),
    path('category/', CatView.as_view(), name='categorys'),
    path('category/<int:pk>/', CategoryView.as_view(), name='catview'),

]
