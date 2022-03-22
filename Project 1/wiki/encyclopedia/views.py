from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from . import util
from markdown2 import Markdown


class NewTaskForm(forms.Form):
    search = forms.CharField(label="")


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": NewTaskForm()},
    )


def create(request):
    return render(request, "encyclopedia/create.html", {"form": NewTaskForm()})


def wiki(request, title):
    return render(
        request,
        "encyclopedia/wiki.html",
        {"stuff": Markdown().convert(util.get_entry(title)), "form": NewTaskForm()},
    )


def search(request, search):
    return render(
        request,
        "encyclopedia/wiki.html",
        {"stuff": Markdown().convert(util.get_entry(search)), "form": NewTaskForm()},
    )
