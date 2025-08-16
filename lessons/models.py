from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

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
        'skills.Skill',
        on_delete=models.PROTECT,
        related_name='lessons',
        help_text='The skill that the lesson is about.'
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    delivery_type = models.CharField(max_length=10, choices=DeliveryType.choices, default=DeliveryType.ONLINE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    duration = models.PositiveBigIntegerField(help_text='Duration of the lesson per session in minutes.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text='Indicates if the lesson is currently active.')

    class Meta:
        indexes = [
            models.Index(fields=['mentor', 'skill']),
            models.Index(fields=['price']),
        ]
        ordering = ['title']

    def clean(self):
        #Ensure that the mentor has the skill they are teaching
        mentor_skills = getattr(self.mentor, "mentor_skill_id", None)
        if mentor_skills is None:
            raise ValidationError('Mentor does not have mentor_skill_set.')
        if mentor_skills != self.skill_id:
            raise ValidationError('Mentor must have the skill they are teaching.')
        

    def __str__(self):
        return f"{self.title} by {self.mentor} ({self.skill})"
    