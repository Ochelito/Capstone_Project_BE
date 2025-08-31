from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Define possible roles for users
class Role(models.TextChoices):
    LEARNER = 'LEARNER', _('Learner')  # Standard learner
    MENTOR = 'MENTOR', _('Mentor')    # Standard mentor
    BOTH = 'both', _('Both')           # Can act as both learner and mentor

# Custom User model extending Django's AbstractUser
class User(AbstractUser):

    # User role: determines if user is a learner, mentor, or both
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.LEARNER,
        help_text=_('Designates whether the user is a learner, mentor, or both.'),
    )

    # Skill taught by the mentor (required for MENTOR/BOTH)
    # Many mentors can teach the same skill
    mentor_skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentors',
        help_text=_('The skill that the mentor teaches (required for MENTOR/BOTH).'),
    )

    # Skills that a learner wants to learn or has acquired (many-to-many)
    learner_skills = models.ManyToManyField(
        'skills.Skill',
        blank=True,
        related_name='learners',
        help_text=_('The skills that the learner wants to learn or has acquired.'),
    )

    # Optional user biography
    bio = models.TextField(
        blank=True,
        default='',
    )

    # Optional profile picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )

    # Optional location string
    location = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    class Meta:
        constraints = [
            # Enforce consistency:
            # - Mentors or BOTH roles must have a mentor_skill assigned
            # - Learners cannot have a mentor_skill assigned
            models.CheckConstraint(
                name='mentor_skill_required_for_mentor',
                check=(
                    Q(role__in=[Role.MENTOR, Role.BOTH], mentor_skill__isnull=False) |
                    Q(role=Role.LEARNER, mentor_skill__isnull=True)
                ),
            ),
        ]

    def __str__(self):
        # Display username as string representation
        return self.username