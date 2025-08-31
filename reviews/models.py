from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User, Role
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    """
    Represents a review given by a learner for a completed booking.
    Can be associated generically with different types of objects (lessons, courses, etc.).
    """
    # The learner who wrote the review
    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True, 
        related_name='reviews',
        limit_choices_to={'role': Role.LEARNER},  # Only learners can write reviews
        help_text='The learner who wrote the review.'
    )
    
    # Generic relation to allow the review to be linked to any content type
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='reviews',    
    )
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')  # Access the related object directly

    # The specific booking this review is associated with
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Exactly one, and the booking associated with this review.'
    )

    rating = models.PositiveSmallIntegerField(
        help_text='Rating given by the learner, from 1 (worst) to 5 (best).'
    )
    comment = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(
        default=timezone.now, 
        help_text='The date and time when the review was created.'
    ) 

    class Meta:
        # Ensure a learner cannot review the same object twice
        unique_together = ('learner', 'content_type', 'object_id')
        indexes = [models.Index(fields=['rating'])]  # Index rating for faster queries/aggregations
        ordering = ['-created_at']  # Most recent reviews appear first

    def clean(self):
        """
        Custom validation logic:
        1. Booking must be completed before creating a review.
        2. Rating must be between 1 and 5.
        """
        from bookings.models import Booking

        # Ensure the booking has been completed
        if self.booking.status != Booking.Status.COMPLETED:
            raise ValidationError('Review can only be created for completed bookings.')
        
        # Ensure rating is within valid bounds
        if not (1 <= int(self.rating) <= 5):
            raise ValidationError('Rating must be between 1 and 5.')
        
    def __str__(self):
        """
        Display format for the admin and debug purposes.
        """
        return f"Review by {self.learner.username} on {self.content_object}"