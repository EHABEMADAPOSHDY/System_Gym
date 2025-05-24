from django.shortcuts import render ,redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from .froms import *
from django.db.models import Q
# Create your views here.



def system(request):
    search = Subscriber.objects.all().order_by('-id')

    search_type = request.GET.get('search_type', 'name') 
    search_query = request.GET.get('search_query')

    if search_query:
        if search_type == 'name':
            search = search.filter(name__icontains=search_query)
        elif search_type == 'mobile':
            search = search.filter(mobil1__icontains=search_query)
        elif search_type == 'coach':  
            search = search.filter(Type_of_training__name__icontains=search_query)

    context = {
        'information': search,
    }
    return render(request, 'parts/index.html', context)


def update(request, id):
    update_id = get_object_or_404(Subscriber, id=id)

    if request.method == 'POST':
        update_save = SubscriberForm(request.POST, instance=update_id)
        if update_save.is_valid():
            update_save.save()
            return redirect('index')
    else:
        update_save = SubscriberForm(instance=update_id)

    context = {
        'form': update_save
    }
    return render(request, 'parts/update.html', context)

def delete(request,id):
    delete_id = get_object_or_404(Subscriber, id=id)
    if request.method=='POST':
        delete_id.delete()
        return redirect ('index')
    return render(request , 'parts/delete.html')

def add(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = SubscriberForm()  

    context = {
        'form': form,
    }
    return render(request, 'parts/add.html', context)

#خصم جلسه  لاعبين 
@csrf_exempt
def deduct_session(request):
    name = request.GET.get('name')

    if not name:
        return JsonResponse({'success': False, 'message': 'اسم العميل مفقود.'})

    try:
        sub = Subscriber.objects.get(name__iexact=name)
        if sub.Number_of_sessions and sub.Number_of_sessions > 0:
            sub.Number_of_sessions -= 1
            sub.save()
            return JsonResponse({'success': True, 'new_sessions': sub.Number_of_sessions})
        else:
            return JsonResponse({'success': False, 'message': 'لا توجد جلسات متبقية لهذا اللاعب.'})
    except Subscriber.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'اللاعب غير موجود.'})

#باركود
def print_client(request, client_id):

    client = get_object_or_404(Subscriber, id=client_id)
    return render(request, 'print_client.html', {'client': client})

# 

def search_client(request):
    barcode = request.GET.get('barcode', '').strip().lower()
    client = Subscriber.objects.filter(barcode__icontains=barcode).first()
    if client:
        return JsonResponse({
            'success': True,
            'client': {
                'name': client.name or '',
                'mobil1': client.mobil1,
                'Type_of_training': str(client.Type_of_training),
                'Number_of_sessions': client.Number_of_sessions,
                'Start_date': client.Start_date,
                'Daytime_date': client.Daytime_date,
                'barcode': client.barcode,
                'remaining_amount': client.the_rest or 0  
            }
        })
    else:
        return JsonResponse({'success': False, 'message': 'العميل غير موجود'})