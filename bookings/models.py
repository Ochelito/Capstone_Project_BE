from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from users.models import User, Role
from django.utils import timezone

# Create your models here.
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    lessons = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.PROTECT,
        related_name='bookings',
    )

    learner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role__in':['LEARNER', 'BOTH']},
    )

    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    booked_at = models.DateTimeField(default=timezone.now)

    #snapshots of the booking for later price changes 
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        default='NGN',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        default=ContentType.objects.get(app_label='lessons', model='lesson').pk,
        help_text='Content type of the booking, e.g., lesson.'
    )
    object_id = models.PositiveIntegerField(default=1, help_text='ID of the object being booked, e.g., lesson ID.')
    content_object = GenericForeignKey('content_type', 'object_id')

    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        indexes = [
            models.Index(fields=['lessons', 'scheduled_start']),
            models.Index(fields=['learner', 'status']),
        ]
        ordering = ['-scheduled_start']

    def clean(self):
        # Ensure that the booking's scheduled times are valid
        if self.scheduled_end <= self.scheduled_start:
            raise ValidationError('Scheduled_end time must be after the scheduled_start time.')

        # Learner cannot be the mentor of the lesson
        if self.learner_id== self.lesson.mentor_id:
            raise ValidationError('Learner cannot be the mentor of the lesson.')

        #Ensure snapshot currency matches lesson currency
        if self.currency != self.lesson.currency:
            raise ValidationError('Booking currency must match the lesson currency.')
        
    def __str__(self):
        return f"Booking #{self.pk} - {self.learner} on {self.lesson} [{self.status}]"
    