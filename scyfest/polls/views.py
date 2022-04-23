from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


from attendance.models import Ticket
from attendance.views import ticket_home


from .models import Poll, Vote, HasVoted, Option
from .forms import VoteForm

# Create your views here.

def polls_list(req):

    context = {}
    polls = Poll.objects.filter(active=True)
    voted = [p.poll for p in HasVoted.objects.filter(ticket=req.session.get("ticket", None))]
       


    return render(req, 'polls_list.html', {
        'polls' : polls,
        'voted':voted
    })

def vote(req,poll_id):
    poll = Poll.objects.filter(pk=poll_id).first()

    ticket_id=req.session.get("ticket_id", None)
    ticket = Ticket.objects.get(id=ticket_id)
    if not ticket:
        return HttpResponseForbidden()

    if not poll or not poll.user_can_vote(ticket):
        return redirect("ticket_home", ticket.qr_text)

    if req.method == 'POST':
        form = VoteForm(poll, req.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.poll = poll
            if not poll.anonymous:
                vote.ticket = ticket
            vote.save()
            form.save_m2m()

            h = HasVoted()
            h.ticket = ticket
            h.poll = poll
            h.save()

            return redirect("ticket_home", ticket.qr_text)
    else:
        return redirect("ticket_home", ticket.qr_text)
        form = VoteForm(poll)
        return render(req, 'vote.html', {'form':form, 'poll':poll})