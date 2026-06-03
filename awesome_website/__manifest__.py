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
        "views/snippets/snippets.xml",
        "views/snippets/s_image_comparison.xml",
        "views/snippets/static_banner.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "awesome_website/static/src/interactions/**/*",
            "awesome_website/static/src/snippets/**/*",
            "awesome_website/static/src/components/**/*",
            ("remove", "awesome_website/static/src/interactions/**/*.edit.*"),
            ("remove", "awesome_website/static/src/snippets/**/*.edit.*"),
        ],
        "website.assets_inside_builder_iframe": [
            "awesome_website/static/src/snippets/**/*.edit.*",
        ],
        "website.website_builder_assets": [
            "awesome_website/static/src/builder/**/*",
        ],
        "web.assets_unit_tests": [
            "website/static/tests/builder/website_helpers.js",
            "awesome_website/static/tests/interactions/**/*",
            "awesome_website/static/tests/builder/**/*",
        ],
        "web.assets_unit_tests_setup": [
            "awesome_website/static/src/interactions/**/*",
            "awesome_website/static/src/snippets/**/*",
            "awesome_website/static/src/builder/**/*",
        ],
    },
    "license": "AGPL-3",
}
