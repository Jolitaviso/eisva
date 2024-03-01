from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from tinymce.models import HTMLField


class Blog(models.Model):
    name = models.CharField(_("name"), max_length=200, db_index=True)
    description = HTMLField(_("description"), max_length=10000, null=True, blank=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='blogs',
    )
    youtube_video = models.CharField(
        _('Youtube video'),
        max_length=50, null=True,
        blank=True,
        help_text =_("from Youtube's video URL copy the part after 'https://www.youtube.com/watch?v='.")
    )

    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")
        ordering = ['name']
        
        
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.pk})


class Communication(models.Model):
    name = models.CharField(_("name"), max_length=200, db_index=True)
    description = HTMLField(_("description"), max_length=100000, null=True, blank=True)
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE, 
        verbose_name=_("blog"), 
        related_name='communications',
    )
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='communications',
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("communication")
        verbose_name_plural = _("communications")
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("communication_detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    title = models.CharField(_("title"), max_length=200, db_index=True)
    note = models.TextField(_("note"), blank=True, max_length=10000)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='comments',
    )
    communication = models.ForeignKey(
        Communication,
        on_delete=models.CASCADE,
        verbose_name=_("communication"),
        related_name='comments',
        null=True,
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})
    
class BlogLike(models.Model):
    blog = models.ForeignKey(
        Blog, 
        verbose_name=_("blog"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='blog_likes',
    )
    
    class Meta:
        verbose_name = _("blog like")
        verbose_name_plural = _("blog likes")

    def __str__(self):
        return f"{self.blog} {self.user}"

    def get_absolute_url(self):
        return reverse("blog_like_detail", kwargs={"pk": self.pk})

class CommunicationLike(models.Model):
    communication = models.ForeignKey(
        Communication, 
        verbose_name=_("communication"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='communication_likes',
    )
    
    class Meta:
        verbose_name = _("communication like")
        verbose_name_plural = _("communication likes")

    def __str__(self):
        return f"{self.communication} {self.user}"

    def get_absolute_url(self):
        return reverse("communication_like_detail", kwargs={"pk": self.pk})