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

            'menu_items': menu_items,
        }
        return render(request, 'customer/menu.html', context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))

            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
            price = 0
            item_ids = []
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
        )
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order_info', pk=order.pk)


class OrderInfo(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
            'order': order,

        }
        return render(request, 'customer/order_info.html', context)



""" for next ver."""
# class MenuSearch(View):
#     def get(self, request, *args, **kwargs):
#         query = self.request.GET.get('q')
#
#         menu_items = MenuItem.objects.filter(
#             Q(name__icontains=query) |
#             Q(price__icontains=query) |
#             Q(description__icontains=query)
#         )
#         context = {
#             'menu_items': menu_items
#         }
#         return render(request, 'customer/menu.html', context)
#
#
# class CatView(View):
#     def get(self, request, *args, **kwargs):
#         categorys = Category.objects.all()
#
#         context = {
#             'categorys': categorys,
#         }
#         return render(request, 'customer/category.html', context)
#
#
# class CategoryView(ListView):
#     template_name = 'customer/cat-view.html'
#     context_object_name = 'post'
#
#     def get_queryset(self):
#         return MenuItem.objects.filter(category__pk=self.kwargs['pk'])
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['name'] = Category.objects.get(pk=self.kwargs['pk'])
#         return context
