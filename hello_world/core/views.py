from django.shortcuts import render

def index(request):
    data = "Hy Python"
    context = {
        'form': data
    }
    return render(request, "index.html", context )
