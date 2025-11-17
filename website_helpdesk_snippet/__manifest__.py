{
    'name': 'Website Helpdesk Snippet',
    'version': '1.0',
    'author': "sujal asodariya",
    'summary': 'Website snippet for displaying Helpdesk Tickets',
    'depends': ['website', 'helpdesk'],
    'data': [
        "data/helpdesk_snippet_tour.xml",
        "views/snippets/snippets.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'website_helpdesk_snippet/static/src/snippets/s_helpdesk_ticket/000.xml',
            "website_helpdesk_snippet/static/src/snippets/s_helpdesk_ticket/000.js",
        ],
        'website.assets_wysiwyg': [
            'website_helpdesk_snippet/static/src/snippets/s_helpdesk_ticket/options.js',
        ],
        'web.assets_tests': [
            'website_helpdesk_snippet/static/tests/tours/helpdesk_snippet_tour.js',
        ],
    },
    'application': False,
    'installable': True,
    'license': "LGPL-3",
}
