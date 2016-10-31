from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic.list import ListView
from .forms import CommentForm, EmailPostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', {'page': page,
                                              'posts': posts,
                                              'tag': tag})

class PostListView(ListView):    
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    #List of active comments for this post
    comments = post.comments.filter(active=True)
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to DB
            new_comment = comment_form.save(commit=False)
            # Assign current post to the comment
            new_comment.post = post
            # Save the comment to the database 
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
                        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags', '-publish')[:4]
    
    return render(request, 'post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similiar_posts': similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            # ... send email
            post_url = post.get_absolute_url()
            subject = '{} ({}) recommends you reading "{}"' \
                .format(cd['name'], cd['email'], post.title) 
            message = 'Read "{}" at {}\n\n{}\' comments: {}' \
                .format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@localhost.com', [cd['to'],])
            sent = True
            
    else:
        form = EmailPostForm()
    
    return render(request, 'post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})
    