from django.db import models
from django.template.defaultfilters import slugify
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return str(self.id)


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SlugModel, self).save(*args, **kwargs)
