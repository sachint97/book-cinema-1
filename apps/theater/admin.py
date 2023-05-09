from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(Movie)
admin.site.register(Media)
admin.site.register(Theater)
admin.site.register(Screen)
admin.site.register(Show)
admin.site.register(ScreenShowMapper)
admin.site.register(SeatingClass)
admin.site.register(Fare)
admin.site.register(Seat)


