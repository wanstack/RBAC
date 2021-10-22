import json

from django.views.generic.base import View
from django.views.generic import ListView, UpdateView
from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.common.views_custom import SimpleInfoCreateView
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

class MenuCreateView(SimpleInfoCreateView):
    model = Menu
    fields = '__all__'
    extra_context = dict(menu_all=Menu.objects.all())


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'menu_all'


class MenuUpdateView(LoginRequiredMixin, UpdateView):
    model = Menu
    fields = '__all__'
    template_name_suffix = '_update'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()
        if 'id' in self.request.GET and self.request.GET['id']:
            queryset = queryset.filter(id=int(self.request.GET['id']))
        elif 'id' in self.request.POST and self.request.POST['id']:
            queryset = queryset.filter(id=int(self.request.POST['id']))
        else:
            raise AttributeError("Generic detail view %s must be called with id. "
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


