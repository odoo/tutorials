{
    'name': 'Invoice Email Automation',
    'version': '1.0',
    'summary': 'Automatically sends emails when invoices are posted.',
    'description': """
        This module sends an email to customers when an invoice is posted, using an email template and a scheduled cron job.
    """,
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'data/cron_invoice_email.xml'
    ],
    'license': 'AGPL-3'
}
