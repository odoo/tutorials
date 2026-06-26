{
    'name': "Discuss AI Search",
    'version': '1.0',
    'category': 'Discuss',
    'summary': "Categorize and summarize Discuss messages using AI",
    'depends': ['mail'],
    'data': [
        'data/discuss_demo_data.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'discuss_ai_search/static/src/**/*',
        ],
    },
    'author': "Parth Sawant",
    'license': 'LGPL-3',
}