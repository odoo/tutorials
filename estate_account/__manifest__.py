{
    'name':"estate_account",
    'author':"Odoo S.A.",
    'licence':"none",
    
    'summary': """
        Link module between estate and account!
    """,

    'description': """
        Lots of Houses!!"
    """,

    'depends': [
        'estate',
        'account',

    ],
    
    'application': True,
    'installable': True,
    'data':[
        'security/ir.model.access.csv',
    ],
}
