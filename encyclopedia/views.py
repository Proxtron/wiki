from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponse
import os
import random

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

def newpage(request):
    return render(request, "encyclopedia/newpage.html", {
        
    })

def createnewpage(request):
    if request.method == "POST":
        entry_title = request.POST['title']
        entry_text = request.POST['q']

        for entry in util.list_entries():
            if entry.lower() == entry_title.lower():
                return HttpResponse("The entry with the title '%s' already exists" % entry_title)


        current_directory = os.getcwd()
        directory_name = os.path.join(current_directory, "entries", "%s.md" % entry_title)

        entry_file = open(directory_name, 'w+')
        entry_file.write(entry_text)
        entry_file.close()
        
        return render(request, "encyclopedia\entry.html", {
            "title" : entry_title,
            "html_content" : entry_text
        })

def editpage(request, title):
    entry_text = util.get_entry(title)
    return render(request, "encyclopedia\editpage.html", {
        "title" : title,
        "entry_text" : entry_text
    })

def editpagecontents(request, title):
    if request.method == "POST":
        entry_text = request.POST["q"]

        markdowner = Markdown()
        html_content = markdowner.convert(entry_text)

        current_directory = os.getcwd()
        directory_name = os.path.join(current_directory, "entries", "%s.md" % title)

        entry_file = open(directory_name, 'w+')
        entry_file.write(entry_text)
        entry_file.close()

        return render(request, "encyclopedia\entry.html", {
            "title" : title,
            "html_content" : html_content
        })

def randompage(request):
    random_entry = random.choice(util.list_entries())
    html_content = convert_md_to_html(random_entry)
    return render(request, "encyclopedia\entry.html", {
        "title" : random_entry,
        "html_content" : html_content
    })