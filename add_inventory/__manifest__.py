{
    "name": "add/remove_inventory",
    "summary": "Add or remove inventory",
    "version": "1.0",
    "sequence": 1,
    "depends": ["stock" , "purchase" , "l10n_in"],
    "description": "Add or remove inventory",
    "installable": True,
    "application": True, 
    "license": "LGPL-3",
    'data' : [
        'security/ir.model.access.csv',
        'wizards/inventory_wizard_views.xml',
        'views/menuitem.xml',
    ]
}
