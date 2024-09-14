from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.decorators import login_required  # 로그인 필수 데코레이터 추가
from .forms import SignUpForm
from django.contrib import messages  # 메시지 프레임워크 가져오기
from django.db.models import Q  # Q 객체를 사용하여 OR 조건을 처리
# from django.contrib.auth.forms import UserCreationForm



@login_required
def post_list(request):
    query = request.GET.get('q')  # 검색어 입력값을 받음
    posts = None
    
    if request.user.is_superuser:  # 어드민은 모든 게시글을 볼 수 있음
        posts = Post.objects.all()

    elif request.user.is_manager:  # 중간 관리자는 지부 내의 게시글만 볼 수 있음
        posts = Post.objects.filter(branch=request.user.branch)
    
    else:  # 일반 사용자는 자신의 게시글만 볼 수 있음
        posts = Post.objects.filter(user=request.user)

    # 검색어가 입력된 경우 필터링
    if query:
        posts = posts.filter(
            Q(store_name__icontains=query) |  # 매장명 필터링
            Q(user__username__icontains=query) |  # 작성자 필터링
            Q(branch__name__icontains=query)  # 지부 필터링 (지부 이름에 따라 필터링)
        )

    return render(request, 'board/post_list.html', {'posts': posts, 'query': query})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 어드민이거나, 해당 게시글 작성자만 게시글을 볼 수 있음
    if request.user == post.user or request.user.is_superuser:
        return render(request, 'board/post_detail.html', {'post': post})
    else:
        return render(request, 'board/no_access.html')  # 접근 권한이 없을 때
    

@login_required  # 로그인한 사용자만 접근 가능
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # 파일과 데이터를 처리
        if form.is_valid():
            post = form.save(commit=False)  # 아직 DB에 저장하지 않음
            post.user = request.user  # 로그인한 사용자(request.user)를 작성자로 할당
            post.save()  # 작성자를 할당한 후 저장
            return redirect('post_list')  # 성공적으로 저장 후 리다이렉트
        else:
            print(form.errors)  # 에러 확인용
    else:
        form = PostForm()

    return render(request, 'board/post_create.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/accounts/login/')
    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # 폼 검증
            form.save()  # 유저 저장
            messages.success(request, '회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.')  # 성공 메시지 추가
            return redirect('login')  # 회원가입 후 리디렉션
        else:
            # 폼이 유효하지 않은 경우 오류 메시지를 포함한 폼을 다시 렌더링
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})