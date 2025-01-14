from django.shortcuts import render, get_object_or_404, redirect
from .models import Post  # Post 모델 가져오기
from .forms import PostForm
from django.core.paginator import Paginator
import calendar
from datetime import datetime, timedelta, date


# Create your views here.
# webapp/views.py
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # 최신 게시글 순으로 정렬
    paginator = Paginator(posts, 5)  # 한 페이지에 5개의 게시글만 표시

    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옴
    page_obj = paginator.get_page(page_number)  # 페이지 객체 생성

    return render(request, 'list.html', {'page_obj': page_obj})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})

def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # 게시글 저장
            return redirect('list')  # 게시글 목록 페이지로 리디렉션
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()  # 게시글 삭제
    return redirect('list')  # 게시글 목록 페이지로 리디렉션

def calender(request):
    return render(request, 'calender.html')
