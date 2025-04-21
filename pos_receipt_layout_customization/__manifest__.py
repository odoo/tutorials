{
    'name': 'pos receipt layout customization',
    'version': '1.0',
    'summary': 'pos receipt layout',
    'description': """
POS Preview and Receipt Layout Customization
====================
This module allows users to customize their Point of Sale (POS) receipt layout with a live preview directly from the backend. Businesses can define how receipts look when printed—selecting from multiple layout styles (Light, Lined, Boxed), and configure elements such as a custom header, footer, and logo.

It introduces an intuitive wizard for backend users to visualize and select the layout, and ensures that the selected format is dynamically applied in the actual printed receipts from the POS frontend.
    """,
    'author': 'Raghav Agiwal',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/pos_receipt_preview_templates.xml',
        'views/pos_receipt_render_templates.xml',
        'wizards/pos_receipt_layout_wizard_views.xml',
    ],
    'assets': {
         'point_of_sale._assets_pos': [
             'pos_receipt_layout_customization/static/src/**/*',
         ],
     },
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
