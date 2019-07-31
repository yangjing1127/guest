from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest


# Create your views here.
def index(request):
    # return HttpResponse("Hello yangjing !")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error'})
    return


def login_action_2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin123':
            # return HttpResponse('Login Success')
            response = HttpResponseRedirect('/event_manage')
            # response.set_cookie('user',username,3600)
            request.session['user'] = username;
            return response
            # return HttpResponseRedirect('/event_manage/')
        else:
            return render(request, 'index.html', {'error': 'username or password error'})


# @login_required("accounts/login/")
def event_manege(request):
    # username=request.COOKIES.get('user','')
    event_list = Event.objects.all()
    username = request.session.get('user', '')

    return render(request, "event_manage.html", {'user': username, "events": event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})


@login_required
def search_guest_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("realname", "")
    guest_list = Guest.objects.filter(realname__contains=search_name)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    # return render(request,'sign_index.html'),{'event':event}
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event  or phone error'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success', 'guest': result})
    return render(request, 'sign_index.html'), {'event': event}


@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
