from random import choice
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from markdown2 import Markdown
import random


class SearchForm(forms.Form):
    search = forms.CharField(label="")


def index(request):
    if request.method == "POST":
        print("procurou")
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            entries_all = util.list_entries()
            entries_found = []
            if util.get_entry(query) is not None:
                return render(
                    request,
                    "encyclopedia/wiki.html",
                    {
                        "title": query,
                        "stuff": Markdown().convert(util.get_entry(query)),
                        "form": SearchForm(),
                    },
                )
            else:
                for entry in entries_all:
                    if query.lower() in entry.lower():
                        entries_found.append(entry)
                print(entries_found)
                return render(
                    request,
                    "encyclopedia/notfound.html",
                    {
                        "title": query,
                        "form": SearchForm(),
                        "entries": entries_found
                    },
                )

    return render(
        request,
        "encyclopedia/index.html",
        {"title": "Home", "entries": util.list_entries(), "form": SearchForm()},
    )


def create(request):
    return render(request, "encyclopedia/create.html", {"form": SearchForm()})


def wiki(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/notfound.html", {"form": SearchForm()})
    else:
        return render(
            request,
            "encyclopedia/wiki.html",
            {"title": title, "stuff": Markdown().convert(util.get_entry(title)), "form": SearchForm()},
        )


def search(request, search):
    if util.get_entry(search) is not None:
        return render(
            request,
            "encyclopedia/wiki.html",
            {
                "title": search,
                "stuff": Markdown().convert(util.get_entry(search)),
                "form": SearchForm(),
            },
        )

def random(request):
    list = util.list_entries()
    select = choice(list)
    if util.get_entry(select) is None:
        return render(request, "encyclopedia/notfound.html", {"form": SearchForm()})
    else:
        return HttpResponseRedirect(f"/wiki/{select}")