from django.db import models
from django.template.defaultfilters import slugify
import uuid
from utils.constants import SLUG_LENGTH


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
    slug = models.SlugField(unique=True, null=True, default=None, blank=True, max_length=SLUG_LENGTH)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            get_obj_by_slug = self.__class__.objects.filter(slug=self.slug)
            if get_obj_by_slug:
                self.slug = self.slug + "-" + str(self.id)[: int(len(str(self.id)) / 2)]
        super(SlugModel, self).save(*args, **kwargs)
