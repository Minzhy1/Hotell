from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=10)

class Document(models.Model):
    series = models.CharField(max_length=20, verbose_name='Серия')
    numbers = models.CharField(max_length=20)
    date = models.DateField()
    issued =models.CharField(max_length=250)

    def __str__(self):
        return f'{self.series} {self.numbers}'

class Guest(models.Model):
    fio = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.fio

# Категория номера (люкс, обычный и тд)
class Category(models.Model):
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.category

# Предметы мебели
class Subject(models.Model):
    subject = models.CharField(max_length=20)
    def __str__(self):
        return self.subject

# Оснащение номера
class Osn(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.category} {self.subject}'

class Room(models.Model):
    floor = models.IntegerField()
    count_room = models.IntegerField()
    count_sleep = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.floor

# Бронирование
class Bron(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_in = models.DateField()
    date_out= models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fact = models.CharField(max_length=20)
    def __str__(self):
        return self.guest

# Услуга
class Service(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    def __str__(self):
        return self.title

# Оказание услуг
class ProvisionService(models.Model):
    bron = models.ForeignKey(Bron, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    decimal = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return self.bron





