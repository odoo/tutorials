{
    'name': 'Hackathon Video Monitoring',
    'version': '1.0',
    'summary': 'Hackathon participant video recording',
    'author': 'Pranjali',
    'depends': ['portal', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/hackathon_menu.xml',
        'views/hackathon_session_views.xml',
        'views/hackathon_team_views.xml',
        'views/hackathon_participant_views.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'hackathon_module/static/src/js/recorder.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
