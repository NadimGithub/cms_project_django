from django.db import models

class InstituteMaster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    village = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')  # Set default value
    logo = models.ImageField(upload_to='logos/')
    tagline = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

    def __str__(self):
        return self.name
