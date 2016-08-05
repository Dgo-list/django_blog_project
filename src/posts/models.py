from __future__ import unicode_literals
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from markdown_deux import markdown
from django.utils.safestring import mark_safe

# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length = 120)	
	slug = models.SlugField(unique=True)
	image = models.FileField(null=True,blank=True)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.title

	def get_markdown(self):
		content = self.content
		return mark_safe(markdown(content))
		

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug



def pre_save_post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever, sender=Post)