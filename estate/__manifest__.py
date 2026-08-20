{
    "name": "estate",
    "version": "1.0",
    "depends": ["base", "mail"],
    "category": "tutorials",
    "author": "sadeo-odoo",
    "license": "LGPL-3",
    "description": "A real estate module",
    "installable": True,
    "application": True,
        "data": [
        # Security
        "security/ir.model.access.csv",
        # Data
        "data/booking_sequence.xml",
        "data/payment_sequence.xml",
        "data/estate_property_offer_cron.xml",
        'data/mail_template.xml',
        # Views
        "views/estate_booking_views.xml",  # defines action
        "views/estate_booking_wizard_views.xml",  # wizard views
        "views/estate_payment_views.xml",  # payments
        "views/estate_property_visit_views.xml",  # defines action_open_related_visits used by property view
        "views/estate_property_views.xml",  # property view uses booking + action_open_related_visits
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/res_users_views.xml",
        # Menus (keep last)
        "views/estate_menus.xml",
    ],
}
