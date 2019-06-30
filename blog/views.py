from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe
from .models import Post, Comment
from .forms import PostForm, CommentForm


from main_calendar.web_calendar import WebCalendar

# Create your views here.

def home(request):
    context = dict()
    today = timezone.localdate()
    if 'year' in request.GET:
        year = int(request.GET.get('year'))
    else:
        year = today.year
    if 'month' in request.GET:
        month = int(request.GET.get('month'))
        if month > 12:
            month = 12
        elif month < 1:
            month = 1
    else:
        month = today.month
    web_calendar = WebCalendar(year=year, month=month)
    web_calendar.set_today(today.year, today.month, today.day)
    calendar = web_calendar.get_calendar_table()
    context['info'] = mark_safe(web_calendar.get_info_div().create_element())
    context['calendar'] = mark_safe(calendar.create_element())
    return render(request, 'blog/mypage.html', context)


def newcomment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('detail', post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/newcomment.html', {'form': form})

def removecomment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('detail', post_id = comment.post.pk)

def board(request):
    posts = Post.objects.all().order_by('-updated_at')
    # paginator = Paginator(posts, 3)
    # page = request.GET.get('page')
    # post_page = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts}) #'post_page': post_page

def new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) # commit은 데이터베이스의 모든 작업이 저장되었을 때 True가 되는데, 그러면 comment를 더이상 수정하지 못 하게 됨, 우선 commit = False를 해서 뒤에 작업들을 할 수 있게 해줌
            post.author = request.user
            post.save()  # 여기는 default가 commit = True라서 따로 설정 안 해줌
            return redirect('blog/home.html')
    else:
        form = PostForm()
    return render(request, 'blog/new.html')

def edit(request, date):
    post=get_object_or_404(Post)
    if request.method=="POST":
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
      
            post.updated_at=timezone.now()
            post.save()
            return redirect('detail.html')
    else:
        form=PostForm(instance=post)
    return render(request,'edit.html', {'form':form})

def detail(request, date):
    print("Detail")
    is_written=False
    context = dict()
    try:
        post = Post.objects.get(author=request.user, diary_date__date=date)
        print(post)
    except Exception as e:
        post = None
        print("No date post")
    if post is not None:
        is_written=True
        context['post'] = post
    context['is_written'] = is_written
    return render(request, 'blog/detail.html', context)
    
    # month = 12
    # elif month < 1:
    #     month = 1
    # else:
    #     month = today.month
    # web_calendar = WebCalendar(year=year, month=month)
    # web_calendar.set_today(today.year, today.month, today.day)
    # calendar = web_calendar.get_calendar_table()
    # context['info'] = mark_safe(web_calendar.get_info_div().create_element())
    # context['calendar'] = mark_safe(calendar.create_element())
    # return render(request, 'blog/mypage.html', context)


def newcomment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('detail', post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/newcomment.html', {'form': form})

def removecomment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('detail', post_id = comment.post.pk)

def board(request):
    posts = Post.objects.all().order_by('-updated_at')
    # paginator = Paginator(posts, 3)
    # page = request.GET.get('page')
    # post_page = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts}) #'post_page': post_page

def new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) # commit은 데이터베이스의 모든 작업이 저장되었을 때 True가 되는데, 그러면 comment를 더이상 수정하지 못 하게 됨, 우선 commit = False를 해서 뒤에 작업들을 할 수 있게 해줌
            post.author = request.user
            post.save()  # 여기는 default가 commit = True라서 따로 설정 안 해줌
            return redirect('detail', post.diary_date)
    else:
        form = PostForm()
    return render(request, 'blog/new.html')

def edit(request, index):
    post=get_object_or_404(Post,pk=index)
    if request.method=="POST":
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.pub_date=timezone.now()
            post.save()
            return redirect('read',index=post.pk)
    else:
        form=PostForm(instance=post)
    return render(request,'edit.html',{'form':form})

def detail(request, date):
    is_written=False
    context = dict()
    try:
        post = Post.objects.get(author=request.user, diary_date=date)
    except Exception as e:
        post = None
    if post is not None:
        is_written=True
        context['post'] = post
    context['is_written'] = is_written
    return render(request, 'blog/detail.html', context)
    
    