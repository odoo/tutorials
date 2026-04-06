{
    'name': 'Estate',  # this display the name of our menu.if we removed it ui will show empty name or some weird ui
    'depends': ['base'],  # this define dependencies.odoo install this before our module.if we remove it odoo assume no dependency.the base dependency will always install even if we leave depends field empty.
    'category': 'Tutorials',  # this define the category of our module.ex:sales,knowledge etc. if we remove this our module goes to uncategorized no function issue only ui impact
    'application': True, #marks module as main app because of this app get it's own icon and become visible in ui.if we make it false or remove it our app/module will not shown in ui.the default value of application is false
    'installable': True, #control wheather module can be installed or not.if True we can install it,if false then module can't be install and will be hidden.the default value is True
    'version': '1.0',
    'author': 'vikvi', #shows who created the module.there will be no technical issue if we remove it
    'license': 'LGPL-3', #define legel licence of your moudule it's open source license
    'data' : [
        'security/ir.model.access.csv'
    ],
}
