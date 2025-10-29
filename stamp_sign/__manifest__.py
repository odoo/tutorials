# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stamp Sign",
    "version": "1.0",
    "depends": ["sign"],
    "category": "Sign",
    "author": "arkp",
    "data": [
        "data/sign_data.xml",
        "views/sign_request_templates.xml",
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
    "application": True,
    "license": "LGPL-3",
}
