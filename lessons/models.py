from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from skills.models import Skill

# Create your models here.
class Lesson(models.Model):
    class DeliveryType(models.TextChoices):
        IN_PERSON = 'IN_PERSON', 'In Person'
        ONLINE = 'ONLINE', 'Online'
        HYBRID = 'HYBRID', 'Hybrid'

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        limit_choices_to={'role__in': ['MENTOR', 'BOTH']},
        help_text='The mentor who conducts the lesson.'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name='lessons',
        help_text='The skill that the lesson is about.'
    )

    title = models.CharField(max_length=100)
    content_url = models.URLField(blank=True, null=True, help_text='URL to the lesson content, e.g., video or document.')
    description = models.TextField(blank=True, default='')
    delivery_type = models.CharField(max_length=10, choices=DeliveryType.choices, default=DeliveryType.ONLINE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    order = models.PositiveIntegerField(default=0, help_text='Order of the lesson in the list of lessons for a skill.')
    duration = models.PositiveBigIntegerField(help_text='Duration of the lesson per session in minutes.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text='Indicates if the lesson is currently active.')

    class Meta:
        indexes = [
            models.Index(fields=['mentor', 'skill']),
            models.Index(fields=['price']),
        ]
        ordering = ['order']

    def clean(self):
        if self.skill.mentor != self.mentor:
            raise ValidationError("A lesson can only be created by the mentor who owns this skill.")
        

    def __str__(self):
        return f"{self.skill.name} - {self.title}"
    