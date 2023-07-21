from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib import messages
import iyzipay
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import pprint
from django.core.cache import cache


api_key = 'sandbox-kFEyBGlvCujQmNlNMf0BOwEtshltlsYH'
secret_key = 'sandbox-ifmieOrNcWVpAtusSLdpBRlpbbanbT8J'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()
# ödeme fonksiyonu
def payment(request):
    context = dict()
    kullanici = request.user
    odeme = Odeme.objects.get(user=kullanici, odendiMi = False)
    fiyat = odeme.total
    buyer={
        'id': 'BY789',
        'name': kullanici.username,
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': str(kullanici.last_login),
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': float(fiyat),
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/payment/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    try:
        json_content = json.loads(content)
    except json.decoder.JSONDecodeError as e:
        print("JSONDecodeError:", str(e))
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    token = json_content['token']
    cache.set('token', token)
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(f'<div id="iyzipay-checkout-form" class="responsive">{json_content["checkoutFormContent"]}</div>')


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')
    token = cache.get('token')
    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)



def success(request):
    odeme  = Odeme.objects.get(user=request.user, odendiMi = False)
    odeme.odendiMi = True
    odeme.save()
    sepetim = Sepet.objects.filter(ekleyen = request.user, odendiMi = False)
    for i in sepetim:
        i.odendiMi = True
        i.save()
    messages.success(request, 'Ödeme Başarılı')
    return redirect('index')


def fail(request):
    messages.error(request, 'Ödeme Başarısız ! Tekrar Deneyin')
    return redirect('sepetim')


# index fonksiyonu
def index(request):
    kategoriler = Kategori.objects.all()
    alt_kategoriler = AltKategori.objects.all()
    alt_alt_kategoriler = AltAltKategori.objects.all()
    urunler = Urun.objects.all() 
    uruns = Sepet.objects.filter(ekleyen = request.user, odendiMi = False)
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        urunler = Urun.objects.filter(
            Q(isim__icontains=search) |
            Q(kategori__isim__icontains=search) |
            Q(alt_kategori__isim__icontains=search) |
            Q(alt_alt_kategori__isim__icontains=search)
        )
    if request.user.is_authenticated:
        favori_listesi = [favori.urun.id for favori in Favori.objects.filter(kullanici=request.user)]
    else:
        favori_listesi = []    
    if request.method == 'POST':
        if request.user.is_authenticated:
            urunId = request.POST['urunId']
            adet = request.POST['adet']
            urunum = Urun.objects.get ( id = urunId)
            if Sepet.objects.filter(ekleyen = request.user, urun = urunum, odendiMi = False).exists():
                sepet = Sepet.objects.get(ekleyen = request.user, urun = urunum, odendiMi = False)
                sepet.adet += int(adet)
                sepet.save()
            else:
                sepet = Sepet.objects.create(
                    ekleyen = request.user,
                    urun = urunum,
                    adet = adet,
                    total = urunum.fiyat * int(adet)
                )
                sepet.save()
            return redirect('index')
        else: 
            messages.warning(request,'Lütfen giriş yapıız !')
            return redirect('login')
    context = {
        'alt_alt_kategoriler': alt_alt_kategoriler,
        'alt_kategoriler' : alt_kategoriler,
        'kategoriler':kategoriler,
        'urunler' : urunler,
        'search' : search,
        'uruns' : uruns,
        'favori_listesi': favori_listesi, 
    }
    return render(request, 'index.html', context)

# ürün fonksiyonu
def urun(request, urunId):
    urunum = Urun.objects.get(id = urunId)
    context = {
        'urun' : urunum,
    }
    return render(request, 'detail.html', context)

def olustur(request):
    form = UrunForm()
    if request.method == 'POST':
        form = UrunForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'olustur.html', context)



# sepet fonksiyonu
def sepetim(request):
    urunler = Sepet.objects.filter(ekleyen = request.user, odendiMi = False)
    uruns = Sepet.objects.filter(ekleyen = request.user, odendiMi=False)
    toplam = 0
    for i in urunler:
        toplam += i.total

    
    if request.method == 'POST':
        if 'odeme' not in request.POST:
            sepetId = request.POST['sepetId']
            sepet = Sepet.objects.get(id = sepetId)
        if 'sil' in request.POST:
            sepet.delete()
            messages.success(request, 'Ürün Silindi !')
            return redirect('sepetim')
        elif 'guncelle' in request.POST:
            adet = request.POST['adet']
            if adet == '0':
                 sepet.delete()
                 messages.warning(request, 'Ürün sepetten kaldırıldı !')
            else:
                sepet.adet = adet
                sepet.save()
                messages.success(request, 'Sepet Güncellendi !')
                return redirect('sepetim')
        elif 'odeme' in request.POST:
            if Odeme.objects.filter(user=request.user, odendiMi=False).exists():
                pass
            else:
                odeme = Odeme.objects.create(
                    user = request.user,
                    total = toplam,
                )
                odeme.urunler.add(*urunler)
                odeme.save()
            return redirect('payment')
    context = {
        'urunler':urunler,
        'toplam' : toplam,
        'uruns' : uruns,
    }
    return render(request, 'sepetim.html', context)


# Favoriye ürün eklemek için fonksiyon
def favori_ekle(request, urun_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Favori eklemek için giriş yapmalısınız.")
        return redirect('login')

    try:
        urun = Urun.objects.get(id=urun_id)
        if Favori.objects.filter(kullanici=request.user, urun=urun).exists():
            messages.info(request, "Bu ürün zaten favorilere eklenmiş.")
        else:
            favori = Favori(kullanici=request.user, urun=urun)
            favori.save()
            messages.success(request, "Ürün favorilere eklendi.")
    except Urun.DoesNotExist:
        messages.warning(request, "Böyle bir ürün bulunamadı.")

    return redirect('index')
# Favoriden ürün kaldırmak için fonksiyon
def favori_kaldir(request, urun_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Favori kaldırmak için giriş yapmalısınız.")
        return redirect('login')

    favori = Favori.objects.get(id=urun_id)
    if Favori.objects.filter(kullanici=request.user, urun=favori.urun).exists():
        Favori.objects.filter(kullanici=request.user, urun=favori.urun).delete()
        messages.success(request, "Ürün favorilerden kaldırıldı.")

    return redirect('favorilerim')

# Favorileri göstermek için fonksiyon
def favorilerim(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Favorilerinizi görmek için giriş yapmalısınız.")
        return redirect('login')

    favoriler = Favori.objects.filter(kullanici=request.user)
    favori_sayisi = favoriler.count()
    context = {
        'favoriler': favoriler,
        'favori_sayisi': favori_sayisi,
    }
    return render(request, 'favori.html', context)

# hata fonksiyonu
def view_404(request, exception):
    return redirect('/')

def view_500(request):
    return render(request, 'hata.html')


