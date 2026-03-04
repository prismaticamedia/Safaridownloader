from xhtml2pdf import pisa
def convert_html_to_pdf(source_html, output_filename):
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file,
            encoding='UTF-8'
        )
    return pisa_status.err

source = "<html><body><h1>Hello World</h1></body></html>"
err = convert_html_to_pdf(source, "test.pdf")
print("Error status:", err)
