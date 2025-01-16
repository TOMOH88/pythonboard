from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 홈 URL에 뷰 연결
    path('list/', views.post_list, name='list'), # 게시판 페이지
    path('create/', views.create, name='create'), # 게시판 
    path('post/<int:pk>/', views.detail, name='detail'),  # 상세 페이지 URL
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # 게시글 삭제

    path('calender/', views.calender , name='calender'),

    path('fetch_stock_data/', views.fetch_stock_data, name='fetch_stock_data'),

    path('book/', views.fetch_library_data, name='book'),
]
