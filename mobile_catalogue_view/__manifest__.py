# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Mobile Catalog View",
    'description': "Redesign the mobile catalog view",
    'version': '1.0',
    'author': "nmak",
    'depends': ["sale"],
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mobile_catalogue_view/static/src/scss/style.scss',
            'mobile_catalogue_view/static/src/js/product_image_popup.js',
        ],
    },
    'installable': True,
    'license': "LGPL-3",
}
