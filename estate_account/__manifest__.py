{
    'name': "Estate Account",
    'version': '1.0',
    'depends': ['base','real_estate','account'],
    'author': "Rishav Shah (sris)",
    'category': 'Estate Account',
    'icon':'/estate_account/static/src/img/estate_account_icon.png',
    'description': """    
        Estate Account module used for invoicing
      """,
    'installable':True,
    'application':True,
    'license':'LGPL-3',
    'data':[
        'report/estate_property_templates.xml',
    ]
}
