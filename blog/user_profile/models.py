from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from PIL import Image
from tinymce.models import HTMLField


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)
    picture = models.ImageField(_("picture"), upload_to='user_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("user_detail_current", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            image = Image.open(self.picture.path)
            if image.size[0] > 400 or image.size[1] > 300:
                image.resize((400, 300))
                image.save(self.picture.path)
  
                    
class Message(models.Model):
    text = models.TextField(_("text"), blank=True, max_length=10000)
    image = models.ImageField(_("image"), upload_to='message_images/', blank=True, null=True)
    document = models.FileField(_("document"), upload_to='message_documents/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        get_user_model(),
        verbose_name=_("sender"),
        on_delete=models.CASCADE,
        related_name=_("sent_messages"),
        null=True,
    )
    receiver = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("receiver"),
        related_name=_("received_messages"),
    )
           
    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ['timestamp']

    def __str__(self):
        return "{} {} {}".format(
            self.sender,
            _("sent by"),
            self.receiver,
        )
    
    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})
                