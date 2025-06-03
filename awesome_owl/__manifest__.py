{
    "name": "Awesome Owl",
    "summary": """
     Odoo JS Framework Training
    """,
    "description": """
     Odoo JS Framework Training
    """,
    "author": "Kashish",
    "website": "https://www.odoo.com",
    "category": "Tutorials",
    "version": "0.2",
    "depends": ["base", "web"],
    "application": True,
    "installable": True,
    "auto_install": True,
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "awesome_owl.assets_playground": [
            ("include", "web._assets_helpers"),
            "web/static/src/scss/pre_variables.scss",
            "web/static/lib/bootstrap/scss/_variables.scss",
            "web/static/lib/bootstrap/scss/_maps.scss",
            ("include", "web._assets_bootstrap"),
            ("include", "web._assets_core"),
            "web/static/src/libs/fontawesome/css/font-awesome.css",
            "awesome_owl/static/src/**/*",
        ],
    },
    "license": "AGPL-3",
}
