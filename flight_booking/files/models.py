from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class File(models.Model):
    """
        file upload model
        has a one to one relationship with User
    """
    file = models.FileField(blank=False, null=False)
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.file.name
