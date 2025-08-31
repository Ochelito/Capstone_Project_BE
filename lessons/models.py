from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from skills.models import Skill

# Lesson model representing individual lessons offered by mentors
class Lesson(models.Model):
    # Choices for delivery method of the lesson
    class DeliveryType(models.TextChoices):
        IN_PERSON = 'IN_PERSON', 'In Person'
        ONLINE = 'ONLINE', 'Online'
        HYBRID = 'HYBRID', 'Hybrid'

    # ForeignKey to the mentor who conducts the lesson
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        limit_choices_to={'role__in': ['MENTOR', 'BOTH']},  # Only users with role 'MENTOR' or 'BOTH' can be mentors
        help_text='The mentor who conducts the lesson.'
    )

    # ForeignKey to the skill associated with this lesson
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name='lessons',
        help_text='The skill that the lesson is about.'
    )

    # Basic lesson information
    title = models.CharField(max_length=100)  # Lesson title
    content_url = models.URLField(blank=True, null=True, help_text='URL to the lesson content, e.g., video or document.')
    description = models.TextField(blank=True, default='')  # Optional description
    delivery_type = models.CharField(max_length=10, choices=DeliveryType.choices, default=DeliveryType.ONLINE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per lesson
    currency = models.CharField(max_length=3, default='NGN')  # Currency code
    order = models.PositiveIntegerField(default=0, help_text='Order of the lesson in the list of lessons for a skill.')
    duration = models.PositiveBigIntegerField(help_text='Duration of the lesson per session in minutes.')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp when updated
    is_active = models.BooleanField(default=True, help_text='Indicates if the lesson is currently active.')

    class Meta:
        indexes = [
            models.Index(fields=['mentor', 'skill']),  # Index for faster lookups by mentor and skill
            models.Index(fields=['price']),            # Index for price filtering/sorting
        ]
        ordering = ['order']  # Default ordering by lesson order

    # Custom validation
    def clean(self):
        # Ensure that the mentor of the lesson is the same as the owner of the skill
        if self.skill.mentor != self.mentor:
            raise ValidationError("A lesson can only be created by the mentor who owns this skill.")

    # String representation for easy identification
    def __str__(self):
        return f"{self.skill.name} - {self.title}"