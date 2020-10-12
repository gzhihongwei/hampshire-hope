import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

# this doesn't work well

with open('./Hampshire County Guide to Drug & Alcohol Treatment Resources.pdf', 'rb') as pdf_fd:
    pdf_viewer = SimplePDFViewer(pdf_fd)
    pdf_viewer.navigate(2)
    pdf_viewer.render()
    print(pdf_viewer.canvas.strings)
