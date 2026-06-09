{
    'name': 'Real Estate',            #Module name shown in Apps.
    'depends': [                      #specifies that this module depends on the base module, which is a core module of Odoo
        'base',
    ],
    'application': True,              #Shows module under Apps filter.
    'data': [                         #list of data files to be loaded when the module is installed or updated. These files typically contain XML or CSV data that defines the structure and behavior of the module.
        'security/ir.model.access.csv',
    ],
}
