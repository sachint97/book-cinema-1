from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(Movie)
admin.site.register(Media)
admin.site.register(Theater)
admin.site.register(Screen)
admin.site.register(Seat)
admin.site.register(Show)
admin.site.register(Booking)
admin.site.register(SelectedSeat)

