from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm
# Create your views here


logger = logging.getLogger(__name__)

class PostListView(ListView):
    queryset = Post.draft.all()
    context_object_name = "posts"
    paginate_by = 1
    template_name = "blog/post/list.html"



def post_list(request):
        post_list  = Post.draft.all()
        paginator = Paginator(post_list, 1)
        page_number = request.GET.get("page", 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, "blog/post/list.html",
        {"posts": posts}
        
    )



def post_detail(request,year, month, day, post):
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found")
    post = get_object_or_404(Post, status = Post.Status.DRAFT, 
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )

    logger.info('post ' + str(id) + " title " + post.title )
    return render(request, "blog/post/detail.html", {"post":post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.DRAFT)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ... end email

    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form})
    