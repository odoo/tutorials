{
    "name": "Stamp Sign",
    "version": "1.0",
    "depends": ["sign"],
    "category": "Sign",
    "data": [
        "views/sign_template_views.xml",
        "data/sign_data.xml",
    ],
    "assets": {
        "sign.assets_pdf_iframe": [
            "stamp_sign/static/src/components/**/*",
        ],
    },
    "installable": True,
    "sequence": 1,
    "application": True,
    "license": "OEEL-1",
}
