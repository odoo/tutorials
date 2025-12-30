{
    'name': "Real Estate",
    'version': '1.0.0',
    'depends': ['base'],
    'author': "Mehul Kotak",
   'category': 'Tutorials',
    'description': "This Real Estate app in which the ad for any propertiues can add and also buyer can see and give thier price for that property",
    'application': True,
    'installable': True,
    # data files always loaded at installation
    'data': [
        'views/mymodule_view.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
}