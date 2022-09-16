from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.core.mail import send_mail
from django.db.models import Q
from django.views.generic import ListView


# Create your views here.
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {

            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)


class CatView(View):
    def get(self, request, *args, **kwargs):
        categorys = Category.objects.all()

        context = {
            'categorys': categorys,
        }
        return render(request, 'customer/category.html', context)


class CategoryView(ListView):
    template_name = 'customer/cat-view.html'
    context_object_name = 'post'

    def get_queryset(self):
        return MenuItem.objects.filter(category__pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Category.objects.get(pk=self.kwargs['pk'])
        return context
