{
    'name': "Lead Generation By Ads",
    'version': "1.0",
    'depends': ["base_automation", "crm"],
    'author': "Prathmesh Soni (pdso)",
    'summary': "A module for generates and tracks leads from Google Ads and Facebook Ads lead form extensions.",
    'description': "This module generates leads from ads by utilizing lead form extensions from Google Ads and Facebook Ads. It also tracks the source of each lead.",
    'data': [
        "views/crm_lead_views_inherit.xml",
        "data/ir_config_parameter_data.xml",
    ],
    'sequence': 1,
    'application': True,
    'installable': True,
    'maintainer': "Prathmesh Soni (pdso)",
    'license': "LGPL-3",
}
