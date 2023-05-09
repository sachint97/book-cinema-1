from django.db import models
from apps.user.models import Profile
from apps.theater.models import *
# Create your models here.
class Booking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='booking')
    screen_show = models.ForeignKey(ScreenShowMapper, on_delete=models.CASCADE, related_name='booking')
    booking_date = models.DateField(auto_now_add=False,auto_now=False)


    def __str__(self):
        return f'{self.profile} - {self.screen_show} - {self.booking_date}'


class BookingSeat(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='booking_seat')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_seat')
    booking_status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.booking} - {self.seat}"

class Payment(models.Model):
    pay_methods=(
        ('DEBIT CARD','Debit card'),
        ('CREDIT CARD', 'Credit card'),
        ('NET BANKING' , 'Net banking'),
        ('UPI','UPI')
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20,choices=pay_methods)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='payment')
    coupon = models.CharField(null=True,blank=True,max_length=20)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking} {self.payment_method} {self.payment_status}"

    def save(self, *args, **kwargs):
        booking_seats = BookingSeat.objects.filter(booking=self.booking)
        total_amount = sum([booking_seat.seat.fare.price for booking_seat in booking_seats])
        self.amount = total_amount

        super(Payment, self).save(*args, **kwargs)
