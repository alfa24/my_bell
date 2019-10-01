from django.shortcuts import render


# Create your views here.

def index_view(request):
    """Представление главной страницы"""

    return render(request, 'index.html')
