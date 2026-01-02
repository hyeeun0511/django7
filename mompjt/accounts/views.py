from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

import random

from .forms import SignUpForm
from .models import User


# =========================
# ✅ 이메일 인증번호 발송/검증 (회원가입 페이지 내부)
# =========================

@require_POST
def send_email_code(request):
    email = (request.POST.get("email") or "").strip()

    if not email:
        return JsonResponse({"ok": False, "error": "이메일을 입력해 주세요."})

    # ✅ 중복 체크
    if User.objects.filter(email=email).exists():
        return JsonResponse({"ok": False, "error": "이미 사용 중인 이메일입니다."})

    code = f"{random.randint(0, 999999):06d}"

    request.session["email_verify_code"] = code
    request.session["email_verify_target"] = email
    request.session["email_verify_tries"] = 0
    request.session["email_verify_sent_at"] = int(timezone.now().timestamp())
    request.session.pop("verified_email", None)  # 이메일 바뀌면 인증 초기화

    subject = "[맘스로그] 이메일 인증번호"
    message = f"인증번호: {code}\n\n5분 이내에 입력해 주세요."

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    except Exception as e:
        print("send_email_code mail error:", e)
        return JsonResponse({"ok": False, "error": "메일 발송에 실패했습니다."})

    return JsonResponse({"ok": True})


@require_POST
def verify_email_code(request):
    email = (request.POST.get("email") or "").strip()
    code = (request.POST.get("code") or "").strip()

    if not email or not code:
        return JsonResponse({"ok": False, "error": "이메일과 인증번호를 입력해 주세요."})

    target = request.session.get("email_verify_target")
    saved = request.session.get("email_verify_code")
    tries = int(request.session.get("email_verify_tries") or 0)
    sent_at = int(request.session.get("email_verify_sent_at") or 0)

    if not target or not saved or target != email:
        return JsonResponse({"ok": False, "error": "인증번호를 다시 요청해 주세요."})

    # ✅ 5분(300초) 만료
    now_ts = int(timezone.now().timestamp())
    if now_ts - sent_at > 300:
        return JsonResponse({"ok": False, "error": "인증번호가 만료되었습니다. 다시 요청해 주세요."})

    # ✅ 최대 5회
    if tries >= 5:
        return JsonResponse({"ok": False, "error": "시도 횟수를 초과했습니다. 다시 요청해 주세요."})

    if code != saved:
        request.session["email_verify_tries"] = tries + 1
        return JsonResponse({"ok": False, "error": "인증번호가 올바르지 않습니다."})

    # ✅ 성공
    request.session["verified_email"] = email
    return JsonResponse({"ok": True})


# =========================
# 1. 회원가입
# =========================
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        terms_agreed = request.POST.get('terms_agreed')
        if not terms_agreed:
            messages.error(request, "이용약관 및 개인정보 처리방침에 동의해 주세요.")

        if terms_agreed and form.is_valid():
            # ✅ 이메일 인증 완료 체크(세션)
            verified_email = (request.session.get("verified_email") or "").strip()
            form_email = (form.cleaned_data.get("email") or "").strip()

            if not verified_email or verified_email != form_email:
                messages.error(request, "이메일 인증을 먼저 완료해 주세요.")
                return render(request, 'accounts/signup/signup.html', {'form': form})

            user = form.save(commit=False)
            user.terms_agreed = True

            # ✅ 인증번호 인증 통과 → 바로 활성
            user.is_active = True
            user.save()
            form.save_m2m()

            # ✅ 가입 완료 후 로그인
            login(request, user)

            # ✅ 인증 세션 정리(선택)
            request.session.pop("email_verify_code", None)
            request.session.pop("email_verify_target", None)
            request.session.pop("email_verify_tries", None)
            request.session.pop("email_verify_sent_at", None)
            request.session.pop("verified_email", None)

            messages.success(request, "가입이 완료되었습니다. 로그인 되었습니다!")
            return redirect('/')

        if form.errors:
            print("회원가입 실패:", form.errors)

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup/signup.html', {'form': form})


# =========================
# 2. 로그인
# =========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        return render(request, 'accounts/login/login.html', {'form': form})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login/login.html', {'form': form})


# =========================
# 3. 로그아웃
# =========================
def logout_view(request):
    logout(request)
    return redirect('/')


# =========================
# 4. 아이디 중복 확인 (AJAX)
# =========================
@require_GET
def check_id(request):
    username = (request.GET.get('username') or '').strip()
    UserModel = get_user_model()

    if not username:
        return JsonResponse({'exists': True})

    try:
        exists = UserModel.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        print(f"ID Check Error: {e}")
        return JsonResponse({'exists': True})


# =========================
# 5. 닉네임 중복 확인 (AJAX)
# =========================
@require_GET
def check_nickname(request):
    nickname = (request.GET.get('nickname') or '').strip()
    UserModel = get_user_model()

    if not nickname:
        return JsonResponse({'exists': True})

    try:
        exists = UserModel.objects.filter(nickname=nickname).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        print(f"Nickname Check Error: {e}")
        return JsonResponse({'exists': True})


# =========================
# 6. 이메일 중복 확인 (AJAX)
# =========================
@require_GET
def check_email(request):
    email = (request.GET.get('email') or '').strip()
    exists = False
    if email:
        exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})


# =========================
# 7. 비밀번호 찾기
# =========================
def find_pw(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            UserModel = get_user_model()
            user = UserModel.objects.get(username=username, email=email)

            import string
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            user.set_password(temp_password)
            user.save()

            subject = '[맘스로그] 임시 비밀번호 발급 안내'
            message = f'''
안녕하세요, {user.real_name}님

임시 비밀번호가 발급되었습니다.

아이디: {user.username}
임시 비밀번호: {temp_password}

로그인 후 반드시 비밀번호를 변경해 주세요.

감사합니다.
맘스로그 드림
            '''

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                context['found'] = True
            except Exception as e:
                print(f"이메일 발송 실패: {e}")
                context['error'] = f"임시 비밀번호 생성에는 성공했으나 이메일 발송에 실패했습니다. 관리자에게 문의하세요. (임시 비밀번호: {temp_password})"

        except User.DoesNotExist:
            context['error'] = "입력하신 아이디와 이메일이 일치하는 회원 정보를 찾을 수 없습니다."

    return render(request, 'accounts/find_pw.html', context)


# =========================
# 8. 아이디 찾기
# =========================
def find_id(request):
    context = {}
    if request.method == 'POST':
        real_name = request.POST.get('real_name')
        email = request.POST.get('email')

        try:
            UserModel = get_user_model()
            user = UserModel.objects.get(real_name=real_name, email=email)
            context['found_id'] = user.username
        except UserModel.DoesNotExist:
            context['error'] = "일치하는 회원 정보를 찾을 수 없습니다."

    return render(request, 'accounts/find_id.html', context)


# =========================
# 9. 비밀번호 확인 (검문소)
# =========================
@login_required
def profile_auth(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        if request.user.check_password(password):
            request.session['is_verified'] = True
            return redirect('accounts:profile')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')

    return render(request, 'accounts/profile_auth.html')


# =========================
# 10. 마이페이지
# =========================
@login_required
def profile(request):
    if not request.session.get('is_verified'):
        return redirect('accounts:profile_auth')

    return render(request, 'accounts/profile.html')
