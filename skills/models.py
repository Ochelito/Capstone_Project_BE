from django.db import models
from django.utils.text import slugify

# Model representing a category of skills (e.g., Programming, Design)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name, must be unique
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # URL-friendly version of name

    class Meta:
        ordering = ['name']  # Default ordering when querying categories

    def save(self, *args, **kwargs):
        """
        Automatically generate slug from name if not provided.
        Ensures it doesn't exceed max_length.
        """
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Display name in admin and other contexts


# Model representing a skill under a specific category
class Skill(models.Model):
    name = models.CharField(max_length=100)  # Skill name (e.g., Python, Photoshop)
    description = models.TextField(blank=True, default='')  # Optional skill description
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Prevent deleting category if skills exist
        related_name='skills'
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # URL-friendly slug

    class Meta:
        unique_together = ('name', 'category')  # Skill names must be unique within a category
        indexes = [
            models.Index(fields=['name']),  # Index for faster lookups by name
            models.Index(fields=['slug']),  # Index for faster lookups by slug
        ]
        ordering = ['name']  # Default ordering when querying skills

    def save(self, *args, **kwargs):
        """
        Automatically generate slug based on category and skill name if not provided.
        Ensures slug does not exceed max_length.
        """
        if not self.slug:
            base = f"{self.category.name}-{self.name}"
            self.slug = slugify(base)[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"  # Display skill name with category