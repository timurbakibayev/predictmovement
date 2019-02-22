from django.db import models

# Create your models here.
class Last(models.Model):
    last_file = models.TextField(default="df.png",max_length=1000, blank=False, null=False)
