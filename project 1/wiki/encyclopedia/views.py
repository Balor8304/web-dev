from django.shortcuts import render
from markdown2 import markdown
from . import util
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def converter(title):
    c=util.get_entry(title)
    html=markdown(c)
    return html

def page(request,title):
    if util.get_entry(title)==None:
        return render(request,"encyclopedia/error_page.html",{"m":"Page not found"})
    else:
        html=converter(title)
        return render(request,"encyclopedia/page.html",{
            "title":title,"content":html
        })
    
def edit(request):
    if request.method=="POST":
        title=request.POST.get('title')
        markup=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "content":markup,"title":title
        })
    
def save_edit(request):
    if request.method=="POST":
        title=request.POST.get('p')
        content=request.POST.get('q')
        util.save_entry(title,content)
        return render(request,"encyclopedia/page.html",{
            "content":converter(title),"title":title
            })
def newpage(request):
    if request.method=="GET":
        return render(request,"encyclopedia/newpage.html")
    else:
        title=request.POST.get('p')
        content=request.POST.get('q')
        if title in util.list_entries():
            return render(request,"encyclopedia/error_page.html",{"m":"page already exists"})
        else:
            util.save_entry(title,content)
            return render(request,"encyclopedia/page.html",{"content":converter(title),"title":title})

def random_page(request):
    title=choice(util.list_entries())
    html=converter(title)
    return render(request,"encyclopedia/random.html",{"title":title,"content":html})

def search(request):
    if request.method=="POST":
        title=request.POST.get('q')
        if title in util.list_entries():
            html=converter(title)
            return render(request,"encyclopedia/page.html",{"content":html,"title":title})
        else:
            add=[]
            for i in util.list_entries():
                if title.lower() in i.lower():
                    add.append(i)
            return render(request,"encyclopedia/search.html",{"add":add})
    else:
        return render(request,"encyclopedia/search.html",{
            "content":"Error"
        })