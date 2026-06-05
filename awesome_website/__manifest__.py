{
    "name": "Awesome Website",
    "summary": """
        Companion addon for the Odoo JS Framework Training
    """,
    "description": """
        Companion addon for the Odoo JS Framework Training
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Tutorials",
    "version": "0.2",
    # any module necessary for this one to work correctly
    "depends": ["website"],
    "application": True,
    "installable": True,
    "data": [
        "data/images.xml",
        "views/snippets/s_image_comparison.xml",
        "views/snippets/s_timer.xml",
        "views/snippets/snippets.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "awesome_website/static/src/snippets/**/*.scss",
            "awesome_website/static/src/interactions/**/*.js",
            "awesome_website/static/src/snippets/s_image_comparison/image_comparison.js",
        ],
        "website.assets_inside_builder_iframe": [
            "awesome_website/static/src/snippets/**/*.edit.scss",
        ],
        "html_builder.iframe_add_dialog": [
            "awesome_website/static/src/snippets/**/*.preview.scss",
        ],
        "website.website_builder_assets": [
            "awesome_website/static/src/website_builder/image_comparison_snippet_option.*",
        ],
        "web.assets_unit_tests": [
            "awesome_website/static/tests/**/*",
        ],
        "web.assets_unit_tests_setup": [
            "awesome_website/static/src/**/*",
        ],
    },
    "license": "AGPL-3",
}
