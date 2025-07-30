{
    'name': "Website Autocomplete GST",
    'version': "1.0",
    'category': "Website/Website",
    'summary': "Get Auto-completed Company address based on VAT",
    'depends': [
        'website_sale'
    ],
    'description': """
        This module adds an option of "do you want tax credit" during checkout process in website and upon entering a valid VAT number auto-completes company address details.
    """,
    'data': [
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_autocomplete_gst/static/src/js/**/*.js',
        ],
    },
    'installable': True,
    'license': "AGPL-3"
}
