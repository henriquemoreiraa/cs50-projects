import random
from django import forms
from django.http import HttpResponseRedirect
import markdown2

from django.shortcuts import render

from encyclopedia.validators import validate_title

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search_results(request):
    q = request.GET.get('q')
    content = util.get_entry(q)

    if content:
        return HttpResponseRedirect(f'/wiki/{q}')

    entries = util.list_entries()
    similiar_results = [entry for entry in entries if q in entry]

    return render(request, "encyclopedia/search-results.html", {
        "entries": similiar_results,
        "title": q
    })


def wiki(request, title):
    content = util.get_entry(title)

    if not content:
        return render(request, "encyclopedia/not-found.html")

    return render(request, "encyclopedia/wiki.html", {
        "content": markdown2.markdown(content),
        "title": title.capitalize()
    })


def create_new_page(request):
    if request.method == 'POST': 
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = request.POST['title']
            content = request.POST['content']

            util.save_entry(title, content)

            return HttpResponseRedirect(f'/wiki/{title}')
        
        return render(request, "encyclopedia/create-new-page.html", {
                "form": form,
        })

    return render(request, "encyclopedia/create-new-page.html", {
        "form": NewPageForm()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    form = EditPageForm({'content': content})

    if request.method == 'POST': 
        form = EditPageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            util.save_entry(title, content)

            return HttpResponseRedirect(f'/wiki/{title}')
        
        return render(request, "encyclopedia/edit-page.html", {
            "form": form,
        })

    return render(request, "encyclopedia/edit-page.html", {
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = entries[random.randint(0, len(entries) - 1)]
    
    return HttpResponseRedirect(f"/wiki/{random_entry}")


class NewPageForm(forms.Form):
    title = forms.CharField(label='Page title', required=True, validators=[validate_title])
    content = forms.CharField(label=' ', required=True, widget=forms.Textarea(attrs={"rows": "5", "placeholder": 'Page content in markdown.'}))

class EditPageForm(forms.Form):
    content = forms.CharField(label=' ', required=True, widget=forms.Textarea(attrs={"rows": "5", "placeholder": 'Page content in markdown.'}))

