{
    "name": "Stamp Sign",
    "version": "1.0",
    "depends": ["sign"],
    "category": "Sign",
    "data": [
        "data/sign_data.xml",
        "views/sign_template_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "stamp_sign/static/src/components/sign_request/*",
            "stamp_sign/static/src/dialogs/*",
        ],
        "sign.assets_public_sign": [
            "stamp_sign/static/src/components/sign_request/*",
            "stamp_sign/static/src/dialogs/*",
        ],
    },
    "installable": True,
    "sequence": 1,
    "application": True,
    "license": "OEEL-1",
}
