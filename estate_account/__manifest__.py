{
    'name': 'Real Estate Account',
    'category': 'Estate',
    'description': """This module is  sale estate account module""",
    'depends': ['estate', 'account'],
    'data': [
        "security/ir.model.access.csv",
        "report/estate_property_inherit_template.xml",
    ],
    'application': True,
    'license': 'OEEL-1',
    "sequence": 1,
}
