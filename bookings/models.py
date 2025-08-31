from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from users.models import User, Role
from django.utils import timezone

# Booking model represents a scheduled lesson booked by a learner
class Booking(models.Model):
    # Define status choices for a booking
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    # Foreign key to the Lesson being booked
    lessons = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.PROTECT,  # Protect to prevent deletion of lesson with bookings
        related_name='bookings',
    )

    # Learner who made the booking
    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role__in': ['LEARNER', 'BOTH']},  # Only users with learner or both role
    )

    # Scheduled start and end times for the booking
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()

    # Timestamp when booking was created
    booked_at = models.DateTimeField(default=timezone.now)

    # Snapshot of price at the time of booking (for historical reference)
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Currency for the booking
    currency = models.CharField(
        max_length=3,
        default='NGN',
    )

    # Booking status
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Generic relation to support other bookable objects (not just lessons)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=ContentType.objects.get(app_label='lessons', model='lesson').pk,
        help_text='Content type of the booking, e.g., lesson.'
    )
    object_id = models.PositiveIntegerField(
        default=1,
        help_text='ID of the object being booked, e.g., lesson ID.'
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Optional notes added by learner or admin
    notes = models.TextField(blank=True, default='')

    # Timestamps for record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Indexes to optimize queries
        indexes = [
            models.Index(fields=['lessons', 'scheduled_start']),
            models.Index(fields=['learner', 'status']),
        ]
        ordering = ['-scheduled_start']  # Default ordering by latest booking first

    def clean(self):
        """
        Custom validation logic
        - Ensures scheduled_end is after scheduled_start
        - Learner cannot be the mentor of the lesson
        - Currency snapshot must match lesson currency
        """
        # Validate times
        if self.scheduled_end <= self.scheduled_start:
            raise ValidationError('Scheduled_end time must be after the scheduled_start time.')

        # Prevent learner booking their own lesson
        if self.learner_id == self.lesson.mentor_id:
            raise ValidationError('Learner cannot be the mentor of the lesson.')

        # Ensure currency consistency
        if self.currency != self.lesson.currency:
            raise ValidationError('Booking currency must match the lesson currency.')

    def __str__(self):
        """
        String representation of booking
        """
        return f"Booking #{self.pk} - {self.learner} on {self.lesson} [{self.status}]"