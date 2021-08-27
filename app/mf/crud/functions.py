from django.contrib.auth.models import Group
from mf.crud.models import Dolar, HistoryOperations, Permisology
from mf.user.models import User
from django.utils import timezone
from datetime import date, datetime, timedelta

def convertToDecimalFormat(n):
    return n.replace('.', '').replace(',', '.')

def get_dollar():
    data = []
    try:
        dolar1 = Dolar.objects.using('default').get(pk=1)
        dl1 = float(dolar1.dolar)
    except:
        new_dolar1 = Dolar()
        new_dolar1.dolar = '1000000'
        new_dolar1.save()

        dolar1 = Dolar.objects.using('default').get(pk=1)
        dl1 = float(dolar1.dolar)

    try:
        dolar2 = Dolar.objects.using('default').get(pk=2)
        dl2 = float(dolar2.dolar)
    except:
        new_dolar2 = Dolar()
        new_dolar2.dolar = '1200000'
        new_dolar2.save()

        dolar1 = Dolar.objects.using('default').get(pk=1)
        dl1 = float(dolar1.dolar)
    
    data = {
        'dolar1': dl1,
        'dolar2': dl2
    }

    return data

def ValidatePermissions(perms, requestGroup):
    autorized = False
    try:
        permsRequired = perms
        pk = requestGroup.id

        group = Group.objects.get(pk=pk)
        permsRequired = perms

        for p in permsRequired:
            if not group.permissions.filter(codename=p).exists():
                autorized = False
                break
            else:
                autorized = True
    except:
        autorized = False
    return autorized

def RegisterOperation(db, user, action):
    date = timezone.localtime(timezone.now())
    result = 0
    try:
        h = HistoryOperations()
        h.datejoined = date.strftime('%Y-%m-%d | %H:%M:%S %p')
        h.userSession_id = user
        h.description = action
        h.save()
    except:
        result = 1
    return result

def get_q_events_today():
    data = 0
    try:
        start = date.today()
        end = start + timedelta(days=7)
        start_date = start.strftime('%Y-%m-%d')
        end_date = end.strftime('%Y-%m-%d')
        total = 0

        search = Permisology.objects.all()
        if len(start_date) and len(end_date):
            search = search.filter(day__range=[start_date, end_date])
            for s in search:
                total = int(total) + 1
            data = total
    except:
        pass
    return data

def get_events_today():
    data = []
    total = 0
    start = date.today()
    end = start + timedelta(days=7)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')

    search = Permisology.objects.all()
    if len(start_date) and len(end_date):
        search = search.filter(day__range=[start_date, end_date])
    for s in search:
        data.append(
            {
                'name': s.name,
                'description': s.description,
                'day': s.day.strftime('%Y-%m-%d'),
            }
        )
    return data

