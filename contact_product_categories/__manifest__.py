# -*- coding: utf-8 -*-
{
    'name': 'Contact Product Categories',
    'summary': 'Bind internal product categories to contacts and browse products by those categories.',
    "version": "19.0.1.0.0",
    'category': 'Contacts',
    'depends': ['base', 'contacts', 'product', "sale_management"],
    'data': [
        "data/partner_status_data.xml",
        "views/partner_convert_wizard_views.xml",
        "views/res_partner_views.xml",
        "views/product_template_views.xml",
        "views/partner_status_views.xml",
        "views/partner_products_view_views.xml",
        "views/market_view_report_run_views.xml",
        "security/ir.model.access.csv"
    ],
    "assets": {
      "web.assets_backend": [
          "contact_product_categories/static/src/js/company_type_confirm.js"
      ]
    },
    'application': False,
    'author': 'Denys Azhymov (azhimov93@gmail.com)',
    'license': 'LGPL-3'
}
