# -*- coding: utf-8 -*-
{
    'name': 'PDF Preview Report',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Add a Preview before PDF export option to account reports',
    'description': """
This module adds a preview dialog before exporting account reports to PDF.
    """,
    'depends': ['account_reports'],
    'assets': {
        'web.assets_backend': [
            'pdf_preview_report/static/src/components/pdf_preview/pdf_preview.js',
            'pdf_preview_report/static/src/components/pdf_preview/pdf_preview.xml',
        ],
    },
    'license': 'LGPL-3',
}
