from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Service, Guest
from django.db.models import Q


# Главная страница
def home(request):
    services = Service.objects.all()
    search_service = request.GET.get('search', '')
    if search_service:
        services = services.filter(
            Q(title__icontains=search_service)
        )
    return render(request, 'service.html', {
        'services':services,
        'search_service': search_service
    })


# Регистрация
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Создаем пользователя
        User.objects.create_user(username=username, password=password)

        # Входим сразу после регистрации
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('service')

    return render(request, 'register.html')


# Вход
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user.groups.filter(name='manager').exists():
            return redirect('service')

        if user is not None:
            login(request, user)
            return redirect('service')

    return render(request, 'avtoriz.html')

# Список клиентов для менеджера
def clients(request):
    cliens = Guest.objects.all().select_related('document')
    return render(request, 'clients.html', {
        'cliens': cliens
    })

# Выход
def user_logout(request):
    logout(request)
    return redirect('service')