from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name  =models.CharField(max_length=200, null=True, blank=True)
    last_name   =models.CharField(max_length=200, null=True, blank=True)
    phone_number= models.IntegerField(default=0, unique=True)
    email       =models.EmailField()
    location    =models.CharField(max_length=200, null=True, blank=True)
    emergency_contact = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

















