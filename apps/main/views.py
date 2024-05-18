from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def whats_new_view(request):
    return render(request, 'main/whats_new.html')

def error_404_view(request, exception):
    return render(request, 'error_404.html')