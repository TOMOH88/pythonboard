from django.shortcuts import render, get_object_or_404, redirect
from .models import Post  # Post 모델 가져오기
from .forms import PostForm
from django.core.paginator import Paginator
import calendar
from datetime import datetime, timedelta, date
import yfinance as yf
from .models import StockData
import json
import numpy as np
from django.http import HttpResponse
from .forms import StockForm
import requests
import xml.etree.ElementTree as ET

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




# def fetch_stock_data(request):
#     symbols = ["AAPL", "GOOGL", "MSFT", "OPTT", "NVLD"]
#     stock_data = []

#     for symbol in symbols:
#         stock = yf.Ticker(symbol)
#         hist = stock.history(period="1d")
#         if not hist.empty:
#             current_price = hist["Close"].iloc[-1]
#             stock_data.append({"symbol": symbol, "price": current_price})

#     # 심볼 및 가격을 JSON으로 전달
#     symbols = [stock['symbol'] for stock in stock_data]
#     prices = [stock['price'] for stock in stock_data]

#     return render(request, 'stock_data.html', {
#         "symbols": symbols,
#         "prices": prices,
#     })


# def stock_data_view(request):
#     symbols = ['AAPL', 'GOOGL', 'MSFT']
#     prices = [150, 2800, 299]

#     return render(request, 'stock_data.html', {
#         'symbols': json.dumps(symbols),
#         'prices': json.dumps(prices)
#     })


def fetch_stock_data(request):
    # 기본 설정된 심볼
    symbols = ["AAPL", "GOOGL", "MSFT", "OPTT", "NVDL"]
    stock_data = []

    # 기본 심볼에 대한 데이터 가져오기
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if not hist.empty:
            current_price = hist["Close"].iloc[-1]
            stock_data.append({"symbol": symbol, "price": current_price})

    # POST 요청이 들어올 경우, 데이터를 처리
    if request.method == 'POST':
        symbol = request.POST.get('symbol')  # 사용자가 입력한 심볼

        if symbol and symbol not in symbols:  # 심볼이 비어 있지 않고 중복되지 않으면 추가
            symbols.append(symbol)  # 새로운 심볼 추가

            # 새로 추가된 심볼에 대한 가격 가져오기
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist["Close"].iloc[-1]
                stock_data.append({"symbol": symbol, "price": current_price})

    # 심볼 및 가격 데이터를 JSON으로 변환하여 템플릿에 전달
    symbols = [stock['symbol'] for stock in stock_data]
    prices = [stock['price'] for stock in stock_data]

    # 데이터를 JSON으로 변환하여 템플릿에 전달
    return render(request, 'stock_data.html', {
        'symbols': json.dumps(symbols),
        'prices': json.dumps(prices),
    })





def fetch_library_data(request):
    # API URL 및 인증키
    url = "https://openapi.gg.go.kr/Poplitloanbook"
    api_key = "5d2ea9292e75441a9efdecaa4637c253"  # 발급받은 인증키로 교체

    # 요청 파라미터
    params = {
        'Key': api_key,
        'Type': 'xml',  # XML 형식으로 요청
        'pIndex': 1,     # 페이지 번호
        'pSize': 50      # 한 번에 가져올 데이터 크기
    }

    # API 호출
    response = requests.get(url, params=params)
    rows = []  # 데이터를 저장할 리스트

    if response.status_code == 200:
        try:
            # XML 데이터를 파싱
            root = ET.fromstring(response.content)
            for item in root.findall(".//row"):  # row 태그 검색
                row_data = {
                    'ranking': item.findtext('RKI_NO'),  # 순위번호
                    'title': item.findtext('BOOK_NM_INFO'),  # 도서명정보
                    'author': item.findtext('AUTHOR_NM_INFO'),  # 저자명정보
                    'publisher': item.findtext('PUBLSHCMPY_NM'),  # 출판사명
                    'publication_year': item.findtext('PUBLCATN_YY'),  # 출판년도
                    'volume_count': item.findtext('VOLM_CNT'),  # 권수
                    'book_image_url': item.findtext('BOOK_IMAGE_URL')  # 도서 이미지 URL
                }
                rows.append(row_data)
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
    else:
        print(f"API request failed with status code: {response.status_code}")

    # Django Paginator로 페이징 처리 (5개씩 나누기)
    paginator = Paginator(rows, 5)  # 페이지 당 5개 데이터
    page_number = request.GET.get('page', 1)  # 요청에서 페이지 번호 가져오기 (기본 1)
    page_obj = paginator.get_page(page_number)

    # 데이터를 템플릿에 전달
    return render(request, 'book.html', {'page_obj': page_obj})