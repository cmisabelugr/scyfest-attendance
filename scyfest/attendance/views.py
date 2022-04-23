from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from polls.forms import VoteForm


from .forms import TicketForm, TicketPureForm
from .models import Ticket, Points
from polls.models import Poll

# Create your views here.

def test_view(req):
    return render(req,"ticket.html")


def ticket_home(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        error = False
        if t.active:

            if t.name =="":
                t.name = "Sin nombre"

            req.session["ticket_id"] = t.id

            t.points = t.get_points()
            try:
                v = Poll.objects.get(active=True)
                t.has_voted = not v.user_can_vote(t)
                f = VoteForm(v)
                option_pictures = {o.id: o.image for o in v.option_set.all()}
            except Poll.DoesNotExist as e:
                v = None
                f = None
                option_pictures = {}
            context = {
                'error' :error,
                'ticket' : t,
                'poll' : v,
                'form' : f,
                'option_pictures' : option_pictures,
            }
            return render(req, "ticket.html", context=context)
        else:
            return render(req, "ticket_free.html")
    
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def ticket_history(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        error = False
        if t.active:

            if t.name =="":
                t.name = "Sin nombre"

            t.points = t.get_points()

            context = {
                'error' :error,
                'ticket' : t,
            }
            return render(req, "ticket_history.html", context=context)
        else:
            return render(req, "ticket_free.html")
    
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def change_name(req, qr_text, new_name):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        error = False
        
        t.name = new_name
        t.save()

        return redirect("ticket_home", qr_text)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    pass

@login_required
def door_scan(req):
    return render(req, "door_scan.html")

@login_required
def door_ticket(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        error = False
        

        if req.method =="POST":

            f = TicketPureForm(req.POST, req.FILES)

            if f.is_valid():
                t.name = f.cleaned_data['name']
                t.has_tui = f.cleaned_data['has_tui']
                t.from_college = f.cleaned_data['from_college']
                t.checkedin = f.cleaned_data['checkedin']
                t.active = f.cleaned_data['active']
                if f.cleaned_data['profile_picture']:
                    t.profile_picture = f.cleaned_data['profile_picture']
                t.save()

                return redirect("door_scan")
            else:
                print("Formulario inválido")
                print(f.errors)
                context = {
                'ticket' : t,
                'form' : f,
                }
                return render(req, "door_ticket.html", context=context)

        else:
            print("pues te lo muestro normal")
            data = {
                "name": t.name,
                "has_tui" : t.has_tui,
                "from_college": t.from_college,
                "checkedin" : t.checkedin,
                "active" : t.active,
                "profile_picture" : t.profile_picture
            }
            f = TicketPureForm(data)
            context = {
                'ticket' : t,
                'form' : f,
            }
            #print(f)
            print("Venga vamos")
            return render(req, "door_ticket.html", context=context)


        return render("ticket_home", qr_text)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    pass



def ranking_view(req):
    return render(req, "ranking.html")

def get_ranking(req):
    novatos = Ticket.objects.all()

    lista = []

    for n in novatos:
        if n.profile_picture:
            foto = n.profile_picture.url
        else:
            foto = "/static/img/perfil_defecto.png"
        novato = {
            "urlfoto" : foto,
            "mote" : n.name,
            "puntos" : n.get_points()
        }
        lista.append(novato)
        lista = sorted(lista, reverse=True, key = lambda i: i['puntos'])

    return JsonResponse(lista, safe=False)

@login_required
def scan_barra(req):
    return render(req, "barra_scan.html")

@login_required
def scan_taller(req):
    return render(req, "taller_scan.html")

@login_required
def scan_mercado(req):
    return render(req, "mercado_scan.html")

def points_barra(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        p = Points()
        p.ticket = t
        p.value = 1
        p.activity = "Barra"
        p.save()

        return redirect("scan_barra")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def points_taller(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        p = Points()
        p.ticket = t
        p.value = 3
        p.activity = "Taller"
        p.save()

        return redirect("scan_taller")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

def points_mercado(req, qr_text):
    try:
        t = Ticket.objects.get(qr_text=qr_text)
        p = Points()
        p.ticket = t
        p.value = 4
        p.activity = "Mercado"
        p.save()

        return redirect("scan_mercado")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()