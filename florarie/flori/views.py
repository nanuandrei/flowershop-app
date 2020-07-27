from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from flori.models import Produse
import time
from flori.forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail

# profil
from flori.forms import UserForm
from flori.models import Useri
from django.contrib.auth.models import User
from django.shortcuts import redirect
from flori.forms import SignUpForm
from django.contrib.auth import login, authenticate

# signup form
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            adress = form.cleaned_data.get('adress')
            phone_number = form.cleaned_data.get('phone_number')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Useri.objects.create(email = email, adresa=adress, telefon = phone_number,
                                 user_id = User.objects.get(username = username).id)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#query for promo day
zi = int(time.strftime('%w'))+1
floare_r = Produse.objects.get(id=zi)
floare_r.pret_cumparare += floare_r.pret_cumparare * 0.4


# Create your views here.
def index(request):
    cart = _extragere_cos(request)
    return render(request, 'index.html', {'floare_r': floare_r, 'cos': sum(cart.values()),
                                          'username':request.user.username})


def listare(request):
    flori = Produse.objects.exclude(id=floare_r.id)
    cart = _extragere_cos(request)
    return render(request, 'listare.html', {'flori': flori, 'floare_r': floare_r, 'cos': sum(cart.values()),
                                            'username':request.user.username})


def entry_detail(request,produs_id):
  try:
    produs = Produse.objects.get(id=produs_id)
  except:
    raise Http404("Produsul nu mai exista in momentul de fata spre vanzare.")
  else:
    cart = _extragere_cos(request)
    return render(request,'entry_detail.html',{'produs':produs, 'zi': zi, 'floare_r': floare_r,
                                               'cos':sum(cart.values()), 'username':request.user.username})


def contact(request):
  cart = _extragere_cos(request)
  if request.method == 'POST':
     form = ContactForm(request.POST)
     if form.is_valid():
         mesaj="Mesaj de la:"+form.cleaned_data['contact_name']+",email:"+\
                 form.cleaned_data['contact_email']+"\n\n"+\
                 form.cleaned_data['content']
         send_mail('Contact prin django', mesaj,  settings.EMAIL_HOST_USER,
                 ['andryushananu@gmail.com'], fail_silently=False)
     return render(request, 'contact_sent.html', {'username':request.user.username, 'cos': sum(cart.values())})
  else:
     return render(request, 'contact.html', {'form': ContactForm, 'username':request.user.username,
                                             'cos': sum(cart.values())})


def profil(request):
  user_is_valid = True
  cart = _extragere_cos(request)
  try:
    user_oficial = User.objects.get(username=request.user.username)
    user = Useri.objects.get(user=user_oficial.id)
  except:
    user_is_valid = False
  if request.method == 'POST':
      form = UserForm(request.POST, instance=user)
      if not user_is_valid :
        return redirect('login')
      elif form.is_valid():
        form.save()
        return redirect('index')
  else:
    if not user_is_valid:
      return redirect('login')
    form = UserForm(instance=user)
  return render(request, 'profil.html', {'form': form, 'username':request.user.username,
                                         'cos': sum(cart.values())})


# cos cumparaturi
from flori.models import Comanda
from django.contrib.auth.decorators import login_required
from flori import views


@login_required
def comanda(request):
  cart = _extragere_cos(request)
  user_oficial = User.objects.get(id=request.user.id)
  for produs,numar in cart.items():
    produs_q = Produse.objects.get(id=produs)
    #if block for promo day
    if produs_q.id == zi:
        pret_achizitie_r = floare_r.pret_cumparare
    else:
        pret_achizitie_r = produs_q.pret
    Comanda.objects.create(
      pret_achizitie = pret_achizitie_r,
      produs = produs_q,
      user = Useri.objects.get(user=user_oficial.id),
      finalizat = False)
    produs_q.stoc -= numar
    produs_q.save()
  request.session['cart'] = {}
  return render(request, 'cart_comandat.html', {'produse': [], 'cos': len(_extragere_cos(request)),
                                                'username': request.user.username, 'titlu': 'cos'})


@login_required
def goleste_cos(request):
    request.session['cart'] = {}
    return render(request, 'cart.html', {'cos': '0',
                                         'username': request.user.username,
                                         'titlu': 'cos'})


def _extragere_cos(request):
  if not request.session.has_key('cart'):
    return {}
  else:
    return request.session['cart']


@login_required
def cos(request):
  cart = _extragere_cos(request)
  produse = []
  for produs,numar in cart.items():
    produs_q = Produse.objects.get(id=produs)
    if produs_q.id == zi:
        produs_q.pret = floare_r.pret_cumparare
    produs_q.numar = numar
    produse.append(produs_q)
  return render(request, 'cart.html', {'produse': produse,
                                       'cos': sum(cart.values()),
                                       'username': request.user.username,
                                            'titlu': 'cos'})


@login_required
def istoric(request):
  produse = []
  cart = _extragere_cos(request)
  produse_query = Comanda.objects.filter(user_id=Useri.objects.get(user=request.user.id).id).reverse()
  for produs in produse_query:
    produs_q = Produse.objects.get(id=produs.produs_id)
    produs_q.pret_achizitie = produs.pret_achizitie
    produs_q.numar = produs.numar
    produs_q.data = produs.data
    produs_q.finalizat = produs.finalizat
    produse.append(produs_q)
  return render(request, 'istoric.html', {'produse': produse, 'cos': sum(cart.values()),
                                          'username': request.user.username, 'titlu': 'cos'})


def adauga_in_cos(request, produs_id):
  produs_id = str(produs_id)
  if not request.user.id:
      from django.contrib import messages
      messages.add_message(request, messages.INFO, 'Pentru a vizualiza coșul de cumpărături, trebuie să te loghezi!')
  if not request.session.has_key('cart'):
    request.session['cart']={produs_id: 1}
  else:
    all_cart = request.session['cart']
    if all_cart.get(produs_id):
      all_cart[produs_id]+=1
    else:
      all_cart[produs_id] = 1
    request.session['cart']=all_cart
  request.session.modified = True
  return getattr(views,'entry_detail')(request, produs_id)