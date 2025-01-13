from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Event  # Post 모델 가져오기
from .forms import PostForm, EventForm
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



# def calendar_view(request):
#     # 현재 날짜 가져오기
#     today = date.today()
#     year = request.GET.get('year', today.year)
#     month = request.GET.get('month', today.month)

#     # 해당 월의 일정 가져오기
#     events = Event.objects.filter(
#         start_date__year=year,
#         start_date__month=month
#     )

#     # 달력 생성
#     cal = calendar.Calendar()
#     month_days = cal.monthdayscalendar(int(year), int(month))

#     # 일정 데이터와 함께 템플릿으로 전달
#     return render(request, 'calender2.html', {
#         'year': year,
#         'month': month,
#         'month_days': month_days,
#         'events': events
#     })

# # def calendar_view(request):
# #     events = Event.objects.all()  # 모든 일정 가져오기
# #     return render(request, 'calendar2.html', {'events': events})

# def add_event(request):     
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('calendar2')
#     else:
#         form = EventForm()
#     return render(request, 'add_event.html', {'form': form})


# def calendar_view(request):
#     events = Event.objects.all()  # 모든 일정 가져오기
#     return render(request, 'calendar2.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # 일정을 저장
            return redirect('calendar')  # 캘린더 페이지로 리디렉션
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def calendar_view(request):
    # 현재 날짜와 월
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # 달력 시작과 끝 날짜 계산 (예: 2025년 1월)
    first_day = datetime(current_year, current_month, 1)
    last_day = datetime(current_year, current_month + 1, 1) - timedelta(days=1)
    
    print(f"Events: {events}")
    try:
        # 해당 월의 모든 이벤트 가져오기
        events = Event.objects.filter(start_date__month=current_month, start_date__year=current_year)
    except Exception as e:
        # 예외가 발생한 경우 로그에 기록하고, events는 빈 쿼리셋으로 설정
        print(f"Error fetching events: {e}")
        events = Event.objects.none()  # 빈 쿼리셋    
    # 해당 월의 모든 이벤트 가져오기
    events = Event.objects.filter(start_date__month=current_month, start_date__year=current_year)

    # 달력에 표시할 날짜 목록
    month_days = []
    for day in range(1, last_day.day + 1):
        date = datetime(current_year, current_month, day)
        month_days.append(date)

    # 일정을 날짜별로 저장 (날짜 -> 일정 목록)
    event_dict = {}
    for event in events:
        if event.start_date.date() not in event_dict:
            event_dict[event.start_date.date()] = []
        event_dict[event.start_date.date()].append(event)

    return render(request, 'calendar2.html', {
        'month_days': month_days,
        'event_dict': event_dict,
        'today': today,
        'current_month': current_month,
        'current_year': current_year,
    })