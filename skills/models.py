from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]  # Ensure slug is not too long
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='skills')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        unique_together = ('name', 'category') #ensure unique skill names within a category
        indexes=[
            models.Index(fields=['name']),
            models.indexes(fields=['slug']),
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base=f"{self.category.name}-{self.name}"
            self.slug = slugify(self.name)[:200]  # Ensure slug is not too long
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"