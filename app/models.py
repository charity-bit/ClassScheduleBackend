from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone

from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    # User Types
    TECHNICAL_MENTOR = "TM"
    STUDENT = "STUD"

    USER_TYPES = ((STUDENT, "Student"), (TECHNICAL_MENTOR, "Technical Mentor"))

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(max_length=4, choices=USER_TYPES, default=STUDENT)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    def save_user(self):
        self.save()

    def delete_user(self):
        self.delete()


class Module(models.Model):
    technical_mentor = models.ForeignKey(
        User, related_name="module_tm", on_delete=models.DO_NOTHING, null=True
    )
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"

    def save_module(self):
        self.save()

    def delete_module(self):
        self.delete()

    @classmethod
    def update_module(cls, name, tm):
        module = cls.objects.filter(technical_mentor=tm).first()
        module.update(name=name)
        module.save()
        return module

    @classmethod
    def get_module_by_id(cls, id):
        module = cls.objects.get(id=id)

        return module


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField("image")
    modules = models.ManyToManyField(Module, blank=True)
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.email}"

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_profile(cls, user, bio):
        profile = cls.objects.filter(user=user).update(bio=bio)

        return profile


class Session(models.Model):
    technical_mentor = models.ForeignKey(
        User, related_name="session_tm", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    meet_url = models.URLField(max_length=255)
    date_of_session = models.DateTimeField()
    module = models.ForeignKey(
        Module, related_name="module_session", on_delete=models.CASCADE
    )
    start = models.TimeField()
    end = models.TimeField()

    def save_session(self):
        self.save()

    def delete_session(self):
        self.delete()

    @classmethod
    def update_session(cls, tm, title, url, date, start, end):
        session = cls.objects.filter(technical_mentor=tm).update(
            title=title, meet_url=url, start=start, end=end, date_of_session=date
        )

        return session

    @classmethod
    def get_session_by_id(cls, id):
        session = cls.objects.get(id=id)

        return session

    def __str__(self):
        return f"{self.title}"


class Announcement(models.Model):
    technical_mentor = models.ForeignKey(
        User, related_name="announcement_tm", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.technical_mentor.email}"

    def save_announcement(self):
        self.save()

    def delete_announcement(self):
        self.delete()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    likes = models.ManyToManyField(User, related_name="likes")
    date_created = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="session"
    )

    def __str__(self):
        return f"{self.user.name}"

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    def get_likes(self):

        likes = self.likes.count()
        # likes = self.likes.all()

        return likes
