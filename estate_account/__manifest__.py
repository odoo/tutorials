{
    "name": "estate_account",
    "version": "0.1",
    "description": """ 
    The estate account manage accounts and help to generate invoice for customer of estate property
    """,
    "depends": ["base", "estate", "account"],
    "data": [
        "views/estate_property_view.xml",
        "views/account_menus.xml",
    ],
    "application": True,
    "license": "AGPL-3",
}
