from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Review(models.Model):
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Exactly one, and the booking associated with this review.'
    )

    rating = models.PositiveSmallIntegerField(help_text='Rating given by the learner, from 1(worst) to 5(best).')
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        indexes = [models.Index(fields=['rating']),]
        ordering = ['-created_at']

    def clean(self):
        #Ensure booking is completed before allowing a review
        from bookings.models import Booking
        if self.booking.status != Booking.Status.COMPLETED:
            raise ValidationError('Review can only be created for completed bookings.')
        
        #Rating bouns
        if not (1 <= int(self.rating) <= 5):
            raise ValidationError('Rating must be between 1 and 5.')
        
    def __str__(self):
        return f"Review for {self.booking} - Rating: {self.rating}/5"
    