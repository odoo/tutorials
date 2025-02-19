{
    'name' : "Real Estate Accounting",
    'summary' : """
        Estate and Account Made Easy
    """,
    'description' : """
        Estate and accounting can be very easy with Odoo
    """,

    'depends' : [
        "estate",
        "account"
    ],

    'data':[
        'report/estate_account_report_template.xml'
    ],

    "auto_install" : True,
    'license': "LGPL-3"
}
