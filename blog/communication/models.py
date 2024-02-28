from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Blog(models.Model):
    name = models.CharField(_("name"), max_length=200, db_index=True)
    description = models.TextField(_("description"), blank=True, max_length=5000)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("owner"), 
        related_name='blogs',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.pk})


class Communication(models.Model):
    name = models.CharField(_("name"), max_length=200, db_index=True)
    description = models.TextField(_("description"), blank=True, max_length=10000)
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

    comments = models.ManyToManyField(
        'Comment',
        verbose_name=_("comments"),
        related_name='communications',
        blank=True,
    )

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

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})
    
    