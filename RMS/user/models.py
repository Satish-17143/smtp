from django.db import models

# Create your models here.

class smtp(models.Model):
    Name = models.CharField(max_length=256)
    Phone=models.IntegerField()
    Email=models.CharField(max_length=256)
    Location = models.CharField(max_length=256)
    Message=models.CharField(max_length=256)
    
    def __str__(self):
        return self.Name