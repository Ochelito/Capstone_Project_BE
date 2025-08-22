from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User, Role
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True, 
        related_name='reviews',
        limit_choices_to={'role': Role.LEARNER},
        help_text='The learner who wrote the review.'
    )
    
    #Generic relationship
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='reviews',    
    )
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Exactly one, and the booking associated with this review.'
    )

    rating = models.PositiveSmallIntegerField(help_text='Rating given by the learner, from 1(worst) to 5(best).')
    comment = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(default=timezone.now, help_text='The date and time when the review was created.') 

    class Meta:
        #prevent duplicate reviews for the same booking by the same learner
        unique_together = ('learner', 'content_type', 'object_id')
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
        return f"Review by {self.learner.username} on {self.content_object}"
    