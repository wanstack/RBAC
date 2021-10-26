import json

from django.views.generic.base import View
from django.views.generic import ListView, UpdateView
from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.system.mixin import LoginRequiredMixin
from apps.system.models import Menu
from apps.system.forms import MenuForm
from django.views.generic import CreateView
from django.http import Http404
from apps.system.mixin import LoginRequiredMixin
from apps.system.models import Menu

# class MenuCreateView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         ret = dict(menu_all=Menu.objects.all())
#         return render(request, 'system/rbac/menu_create.html', ret)
#
#     def post(self, request):
#         res = dict(result=False)
#         menu = Menu()
#         menu_form = MenuForm(request.POST, instance=menu)
#         if menu_form.is_valid():
#             menu_form.save()
#             res['result'] = True
#         return HttpResponse(json.dumps(res), content_type='application/json')

from django.views.generic import ListView

from .mixin import LoginRequiredMixin
from apps.common.views_custom import CPOSCreateView, CPOSUpdateView
from .models import Menu


class MenuCreateView(CPOSCreateView):
    model = Menu
    fields = '__all__'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)


from apps.common.views_custom import BreadcrumbMixin


class MenuListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(CPOSUpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        kwargs['menu_all'] = Menu.objects.all()
        return super().get_context_data(**kwargs)
