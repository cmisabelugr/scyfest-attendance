from django.contrib import admin
from django.http import FileResponse
from pdfrw import PdfWriter, PdfReader
from io import BytesIO

from .models import *
from .ticket_creator import *

class TicketAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'active', 'checkedin')
    actions = ['generate_tickets']

    def generate_tickets(self, req, q):
        result = PdfWriter()
        ticket_list = list(q.all())
        lista = [ticket_list[i * 10:(i + 1) * 10] for i in range((len(ticket_list) + 10 - 1) // 10 )]
        for t in lista:
                result.addPage(PdfReader(generate_ticket([i.qr_text for i in t])).pages[0])
        file = BytesIO()
        result.write(file)
        file.seek(0)
        return FileResponse(file, as_attachment=True, filename='attempt1.pdf')
    generate_tickets.short_description = "Generar PDFs"








# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Points)
admin.site.register(BoothPoints)
