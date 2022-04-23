from hashlib import blake2b
from tokenize import blank_re
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from attendance.models import Ticket


# Create your models here.
class Poll(models.Model):
    question = models.TextField(verbose_name="Pregunta")
    active = models.BooleanField(verbose_name="Activa")
    max_options = models.IntegerField(verbose_name="Respuestas máximas", default=1)
    anonymous = models.BooleanField(verbose_name="Anónima", default=True)

    class Meta:
        verbose_name = 'Encuesta'

    def __str__(self):
        return self.question

    @property
    def blank_votes(self):
        num = 0
        for v in self.vote_set.all():
            if v.is_blank():
                num +=1
        return num

    @property
    def null_votes(self):
        num = 0
        for v in self.vote_set.all():
            if v.is_null():
                num +=1
        return num
    
    @property
    def num_votes(self):
        return self.vote_set.count()

    def get_vote(self):
        v = Vote
        v.poll = self
        return v

    def user_can_vote(self,ticket):
        return self.active and not HasVoted.objects.filter(poll=self,ticket=ticket).exists()




class Option(models.Model):
    option_text = models.TextField(verbose_name="Texto")
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Option Image", blank=True)

    def num_votes(self):
        num = 0
        for v in self.poll.vote_set.all():
            if self in v.options.all() and not v.is_null():
                num += 1
        return num

    def __str__(self):
        return '{} - {}'.format(self.poll.question, self.option_text)

    class Meta:
        verbose_name = "Opciones de encuesta"

class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)
    options = models.ManyToManyField(to=Option, symmetrical=False, blank=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True, null=True)

    def is_blank(self):
        if self.options.count()==0:
            return True
        else:
            return False
    
    def is_null(self):
        if self.options.count() > self.poll.max_options:
            return True
        else:
            return False

    def __str__(self):
        if self.student:
            return 'Vote on {} by {}'.format(self.poll.question, self.student)
        else:
            return 'Vote on {}'.format(self.poll.question)

class HasVoted(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)