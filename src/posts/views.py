from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm
from urllib import quote_plus



def post_create(request):

	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(reverse('posts:detail', args=(instance.id,)))

	context = {"form":form}

	return render(request,"post_form.html",context)



def post_detail(request,id=None):

	instance = get_object_or_404(Post, id=id)
	
	context = {"instance":instance,
				}
	return render(request, "post_detail.html", context)



def post_list(request):

	query_list = Post.objects.all().order_by("-timestamp")
	paginator = Paginator(query_list, 6)
	page = request.GET.get('page')
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)
	context = {"query":query,}
	return render(request, "index.html", context)

    


def post_update(request, id=None):

	instance = get_object_or_404(Post, id=id)

	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Updated")
		return HttpResponseRedirect(reverse('posts:detail', args=(id,)))

	context = {"instance":instance,
				"form":form,}
	return render(request, "post_form.html", context)



def post_delete(request,id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return HttpResponseRedirect(reverse('posts:home'))

