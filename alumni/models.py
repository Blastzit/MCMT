from django.db import models

class Alumni(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    intro = models.TextField()
    paragraph = models.TextField()
    modules = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    class Meta:
        db_table = 'info'

    def __str__(self):
        return self.name