from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from apps.system.mixin import LoginRequiredMixin


# class SystemView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, 'system/system_index.html')


class SystemView(LoginRequiredMixin, TemplateView):
    template_name = 'system/system_index.html'
