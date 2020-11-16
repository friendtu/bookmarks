from django.db import models
from django.conf import settings
# Create your models here.




class Profile(model.Model):
    user=models.OneToOneField(setting.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth=models.DateField(null=True,blank=True)
    photo=models.ImageField(upload_to='uploads/%Y/%m/%d/',blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)