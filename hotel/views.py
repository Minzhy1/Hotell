from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Service, Guest, Room, Bron, ProvisionService
from django.db.models import Q
import datetime


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

# Список клиентов
def clients(request):
    cliens = Guest.objects.all().select_related('document')
    return render(request, 'clients.html', {
        'cliens': cliens
    })

# Выход
def user_logout(request):
    logout(request)
    return redirect('service')

def nomerfond(request):
    rooms = Room.objects.all().select_related('category')
    filt = request.GET.get('search', '')
    catfilt = request.GET.get('cate', '')
    if catfilt:
        rooms = rooms.filter(category=int(catfilt))
    if filt:
        rooms = rooms.filter(count_room=int(filt))
    return render(request, 'nomer.html',{
            'rooms': rooms,
            'filt': filt
            })


def book_service(request):
    guests = Guest.objects.all()
    services = Service.objects.all()

    if request.method == 'POST':
        try:
            guest_id = request.POST.get('guest')
            service_id = request.POST.get('service')
            booking_date = request.POST.get('booking_date')

            # Проверяем заполнение даты
            if not booking_date:
                messages.error(request, "Пожалуйста, выберите дату")
                return redirect('book_service')

            guest = Guest.objects.get(id=guest_id)
            service = Service.objects.get(id=service_id)

            # Ищем первую бронь (или создаем фиктивную)
            bron = Bron.objects.first()

            # Создаем запись на услугу
            booking = ProvisionService.objects.create(
                bron=bron,
                service=service,
                decimal=service.price,
                date=booking_date
            )

            messages.success(request, f'✅ Услуга "{service.title}" записана для {guest.fio} на {booking_date}')
            return redirect('book_service')

        except Exception as e:
            messages.error(request, f'❌ Ошибка: {str(e)}')

    return render(request, 'zapis.html', {
        'guests': guests,
        'services': services,
        'today': datetime.date.today()
    })










