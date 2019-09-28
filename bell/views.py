from django.shortcuts import render


# Create your views here.

def IndexView(request):
    """Представление главной страницы"""

    return render(request, 'index.html')
