import json

from django.views.generic import CreateView, UpdateView
from django.shortcuts import HttpResponse

from apps.system.mixin import LoginRequiredMixin
from django.http import Http404
from apps.system.models import Menu


class CPOSGetObjectMixin:
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


class CPOSEditViewMixin:

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


class CPOSCreateView(LoginRequiredMixin, CPOSEditViewMixin, CreateView):
    """"
    View for create an object, with a response rendered by a template.
    Returns information with Json when the data is created successfully or fails.
    """


class CPOSUpdateView(LoginRequiredMixin, CPOSEditViewMixin, CPOSGetObjectMixin, UpdateView):

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class BreadcrumbMixin:

    def get_context_data(self, **kwargs):
        menu = Menu.get_menu_by_request_url(url=self.request.path_info)
        if menu is not None:
            kwargs.update(menu)
        return super().get_context_data(**kwargs)
