{
    'name': 'Website Helpdesk Tickets',
    'version': '1.0',
    'description': 'Display helpdesk tickets on the website via snippets.',
    'license': 'LGPL-3',
    'depends': [
        'website_helpdesk', 'website', 'web_editor'
    ],
    'data': [
        'views/snippets/snippets.xml',
        'views/snippets/s_helpdesk_tickets.xml',
    ],
    'auto_install': False,
    'application': False,
    'assets': {
         'web.assets_frontend': [
            'website_helpdesk_tickets/static/**/*',
            ('remove', 'website_helpdesk_tickets/static/src/snippets/s_helpdesk_tickets/options.js'),
        ],
        'website.assets_wysiwyg': [
            'website_helpdesk_tickets/static/src/snippets/s_helpdesk_tickets/options.js',
        ]
    }
}
