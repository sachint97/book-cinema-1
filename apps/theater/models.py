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
        return f"{self.name}-{self.theater.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='show')
    start_date = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return f'{self.movie.title}:[{self.start_date}-{self.end_date}][{self.start_time}-{self.end_time}]'

class ScreenShowMapper(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='screen_show')
    show = models.ForeignKey(Show,on_delete=models.CASCADE, related_name='screen_show')

    def __str__(self):
        return f"{self.screen} {self.show}"
class SeatingClass(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    slug = models.SlugField(max_length=255, null=True, editable=False)
    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.name)
        self.clean()
        super().save(*args, **kwargs)

class Fare(models.Model):
    screen_show = models.ForeignKey(ScreenShowMapper,on_delete=models.CASCADE, related_name='fare')
    seating_class = models.ForeignKey(SeatingClass,on_delete=models.CASCADE, related_name='fare')
    price = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.screen_show} {self.seating_class}-{self.price}Rs"
class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    fare = models.ForeignKey(Fare,on_delete=models.CASCADE,related_name="seats")
    row = models.IntegerField(null=False, blank=False)
    column = models.IntegerField(null=False,blank=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.screen} {self.fare.seating_class}:Row-{self.row},Column-{self.column}"


