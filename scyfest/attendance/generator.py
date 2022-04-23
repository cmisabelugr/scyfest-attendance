import sys
from fpdf import FPDF
from pdfrw import PageMerge, PdfReader, PdfWriter
import qrcode

IN_FILE = './base.pdf'
OUT_FILE = './output.pdf'
ON_PAGE_INDEX = 0
UNDERNEATH = False

qrcodes = [f"https://entradas.ruralinfra.com/t/test{i}" for i in range(10)]
def new_content(qrcodes):
    fpdf = FPDF(orientation="landscape", format=(190,250))
    fpdf.add_page()

    for (i, qr_text) in enumerate(qrcodes):
        img = qrcode.make(qr_text)
        for j in range(3):
            fpdf.image(img.get_image(), x=60+j*70, y=i*19, h=19, w=19)    

    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]

reader = PdfReader(IN_FILE)
overlay = new_content(qrcodes)
pm = PageMerge(reader.pages[0])
pm.add(overlay, prepend=UNDERNEATH)
pm.render()
#PageMerge(writer.pagearray[ON_PAGE_INDEX]).add(new_content(), prepend=UNDERNEATH).render()
writer = PdfWriter()
writer.write(OUT_FILE, reader)