from django.contrib import admin

from posts.models import Post

class  PostModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","timestamp", "updated","title",]
	list_filter = ["updated","timestamp",]
	search_fields = ["title","content",]
	list_editable = ["title",]
	class Meta:
			model = Post


admin.site.register(Post, PostModelAdmin)
