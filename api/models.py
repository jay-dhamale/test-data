from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    # date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [models.Index(fields=['id', 'username', 'first_name', 'last_name'])]
        # ordering = ['-first_name']

     