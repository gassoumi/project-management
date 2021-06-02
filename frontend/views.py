from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def index(request):
    # return render(request, 'frontend/index.html')
    return redirect('https://obscure-reef-91996.herokuapp.com/')
