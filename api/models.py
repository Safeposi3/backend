from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from uuid import uuid4
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    dni = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'phonenumber', 'country', 'address', 'postal_code', 'city', 'dni'] 

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def __str__(self): 
        return self.email
#Ships model:
class Ship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, related_name='ships', on_delete=models.CASCADE)
    length = models.FloatField()
    ship_title = models.FileField(upload_to='ship_titles/',blank=True,null=True)
    ship_registration = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
class Buoys(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )
    PRICES = {
        'S': {
            'price1': 0.38,
            'price2': 0.75,
        },
        'M': {
            'price1': 0.61,
            'price2': 1.21,
        },
        'L': {
            'price1': 1.06,
            'price2': 2.77,
        },
        'XL': {
            'price1': 3.26,
            'price2': 8.52,
        },
    }
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    size = models.CharField(max_length=10, choices=SIZES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price1 = models.FloatField()
    price2 = models.FloatField()
    def get_reservations(self):
        # This will return a QuerySet of all reservations for this buoy
        return self.reservations.all()
    def save(self, *args, **kwargs):
        self.price1 = self.PRICES[self.size]['price1']
        self.price2 = self.PRICES[self.size]['price2']
        super().save(*args, **kwargs)
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buoy = models.ForeignKey(Buoys, related_name='reservations', on_delete=models.CASCADE,null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user} - {self.buoy} - {self.start_time} to {self.end_time}'
        
    def save(self, *args, **kwargs):
            if not self.id:  # Only execute this logic if the reservation is being created (not updated)
                six_hours_later = timezone.now() + timezone.timedelta(hours=6)
                if self.status == 'UNPAID' and timezone.now() >= six_hours_later:
                    self.status = 'CANCELLED'  # Update the status to 'CANCELLED' if it's within 6 hours after creation
            super().save(*args, **kwargs)

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
    )

    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # You can add additional fields as required

    def __str__(self):
        return f'{self.method} - {self.transaction_id}'