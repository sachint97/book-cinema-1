from django.db import models
from utils.slug_generator import unique_slug_generator
from apps.user.models import Profile


# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=True, max_length=255, editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Movie(models.Model):
    rating_choice = (
        ('U', 'U'),
        ('UA', 'UA'),
        ('A', 'A'),
        ('R', 'R'),
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    language = models.CharField(max_length=255, null=True, blank=True)
    certificate = models.CharField(max_length=2, choices=rating_choice)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.title)
        self.clean()
        super().save(*args, **kwargs)


class Media(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='media')
    image = models.ImageField(null=True, blank=True)
    alt_text = models.CharField(max_length=255)
    is_feature = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie}-{self.image}"


class Theater(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    city = models.ForeignKey(City, related_name="theater", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Screen(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='screen')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Seat(models.Model):
    seat_number = models.IntegerField(null=False, blank=False, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'seat number {self.seat_number}'


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='show')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='show')
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.movie.title} - {self.start_time}'


class Booking(models.Model):
    number_of_seats = models.IntegerField(null=False, blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='booking')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='booking')
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.user.username} - {self.show.movie.title} - {self.number_of_seats}'


class SelectedSeat(models.Model):
    price = models.IntegerField()
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='selected_seat')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='selected_seat')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='selected_seat')

    def __str__(self):
        return f"{self.booking.profile.user.username} - {self.seat.seat_number}"


