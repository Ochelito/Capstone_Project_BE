from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Role(models.TextChoices):
        LEARNER = 'LEARNER', _('Learner')
        MENTOR = 'MENTOR', _('Mentor')
        BOTH = 'both', _('Both')

class User(AbstractUser):

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.LEARNER,
        help_text=_('Designates whether the user is a learner, mentor, or both.'),
    )

    #if user is a mentor or both, they must have exactly a skill they teach
    #multiple mentors can teach the same skill(many mentors to one skill)
    mentor_skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentors',
        help_text=_('The skill that the mentor teaches(required for MENTOR/BOTH).'),
    )

    #Learners can have multiple skills they want to learn(many learners to many skills)
    learner_skills = models.ManyToManyField(
        'skills.Skill',
        blank=True,
        related_name='learners',
        help_text=_('The skills that the learner wants to learn or has acquired.'),
    )

    bio = models.TextField(
        blank=True,
        default='',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    class Meta:
        constraints = [
            #for role MENTOR or BOTH, mentor_skill must be set
            # for role LEARNER, mentor_skill must be null

            models.CheckConstraint(
                name='mentor_skill_required_for_mentor',
                check=(
                    Q(role__in=[Role.MENTOR, Role.BOTH], mentor_skill__isnull=False) |
                    Q(role=Role.LEARNER, mentor_skill__isnull=True)
                ),
            ),
        ]

    def __str__(self):
        return self.username