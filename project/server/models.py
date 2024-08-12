from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_delete
from server.signals import post_delete_category_icon_file
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icons/{filename}"


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.FileField(upload_to=category_icon_upload_path, blank=True)

    def save(self, *args, **kwargs):
        # Check if this is a new instance (without an id)
        if not self.id:
            # Save the instance without the icon first to get an ID
            temp_icon = self.icon
            self.icon = None
            super().save(*args, **kwargs)
            self.icon = temp_icon

        # Now that the instance has an ID, save it again to store the icon in the correct path
        if self.id and 'force_insert' not in kwargs:
            """
            "force_insert" is a flag that is set to True when the instance is being saved for the first time.
            So if "force_insert" is not in kwargs, it means the instance is being updated.
            """

            # Delete the existing icon if it is being updated
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                try:
                    existing.icon.delete(save=False)
                except Exception as e:
                    logger.error(f"Error deleting icon file for category: {self.id}. error: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_servers"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category_servers"
    )
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        User,
        help_text="Members of the server"
    )

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_channels"
    )
    topic = models.CharField(max_length=100, blank=True)
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="server_channels"
    )
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


post_delete.connect(post_delete_category_icon_file, sender=Category)
