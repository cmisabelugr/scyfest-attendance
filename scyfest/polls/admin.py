from django.contrib import admin, messages
from .models import Poll, Option, Vote, HasVoted

import csv
from django.http import HttpResponse, HttpResponseRedirect

# Register your models here.

class OptionInline(admin.TabularInline):
    model = Option
    readonly_fields = ['option_text', 'num_votes']
    extra = 0


class PollAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline
    ]

    list_display = (
        'question',
        'active',
        'anonymous',
        'num_votes'
    )

    fields = (
        'question',
        'active',
        'anonymous',
        'max_options',
        'num_votes',
        'blank_votes',
        'null_votes'
    )
    
    readonly_fields = (
        'num_votes',
        'blank_votes',
        'null_votes'
    )

    actions = ["export_as_csv", "duplicate_poll"]

    def export_as_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'
        ] = 'attachment; filename=polls.csv'
        writer = csv.writer(response)


        for poll in queryset:

            fields_poll = [
                'Pregunta', 'Votos', 'Votos blancos', 'Votos nulos'
            ]

            writer.writerow(fields_poll)

            row = [poll.question, poll.num_votes, poll.blank_votes, poll.null_votes]

            writer.writerow(row)

            if poll.anonymous:
                anon_fields = ['Opcion' , 'Num votos']
                writer.writerow(anon_fields)
                for option in poll.option_set.all():
                    row = [option.option_text, option.num_votes()]
                    writer.writerow(row)

            else:
                non_anon_fields = ['Colegial', 'Respuesta']
                writer.writerow(non_anon_fields)

                for vote in poll.vote_set.all():
                    for o in vote.options.all():
                        row = [vote.ticket, o.option_text]
                        writer.writerow(row)

        return response
    export_as_csv.short_description = "Exportar a CSV"

    def duplicate_poll(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, "Solo puedes seleccionar UNA encuesta", messages.ERROR)
        else:
            antigua = queryset.first()
            nueva = Poll()
            nueva.question = antigua.question
            nueva.active = antigua.active
            nueva.anonymous = antigua.anonymous
            nueva.save()
            for opcion in antigua.option_set.all():
                nuevaOpcion = Option()
                nuevaOpcion.option_text = opcion.option_text
                nuevaOpcion.poll = nueva
                nuevaOpcion.save()
            self.message_user(request, "Duplicada con éxito", messages.SUCCESS)
    duplicate_poll.short_description = "Duplicar encuesta"


admin.site.register(Poll, PollAdmin)
admin.site.register(Option)
admin.site.register(HasVoted)