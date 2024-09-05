{
    'name': "estate_event",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'estate', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/estate_property_event_view.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
