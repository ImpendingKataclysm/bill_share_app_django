from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


def generate_pdf(results, total_billing_amount):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="results.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    story = []

    styles = getSampleStyleSheet()
    title = Paragraph(f'Total Billing Amount: {total_billing_amount}', styles['Title'])
    story.append(title)

    for result in results:
        story.append(Paragraph(f"{result['name']} owes {result['share_amount']}", styles['Normal']))

    doc.build(story)

    return response
