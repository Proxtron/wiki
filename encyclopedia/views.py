from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponse

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "html_content":html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST["q"]
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title" : entry_search,
                "html_content":html_content
            })
        else:
            possible_entries = []
            for entry in util.list_entries():
                if entry_search.lower() in entry.lower():
                    possible_entries.append(entry)

            if len(possible_entries) == 0:
                return render(request, "encyclopedia/error.html")
            else:
                return render(request, "encyclopedia/search.html", {
                    "possible_entries" : possible_entries,
                    "entry" : entry_search
                })