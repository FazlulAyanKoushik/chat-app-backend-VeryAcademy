from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

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
