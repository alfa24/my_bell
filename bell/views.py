from django.shortcuts import render, redirect


# Create your views here.

def index_view(request):
    """Представление главной страницы"""

    return render(request, 'index.html')


def new_bell(request):
    """создание колокольчика"""

    return redirect('bell_view', 1)


def bell_view(request, code):
    """представление колокольчика"""

    return render(request, 'bell.html')
