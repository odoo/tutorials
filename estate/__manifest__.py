{
    "name": "Real Estate",
    "version": "0.1",
    "depends": ["base"],
    "author": "Madhav Pancholi",
    "category": "Real Estate",
    "description": """
        Manage properties, rentals, and real estate sales.
    """,
    "installable": True,
    "application": True,
    "data": [
        "data/auto_reject_offer_cron.xml",
        "security/ir.model.access.csv",
        "security/demo_group.xml",
        "security/salesperson_own_records_rule.xml",
        "views/estate_property_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_menus.xml",
        "views/res_users_view.xml",
    ],
    "demo": [],
}
