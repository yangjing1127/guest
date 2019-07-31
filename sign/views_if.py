from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import time


# 添加发布会
def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    if eid == '' or name == '' or limit == '' or status == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})
    if status == '':
        status = 1
        try:
            Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status),
                                 start_time=start_time)
        except ValidationError as  e:
            error = 'start_time formaterror.It must be in YYYY-MM-DD HH:MM:SS format.'
            return JsonResponse({'status': 10024, 'message': error})
        return JsonResponse({'status': 200, 'message': 'add event success'})


# 查询发布会列表
def get_event_list(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 10000, 'message': 'success', 'data': event})
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 添加嘉宾
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    if (eid == '' or realname == '' or phone == '' or email == ''):
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'messsage': 'event id  null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not avaliable'})
    event_limit = Event.objects.get(id=eid).limit
    guest_limit = Guest.objects.filter(event_id=eid)
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status': 10024, 'message': 'event number is full'})
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))
    now_time = str(time.time())  # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})
    try:
        Guest.objects.create(realname=realname, phone=phone, email=email, sign=0, event_id=int(eid))
    except IntegrityError as e:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})
    return JsonResponse({'status': 200, 'message': 'add guest success'})


# 查询嘉宾列表
def get_guest_list(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('real', '')
    phone = request.POST.get('phone', '')
    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'eid cannot be empty'})
    if eid != '' and phone != '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty', 'data': datas})
    if eid != '' and phone != '':
        guest = {}
        try:
            r = Guest.objects.filter(phone=phone, event_id=eid)
            guest['realname'] = r.realname
            guest['phone'] = r.phone
            guest['email'] = r.email
            guest['sign'] = r.sign

            return JsonResponse({'status': 200, 'message': 'success', 'data': guest})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 嘉宾签到
def guest_sign(request):
    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone', '')

    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))
    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)
    if n_time >= e_time:
        return JsonResponse({'status': 10024, "message": 'event has started'})
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, "message": 'phone not exist'})
    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        return JsonResponse({'status': 10026, "message": '用户未参加这场发布会'})
    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status': 10027, "message": '用户已签到'})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
        return JsonResponse({'status': 200, "message": '用户签到成功'})
