{
    'name':"estate",
    'category': 'product',
    'summary':'Sale product module',
    'depends': ['base'],
    'website':'https://www.odoo.com/app/product',
    'installable': True,
    'application': True,
    'data':['security/ir.model.access.csv',
            'views/estate_property_views.xml'],
}