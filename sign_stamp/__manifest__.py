{
    "name": "Sign Stamp",
    "version": "1.0",
    "depends": ["sign"],
    "category": "Sign",
    "data": [
        "data/sign_data.xml",
        "views/sign_request_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sign_stamp/static/src/components/sign_request/*",
            "sign_stamp/static/src/dialogs/*",
        ],
        "sign.assets_public_sign": [
            "sign_stamp/static/src/components/sign_request/*",
            "sign_stamp/static/src/dialogs/*",
        ],
    },
    "installable": True,
    "application": True,
    "license": "OEEL-1",
}
