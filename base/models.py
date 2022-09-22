from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    actions = models.IntegerField(default=0)
    division = models.ForeignKey('Division', on_delete=models.DO_NOTHING, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # Auto token creation
    if created:
        Token.objects.create(user=instance)


class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    description = models.CharField(max_length=100)
    secretary = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    protocol = models.FileField(upload_to='documents/', null=True, blank=True)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date) + ' ' + str(self.description)


class Material(models.Model):
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='documents')

    def __str__(self):
        return self.document.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING)
    materials = models.ManyToManyField(Material, related_name='materials', blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    decision = models.BooleanField(blank=True)
    proposal = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.user) + str(self.meeting)
