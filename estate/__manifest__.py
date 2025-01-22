{
    'name': "Real estate module!!",
    'version': '1.0',
    'depends': ['base'],
    'author': "Arthur Nanson",
    'category': 'Category',
    'description': """
    With this awesome module you can do awesome things like buy a house somehow maybe
    """,
    'application' : True,
    # data files always loaded at installation
    #'data' : ['data/estate.property.csv'],
    'data' : ['security/ir.model.access.csv',
              'views/estate_property_view.xml',
              'views/estate_menu.xml',
              ],
}
