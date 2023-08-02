from django.shortcuts import render
from django.views.generic.base import View

from .forms import UploadFile


class UploadView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {"form": UploadFile()})