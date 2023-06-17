from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Avatar(models.Model):
    src = models.ImageField(
        upload_to="app_users/avatars/user_avatars/",
        default="app_users/avatars/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    def __str__(self):
        return self.src.url


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullName = models.CharField(_("ФИО"), max_length=140, null=True, blank=True)
    phone = models.CharField(_("Номер телефона"), max_length=140, null=True, blank=True)
    email = models.CharField(_("Почта"), max_length=140, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ForeignKey(
        Avatar,
        related_name="profile",
        verbose_name="Аватар",
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        if self.fullName:
            return self.fullName
        return self.user.username
