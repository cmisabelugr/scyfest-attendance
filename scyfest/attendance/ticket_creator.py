from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter
import qrcode
from io import BytesIO
import os
from scyfest.settings import BASE_DIR

IN_FILE = os.path.join(BASE_DIR, './attendance/base.pdf')
OUT_FILE = './output.pdf'
ON_PAGE_INDEX = 0
UNDERNEATH = False

def new_content(qrcodes):
    fpdf = FPDF(orientation="landscape", format=(52,62))
    fpdf.add_page()

    for (i, qr_text) in enumerate(qrcodes):
        img = qrcode.make("https://fest.ruralinfra.com/t/{}".format(qr_text))
        #for j in range(3):
        fpdf.image(img.get_image(), x=19, y=14, h=24, w=24)    

    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]

def generate_ticket(qrcodes):
    result = BytesIO()
    reader = PdfReader(IN_FILE)
    overlay = new_content(qrcodes)
    pm = PageMerge(reader.pages[0])
    pm.add(overlay, prepend=UNDERNEATH)
    pm.render()
    #PageMerge(writer.pagearray[ON_PAGE_INDEX]).add(new_content(), prepend=UNDERNEATH).render()
    writer = PdfWriter()
    writer.write(result, reader)
    result.flush()
    result.seek(0)
    return result